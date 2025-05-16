import os
import tempfile
import uuid
from manim import *
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.scene import Scene, SceneStatus
from app.models.video import Video
from app.core.config import settings
import httpx

def generate_animation(scene_id: uuid.UUID):
    """Generate an animation for a scene."""
    db = SessionLocal()
    try:
        # Get scene from database
        scene = db.query(Scene).filter(Scene.id == scene_id).first()
        if not scene:
            return
        
        # Update scene status
        scene.status = SceneStatus.PROCESSING
        db.commit()
        
        try:
            # Generate manim code from prompt using Groq
            scene_code = generate_manim_code(scene.prompt)
            
            # Save generated code to scene
            scene.code = scene_code
            db.commit()
            
            # Set up file paths
            video_filename = f"{scene_id}.mp4"
            video_path = os.path.join(settings.VIDEO_DIR, video_filename)
            
            # Ensure directory exists
            os.makedirs(settings.VIDEO_DIR, exist_ok=True)
            
            # Create a temporary file to write the scene class
            with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as f:
                temp_file_path = f.name
                f.write(scene_code)
            
            try:
                # Execute manim to generate the animation
                result = os.system(f"manim {temp_file_path} -o {video_path}")
                
                # Check if manim execution was successful
                if result != 0:
                    raise Exception(f"Manim execution failed with exit code {result}")
                
                # Update scene with video URL and status
                scene.video_url = f"/media/videos/{video_filename}"
                scene.status = SceneStatus.COMPLETED
                
                # Create video entry
                video = Video(
                    scene_id=scene.id,
                    file_path=video_path,
                    duration=5.0  # Default duration, can be updated later
                )
                db.add(video)
                db.commit()
                
            except Exception as e:
                scene.status = SceneStatus.FAILED
                scene.code = f"{scene_code}\n\n# Error: {str(e)}"
                db.commit()
                print(f"Animation generation failed: {e}")
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
            
        except Exception as e:
            # Update scene status to failed in case of error
            scene.status = SceneStatus.FAILED
            db.commit()
            raise e
            
    finally:
        db.close()

def generate_manim_code(prompt: str) -> str:
    """Generate manim code from a prompt using Groq."""
    # Set Groq API key
    groq_api_key = settings.GROQ_API_KEY
    
    # Define the system message
    system_message = """
    You are an expert in Manim, a Python library for creating mathematical animations. 
    Your task is to generate Manim code based on the user's description of an animation.
    The code should be complete and runnable.
    It should define a Scene class that can be rendered by Manim.
    The animation should not be too complex and should render within a reasonable time.
    
    IMPORTANT RULES:
    1. Ensure your Python code is syntactically correct with properly matching parentheses, brackets, and indentation.
    2. Verify your self.play() calls have balanced parentheses.
    3. Do not include any markdown formatting in your code.
    4. Do NOT include any 'if __name__ == "__main__"' block or any code that would render the scene.
    5. Make sure your code defines a single Scene class that inherits from Scene.
    6. All animation code must be within the construct method.
    7. Use only standard Manim objects and methods.
    8. Do not use any external libraries besides manim.
    """
    
    # Create the prompt for Groq
    user_message = f"Create a Manim animation for: {prompt}. Make it visually appealing and professional. Include helpful comments in the code that explain what each section does."
    
    # Groq API endpoint
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    
    # Generate the code using Groq
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    # Make the API request
    response = httpx.post(api_url, json=data, headers=headers)
    response_data = response.json()
    
    # Extract the code from the response
    code = response_data["choices"][0]["message"]["content"]
    
    # Clean up the code (remove markdown code blocks if present)
    code = clean_code(code)
    
    # Ensure the code contains a proper Scene class
    if "class" not in code or "Scene" not in code:
        # The model failed to generate a proper scene, let's add a default one
        code = """from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Display a message indicating there was an issue with generation
        title = Text("Animation Could Not Be Generated", font_size=42)
        title.to_edge(UP)
        
        message = Text("The prompt could not be processed correctly.", font_size=28)
        message.next_to(title, DOWN, buff=1)
        
        suggestion = Text("Try a different prompt with clearer instructions.", font_size=24)
        suggestion.next_to(message, DOWN, buff=0.5)
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(message))
        self.wait(0.5)
        self.play(FadeIn(suggestion))
        self.wait(2)
"""
    
    return code

def clean_code(code: str) -> str:
    """Clean up generated code to ensure it's valid Python."""
    # Remove markdown code blocks
    if "```python" in code:
        code = code.split("```python")[1]
    elif "```" in code:
        code = code.split("```")[1]
    
    if code.endswith("```"):
        code = code.rsplit("```", 1)[0]
    
    # Remove any lines with just the word "Python" (common in AI responses)
    lines = code.strip().split('\n')
    lines = [line for line in lines if line.strip() != "Python"]
    
    # Fix common typos in import statements
    for i, line in enumerate(lines):
        if "from maniml import" in line:
            lines[i] = line.replace("maniml", "manim")
    
    # Completely remove any if __name__ == "__main__" block since this will be handled by the backend
    cleaned_lines = []
    skip_block = False
    
    for line in lines:
        if 'if __name__ == "__main__"' in line or "if __name__ == '__main__'" in line:
            skip_block = True
            continue
        
        if skip_block and (line.strip() == "" or line.startswith(" ") or line.startswith("\t")):
            continue
        elif skip_block:
            skip_block = False
        
        cleaned_lines.append(line)
    
    # Rejoin the lines
    code = '\n'.join(cleaned_lines)
    
    # Ensure code is properly indented and parentheses are balanced
    try:
        # Try to compile the code to catch syntax errors
        compile(code, '<string>', 'exec')
    except SyntaxError as e:
        # If there's a syntax error, add basic error handling
        if "unmatched ')'" in str(e):
            # Fix unbalanced parentheses in self.play() calls
            code = fix_unbalanced_parentheses(code)
    except NameError:
        # Sometimes there are undefined variables
        pass
    
    # Add imports if not present
    if "from manim import" not in code:
        code = "from manim import *\n\n" + code
    
    return code.strip()

def fix_unbalanced_parentheses(code: str) -> str:
    """Basic function to attempt to fix unbalanced parentheses."""
    # Find self.play calls with potential issues
    lines = code.split('\n')
    in_play_block = False
    play_start_line = -1
    fixed_lines = []
    
    for i, line in enumerate(lines):
        if "self.play(" in line:
            # Start of a self.play block
            in_play_block = True
            play_start_line = i
            # Count opening and closing parentheses
            open_count = line.count('(')
            close_count = line.count(')')
            
            if open_count > close_count:
                # We're in a multi-line self.play call
                fixed_lines.append(line)
            else:
                # It's a single line call, add it directly
                fixed_lines.append(line)
                in_play_block = False
        elif in_play_block:
            # We're in the middle of a play block
            open_count = line.count('(')
            close_count = line.count(')')
            
            # If this line has a comma followed by a closing parenthesis, it might be malformed
            if "," in line and ")" in line and "," in line.split(")")[0]:
                # Replace problematic comma+paren pattern
                line = line.replace("),", ")")
            
            fixed_lines.append(line)
            
            # Check if we've closed the block
            if close_count > open_count:
                in_play_block = False
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines) 