import os
from fastapi import FastAPI, APIRouter
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
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount media directory for serving static files
app.mount("/media", StaticFiles(directory=settings.MEDIA_ROOT), name="media")

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the AI-Powered Animated Video Generator API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 