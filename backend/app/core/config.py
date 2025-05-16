import os
from dotenv import load_dotenv
from pydantic import BaseModel
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

class Settings(BaseModel):
    # Application settings
    PROJECT_NAME: str = "Syntax Motion"
    API_V1_STR: str = "/api/v1"
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # Groq API settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    
    # Redis settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    
    # Celery settings
    CELERY_BROKER_URL: str = REDIS_URL
    CELERY_RESULT_BACKEND: str = REDIS_URL
    
    # Storage settings
    MEDIA_ROOT: str = os.getenv("MEDIA_ROOT", os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "media"))
    VIDEO_DIR: str = os.path.join(MEDIA_ROOT, "videos")
    AUDIO_DIR: str = f"{MEDIA_ROOT}/audio"
    
    # Animation settings
    ANIMATION_TIMEOUT: int = 60 * 5  # 5 minutes

    def __init__(self):
        # Ensure media directories exist
        super().__init__()
        os.makedirs(self.MEDIA_ROOT, exist_ok=True)
        os.makedirs(self.VIDEO_DIR, exist_ok=True)

settings = Settings() 