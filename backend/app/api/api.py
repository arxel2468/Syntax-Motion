from fastapi import APIRouter
from app.api.endpoints import auth, projects, scenes

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(scenes.router, prefix="/projects", tags=["Scenes"]) 