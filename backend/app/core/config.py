import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

class Settings(BaseModel):
    # Application settings
    PROJECT_NAME: str = "AI-Powered Animated Video Generator"
    API_V1_STR: str = "/api/v1"
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret_key_for_development")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@db:5432/animatedvideo"
    )
    
    # OpenAI API settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Redis settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    
    # Celery settings
    CELERY_BROKER_URL: str = REDIS_URL
    CELERY_RESULT_BACKEND: str = REDIS_URL
    
    # Storage settings
    MEDIA_ROOT: str = os.getenv("MEDIA_ROOT", "/app/media")
    VIDEO_DIR: str = f"{MEDIA_ROOT}/videos"
    AUDIO_DIR: str = f"{MEDIA_ROOT}/audio"
    
    # Animation settings
    ANIMATION_TIMEOUT: int = 60 * 5  # 5 minutes

settings = Settings() 