import os
import tempfile
import uuid
import shutil
from manim import *
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.scene import Scene, SceneStatus
from app.models.video import Video
from app.core.config import settings
import httpx
import re
import subprocess
import traceback

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
            # Use a temporary directory instead of a single file for better isolation
            temp_dir = tempfile.mkdtemp()
            try:
                temp_file_path = os.path.join(temp_dir, "scene.py")
                with open(temp_file_path, "w") as f:
                    f.write(scene_code)
                
                # Make sure the generated code is safe to execute
                if not is_code_safe(scene_code):
                    raise Exception("Generated code contains potentially unsafe operations")
                
                # Execute manim to generate the animation with a timeout
                command = [
                    "timeout", 
                    str(settings.ANIMATION_TIMEOUT),
                    "manim", 
                    temp_file_path, 
                    "-o", 
                    video_path,
                    "--quality", 
                    "m"  # Medium quality for faster rendering
                ]
                
                # Run the command
                process = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=settings.ANIMATION_TIMEOUT
                )
                
                # Check if manim execution was successful
                if process.returncode != 0:
                    error_message = f"Manim execution failed with code {process.returncode}:\n"
                    error_message += process.stderr
                    raise Exception(error_message)
                
                # Check if the video file actually exists
                if not os.path.exists(video_path):
                    raise Exception("Video file was not created after rendering")
                
                # Update scene with video URL and status
                scene.video_url = f"/media/videos/{video_filename}"
                scene.status = SceneStatus.COMPLETED
                
                # Get video duration using ffprobe
                duration = 0.0
                try:
                    duration_cmd = [
                        "ffprobe", 
                        "-v", "error", 
                        "-show_entries", "format=duration", 
                        "-of", "default=noprint_wrappers=1:nokey=1", 
                        video_path
                    ]
                    duration_output = subprocess.run(
                        duration_cmd, 
                        capture_output=True, 
                        text=True
                    )
                    if duration_output.returncode == 0:
                        duration = float(duration_output.stdout.strip())
                except Exception as e:
                    print(f"Error getting video duration: {str(e)}")
                
                # Create video entry
                video = Video(
                    scene_id=scene.id,
                    file_path=video_path,
                    duration=duration
                )
                db.add(video)
                db.commit()
                
            except Exception as e:
                scene.status = SceneStatus.FAILED
                scene.code = f"{scene_code}\n\n# Error: {str(e)}"
                db.commit()
                print(f"Animation generation failed: {e}")
                traceback.print_exc()
            finally:
                # Clean up temporary directory
                shutil.rmtree(temp_dir, ignore_errors=True)
            
        except Exception as e:
            # Update scene status to failed in case of error
            scene.status = SceneStatus.FAILED
            scene.code = f"# Error during code generation: {str(e)}"
            db.commit()
            print(f"Animation generation failed during preparation: {e}")
            traceback.print_exc()
            
    finally:
        db.close()

