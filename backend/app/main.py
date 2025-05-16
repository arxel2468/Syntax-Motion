import os
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.api import api_router
from app.core.config import settings
from app.db.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Create directories for media files
os.makedirs(settings.VIDEO_DIR, exist_ok=True)
os.makedirs(settings.AUDIO_DIR, exist_ok=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount media directory for serving static files
try:
    # Ensure the directory exists before mounting
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    app.mount("/media", StaticFiles(directory=settings.MEDIA_ROOT), name="media")
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the AI-Powered Animated Video Generator API"}

@app.on_event("startup")
async def startup_event():
    """Create needed directories and perform other startup tasks"""
    import os
    from app.core.config import settings
    
    # Create media directories
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    os.makedirs(settings.VIDEO_DIR, exist_ok=True)
    if hasattr(settings, 'AUDIO_DIR'):
        os.makedirs(settings.AUDIO_DIR, exist_ok=True)
    
    print(f"Media directories setup complete. Videos will be stored in: {settings.VIDEO_DIR}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 