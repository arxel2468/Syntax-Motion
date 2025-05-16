from pydantic import BaseModel, UUID4, Field
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
    
    model_config = {
        "from_attributes": True
    }

# Simple Scene class for ProjectDetail to avoid circular imports
class SimpleSceneInfo(BaseModel):
    id: UUID4
    project_id: UUID4
    prompt: str
    order: int = 0
    status: str
    video_url: Optional[str] = None
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }

class ProjectDetail(ProjectResponse):
    scenes: List[SimpleSceneInfo] = Field(default_factory=list) 