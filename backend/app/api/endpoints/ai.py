from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from app.core.config import settings
import httpx
import re

router = APIRouter()

class RefinePromptRequest(BaseModel):
    project_title: str
    prompt: str = ""

class RefinePromptResponse(BaseModel):
    refined_prompt: str

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

    system_message = "You are an expert at writing prompts for Manim code generation. Your job is to create or refine prompts so they are clear, concise, and compatible with Manim Community Edition. IMPORTANT: Put the prompt in double quotes and make it the first part of your response. Do not include explanations before the prompt."

    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {groq_api_key}", "Content-Type": "application/json"}
    data_json = {
        "model": "llama3-70b-8192",
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
        raw = result["choices"][0]["message"]["content"].strip()
        
        # Extract prompt from double quotes if present
        quote_match = re.search(r'"([^"]*)"', raw)
        if quote_match:
            refined_prompt = quote_match.group(1)
        else:
            # If no quotes, take the first paragraph before any explanation
            refined_prompt = raw.split('\n\n')[0].strip('"` ')
            # Remove any markdown markers
            refined_prompt = re.sub(r'^[#*`]+\s*', '', refined_prompt)
            
        return {"refined_prompt": refined_prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI refinement failed: {e}")