def generate_manim_code(prompt: str) -> str:
    """Generate manim code from a prompt using Groq."""
    # Set Groq API key
    groq_api_key = settings.GROQ_API_KEY
    
    # Define the system message with better instructions
    system_message = """
    You are an expert in Manim, a Python library for creating mathematical animations. 
    Your task is to generate Manim code based on the user's description of an animation.
    Follow these strict guidelines:

    1. Start with standard imports:
       from manim import *
       import numpy as np
    
    2. Define exactly ONE Scene class that inherits from Scene with a construct method.
    
    3. Use only standard Manim objects and methods from the latest version.
    
    4. Keep animations simple and efficient - avoid creating hundreds of objects.
    
    5. Use proper Manim syntax for all animations, including:
       - wait() with specific durations
       - play() for all animations
       - proper animation methods (Create, FadeIn, etc.)
    
    6. Use proper coordinate system (UP, DOWN, LEFT, RIGHT, ORIGIN).
    
    7. Include helpful comments to explain what the code does.
    
    8. DO NOT include any markdown code blocks, explanations outside the code, or "if __name__ == '__main__'" blocks.
    
    9. DO NOT use external libraries other than manim and numpy.
    
    10. Limit animation complexity to ensure it renders within 2 minutes.
    
    11. Use consistent and reasonable timing for animations (e.g., wait(1) not wait(10)).
    
    12. Handle potential errors gracefully, like checking if objects exist before manipulating them.
    
    IMPORTANT: Return ONLY the Python code - no explanations or additional text before or after.
    """
    
    # Create the prompt for Groq
    user_message = f"Create a Manim animation for the following: {prompt}. The animation should be visually appealing, professional, and render within 2 minutes. Use specific colors, positions, and timings."
    
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
        "max_tokens": 1500,
        "temperature": 0.5
    }
    
    # Make the API request
    response = httpx.post(api_url, json=data, headers=headers, timeout=30)
    response_data = response.json()
    
    # Extract the code from the response
    code = response_data["choices"][0]["message"]["content"]
    
    # Clean up the code
    code = clean_code(code)
    
    # Add safety measures to the code
    code = add_safety_measures(code)
    
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
    
    # Completely remove any if __name__ == "__main__" block
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
    
    # Ensure code is balanced with parentheses
    code = '\n'.join(cleaned_lines)
    code = fix_unbalanced_parentheses(code)
    
    # Add imports if not present
    if "from manim import" not in code:
        code = "from manim import *\nimport numpy as np\n\n" + code
    elif "import numpy as np" not in code and "import numpy" not in code:
        # Add numpy import if using manim but not numpy
        code = code.replace("from manim import", "from manim import *\nimport numpy as np\n")
    
    # Add a default scene class if none exists
    if "class" not in code or "Scene" not in code:
        code = """from manim import *
import numpy as np

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
    
    return code.strip()

def fix_unbalanced_parentheses(code: str) -> str:
    """Basic function to attempt to fix unbalanced parentheses."""
    lines = code.split('\n')
    in_play_block = False
    fixed_lines = []
    
    for i, line in enumerate(lines):
        if "self.play(" in line:
            # Start of a self.play block
            in_play_block = True
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

def add_safety_measures(code: str) -> str:
    """Add safety measures to the generated code."""
    # Add timeout to any potentially infinite loops
    # Find all 'while' loops without a timeout
    while_pattern = r'(\s+)(while\s+.*:)'
    
    def add_timeout_to_while(match):
        indent = match.group(1)
        while_statement = match.group(2)
        timeout_var = f"_timeout_counter_{uuid.uuid4().hex[:8]}"
        return f"{indent}{timeout_var} = 0\n{indent}{while_statement}\n{indent}    {timeout_var} += 1\n{indent}    if {timeout_var} > 1000:\n{indent}        break"
    
    code = re.sub(while_pattern, add_timeout_to_while, code)
    
    # Add timeout to construct method to prevent infinite animations
    construct_pattern = r'(def\s+construct\s*\(.+\):)'
    
    def add_timeout_to_construct(match):
        construct_def = match.group(1)
        return f"{construct_def}\n        # Add timeout for safety\n        _start_time = np.time.time()\n"
    
    code = re.sub(construct_pattern, add_timeout_to_construct, code)
    
    # Add time check before each animation
    play_pattern = r'(\s+)(self\.play\(.*\))'
    
    def add_time_check_to_play(match):
        indent = match.group(1)
        play_statement = match.group(2)
        return f"{indent}# Check timeout\n{indent}if np.time.time() - _start_time > {settings.ANIMATION_TIMEOUT - 10}:\n{indent}    self.wait(0.1)\n{indent}    return\n{indent}{play_statement}"
    
    code = re.sub(play_pattern, add_time_check_to_play, code)
    
    return code

def is_code_safe(code: str) -> bool:
    """Check if the generated code is safe to execute."""
    # Check for potentially dangerous imports
    dangerous_imports = [
        "os", "subprocess", "sys", "shutil", "pathlib",
        "socket", "requests", "urllib", "http", "ftplib",
        "importlib", "pickle", "marshal", "builtins", "ctypes"
    ]
    
    # Remove comments to prevent hiding dangerous code in comments
    code_without_comments = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
    
    # Check for suspicious imports
    import_pattern = r'import\s+(\w+)|from\s+(\w+)\s+import'
    imports = re.findall(import_pattern, code_without_comments)
    
    # Flatten and filter the imports list
    flat_imports = [imp for sublist in imports for imp in sublist if imp]
    
    for imp in flat_imports:
        if imp in dangerous_imports:
            return False
    
    # Check for exec, eval or other dangerous functions
    dangerous_functions = [
        r'exec\(', r'eval\(', r'__import__\(', 
        r'open\(', r'file\(', r'compile\('
    ]
    
    for func in dangerous_functions:
        if re.search(func, code_without_comments):
            return False
    
    # Check for accessing filesystem
    filesystem_patterns = [
        r'\.read\(', r'\.write\(', r'\.open\(',
        r'os\.', r'subprocess\.', r'shutil\.', r'pathlib\.'
    ]
    
    for pattern in filesystem_patterns:
        if re.search(pattern, code_without_comments):
            return False
    
    return True
