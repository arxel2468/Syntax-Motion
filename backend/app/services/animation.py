import os
import tempfile
import uuid
from manim import *
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.scene import Scene, SceneStatus
from app.models.video import Video
from app.core.config import settings
import openai

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
            # Generate manim code from prompt using OpenAI
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
            
            # Execute manim to generate the animation
            os.system(f"manim {temp_file_path} -o {video_path}")
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
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
            # Update scene status to failed in case of error
            scene.status = SceneStatus.FAILED
            db.commit()
            raise e
            
    finally:
        db.close()

def generate_manim_code(prompt: str) -> str:
    """Generate manim code from a prompt using OpenAI."""
    # Set OpenAI API key
    openai.api_key = settings.OPENAI_API_KEY
    
    # Define the system message
    system_message = """
    You are an expert in Manim, a Python library for creating mathematical animations. 
    Your task is to generate Manim code based on the user's description of an animation.
    The code should be complete and runnable.
    It should define a Scene class that can be rendered by Manim.
    The animation should not be too complex and should render within a reasonable time.
    """
    
    # Create the prompt for OpenAI
    user_message = f"Create a Manim animation for: {prompt}. Make it visually appealing and professional."
    
    # Generate the code using OpenAI
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        max_tokens=1000,
        temperature=0.7
    )
    
    # Extract the code from the response
    code = response.choices[0].message.content
    
    # Clean up the code (remove markdown code blocks if present)
    if code.startswith("```python"):
        code = code.split("```python")[1]
    if code.startswith("```"):
        code = code.split("```")[1]
    if code.endswith("```"):
        code = code.rsplit("```", 1)[0]
    
    # Add imports if not present
    if "from manim import" not in code:
        code = "from manim import *\n\n" + code
    
    return code 