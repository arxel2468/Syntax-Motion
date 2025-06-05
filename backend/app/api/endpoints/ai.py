from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from app.core.config import settings
import httpx

router = APIRouter()

class RefinePromptRequest(BaseModel):
    project_title: str
    prompt: str = ""

class RefinePromptResponse(BaseModel):
    refined_prompt: str

class GenerateCodeRequest(BaseModel):
    prompt: str

class GenerateCodeResponse(BaseModel):
    code: str

@router.post("/refine-prompt", response_model=RefinePromptResponse)
def refine_prompt(data: RefinePromptRequest):
    """Refine a scene prompt or generate one from the project title using Groq AI."""
    groq_api_key = settings.GROQ_API_KEY
    if not groq_api_key:
        raise HTTPException(status_code=500, detail="GROQ API key not configured.")

    if data.prompt.strip():
        user_message = f"Refine this animation prompt for Manim so it is clear, concise, and compatible with Manim: {data.prompt}"
    else:
        user_message = f"Generate a creative and compatible Manim animation prompt for a project titled: '{data.project_title}'. The prompt should be clear and suitable for AI code generation."

    system_message = """You are an expert at writing prompts for Manim code generation. Follow these rules:
    1. Be extremely specific about dimensions, colors, and timing
    2. Include exact numerical values for positions, sizes, and durations
    3. Specify the exact number of objects and their properties
    4. Avoid vague descriptions like 'slightly' or 'about'
    5. Format the response as a single paragraph without any introductory text
    6. Do not include any explanations or commentary"""

    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_api_key}", "Content-Type": "application/json"}
    data_json = {
        "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }
    try:
        response = httpx.post(api_url, json=data_json, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        refined_prompt = result["choices"][0]["message"]["content"].strip()
        return {"refined_prompt": refined_prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI refinement failed: {e}")

@router.post("/generate-code", response_model=GenerateCodeResponse)
def generate_code(data: GenerateCodeRequest):
    """Generate Manim code from a prompt using Groq AI."""
    groq_api_key = settings.GROQ_API_KEY
    if not groq_api_key:
        raise HTTPException(status_code=500, detail="GROQ API key not configured.")

    system_message = """You are an expert Manim developer. Follow these rules strictly:
1. ALWAYS start with these exact imports in this order:
   from manim import *
   import numpy as np
   import time
2. Define a class that inherits from Scene
3. Use proper Manim color constants (BLUE, RED, GREEN, etc.) or RGB values
4. Use precise numerical values for all parameters
5. Format code with proper indentation (4 spaces)
6. DO NOT include any explanations, comments, or text outside the code
7. DO NOT include markdown formatting or code blocks
8. The response should be valid Python code that can be executed directly
9. Use proper Manim animation methods (Create, FadeIn, MoveTo, etc.)
10. Always include proper timing in animations
11. Use proper coordinate system (UP, DOWN, LEFT, RIGHT, ORIGIN)
12. Include proper scene setup and cleanup
13. For timing, use time.time() NOT np.time.time()
14. Keep the code simple and focused on the animation
15. Use proper indentation (4 spaces) consistently throughout the code
16. ALWAYS close all parentheses, brackets, and braces
17. Keep each line under 100 characters
18. Use proper Python syntax for all statements
19. Ensure all object creations are properly formatted with all parameters
20. Double-check all syntax before returning the code"""

    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_api_key}", "Content-Type": "application/json"}
    data_json = {
        "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Generate Manim code for this animation: {data.prompt}"}
        ],
        "max_tokens": 3000,
        "temperature": 0.2
    }
    try:
        response = httpx.post(api_url, json=data_json, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        code = result["choices"][0]["message"]["content"].strip()
        
        # Basic validation to ensure it's valid Python code with proper imports
        if not code.startswith("from manim import *"):
            raise HTTPException(status_code=500, detail="Generated code must start with proper Manim imports")
            
        # Ensure the code has a Scene class
        if "class" not in code or "Scene" not in code:
            raise HTTPException(status_code=500, detail="Generated code must include a Scene class")
            
        # Ensure proper time import
        if "import time" not in code:
            raise HTTPException(status_code=500, detail="Generated code must include time import")
            
        # Check for common errors
        if "np.time" in code:
            code = code.replace("np.time", "time")
            
        # Validate parentheses
        if code.count("(") != code.count(")"):
            raise HTTPException(status_code=500, detail="Generated code has mismatched parentheses")
            
        # Validate brackets
        if code.count("[") != code.count("]"):
            raise HTTPException(status_code=500, detail="Generated code has mismatched brackets")
            
        # Validate braces
        if code.count("{") != code.count("}"):
            raise HTTPException(status_code=500, detail="Generated code has mismatched braces")
            
        return {"code": code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI code generation failed: {e}") 