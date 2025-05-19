import os
import tempfile
import uuid
import asyncio
import re
from manim import *
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import async_session_maker
from app.models.scene import Scene, SceneStatus
from app.models.video import Video
from app.core.config import settings
import httpx
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for fallback scenes
DEFAULT_SCENE_TEMPLATE = """from manim import *

class GeneratedScene(Scene):
    def construct(self):
        title = Text("Animation Could Not Be Generated", font_size=42)
        self.play(Write(title))
        self.wait(2)
"""

FALLBACK_SCENE_TEMPLATE = """from manim import *

class FallbackScene(Scene):
    def construct(self):
        title = Text("API Error", font_size=42, color=RED)
        self.play(Write(title))
        self.wait(2)
"""

async def generate_animation(scene_id: uuid.UUID):
    """Generate an animation for a scene (async version)."""
    async with async_session_maker() as db:
        scene = await db.get(Scene, scene_id)
        if not scene:
            logger.error(f"Scene {scene_id} not found")
            return

        scene.status = SceneStatus.PROCESSING
        await db.commit()

        try:
            scene_code = await generate_manim_code(scene.prompt)
            scene.code = scene_code
            await db.commit()

            video_filename = f"{scene_id}.mp4"
            video_path = os.path.join(settings.VIDEO_DIR, video_filename)
            os.makedirs(settings.VIDEO_DIR, exist_ok=True)

            with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as f:
                temp_file_path = f.name
                f.write(scene_code)

            try:
                class_name = extract_class_name(scene_code) or "Scene"
                cmd = f"manim {temp_file_path} {class_name} -qm -o {video_path}"

                # Run Manim asynchronously with timeout
                proc = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                try:
                    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=60)
                except asyncio.TimeoutError:
                    proc.kill()
                    await proc.wait()
                    raise Exception("Animation rendering timed out after 60 seconds")

                if proc.returncode != 0:
                    error_output = stderr.decode() if stderr else "Unknown error"
                    raise Exception(f"Manim execution failed: {error_output}")

                # Find and move the generated video
                media_dir = os.path.join(os.path.dirname(video_path), "media")
                video_files = [os.path.join(root, file)
                               for root, _, files in os.walk(media_dir)
                               for file in files if file.endswith(".mp4")]

                if video_files:
                    latest_video = max(video_files, key=os.path.getctime)
                    os.rename(latest_video, video_path)
                else:
                    raise Exception("No video file generated")

                scene.video_url = f"/media/videos/{video_filename}"
                scene.status = SceneStatus.COMPLETED

                video = Video(scene_id=scene.id, file_path=video_path, duration=5.0)
                db.add(video)
                await db.commit()

            except Exception as e:
                scene.status = SceneStatus.FAILED
                scene.code = f"{scene_code}\n\n# Error: {str(e)}"
                await db.commit()
                logger.error(f"Animation generation failed: {e}")
            finally:
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)

        except Exception as e:
            scene.status = SceneStatus.FAILED
            await db.commit()
            logger.error(f"Animation error: {e}")

def extract_class_name(code: str) -> str:
    """Extract Scene class name."""
    match = re.search(r'class\s+(\w+)\s*\(\s*(?:manim\.)?Scene\s*\)', code)
    return match.group(1) if match else None

async def generate_manim_code(prompt: str) -> str:
    """Generate Manim code via Groq API (async)."""
    groq_api_key = settings.GROQ_API_KEY
    if not groq_api_key:
        logger.error("Groq API key not configured")
        return FALLBACK_SCENE_TEMPLATE

    system_message = """
    You are a Manim expert. Generate OPTIMIZED, SHORT (5-10s) animations.
    Follow rules: Fixed steps, no infinite loops, efficient self.play().
    Ensure code is syntactically correct and runnable.
    """

    user_message = f"""Create a Manim animation for: {prompt}
    Keep it short, efficient, and visually appealing.
    IMPORTANT: Avoid infinite loops, use rate_functions, and limit animations to 5-10 seconds.
    """

    headers = {"Authorization": f"Bearer {groq_api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.post("https://api.groq.com/openai/v1/chat/completions",
                                         json=payload, headers=headers)
            response.raise_for_status()
            raw = response.json()["choices"][0]["message"]["content"]
            code = extract_code_from_response(raw)
            code = clean_code(code)

            if "class" not in code or "Scene" not in code:
                logger.warning("Groq returned invalid code; using default template")
                return DEFAULT_SCENE_TEMPLATE

            code = fix_potential_loops(code)
            code = validate_parentheses(code)

            return code
        except httpx.HTTPError as e:
            logger.error(f"Groq API error: {e}")
            return FALLBACK_SCENE_TEMPLATE

def extract_code_from_response(raw: str) -> str:
    """Extract code block from Groq response."""
    match = re.search(r'```python\n(.*?)```', raw, re.DOTALL)
    return match.group(1).strip() if match else raw

def clean_code(code: str) -> str:
    """Remove markdown artifacts and comments."""
    code = code.strip('`').replace('```python', '').replace('```', '')
    code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)  # Remove comments
    return code

def fix_potential_loops(code: str) -> str:
    """Replace infinite loops with fixed iterations."""
    code = re.sub(r'while\s+True', 'for _ in range(5)', code)
    code = re.sub(r'while\s+1\b', 'for _ in range(5)', code)
    return code

def validate_parentheses(code: str) -> str:
    """Basic check for balanced parentheses in self.play() calls."""
    stack = []
    for i, char in enumerate(code):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if not stack:
                logger.warning("Unbalanced parentheses detected; fixing...")
                code = code[:i] + code[i+1:]  # Remove extra ')'
            else:
                stack.pop()
    # If any '(' remains unclosed, append matching ')'
    while stack:
        logger.warning("Unbalanced parentheses detected; fixing...")
        code += ')'
        stack.pop()
    return code

if __name__ == "__main__":
    # Test the Groq API integration
    async def test_groq():
        prompt = "A red ball bouncing 3 times"
        code = await generate_manim_code(prompt)
        print(code)

    asyncio.run(test_groq())