from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime

class ProjectBase(BaseModel):
    title: str

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: UUID4
    user_id: UUID4
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProjectDetail(ProjectResponse):
    from app.schemas.scene import SceneResponse
    scenes: List[SceneResponse] = [] 