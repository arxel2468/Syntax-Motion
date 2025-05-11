from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime
from app.models.scene import SceneStatus

class SceneBase(BaseModel):
    prompt: str
    order: int = 0

class SceneCreate(SceneBase):
    pass

class SceneUpdate(BaseModel):
    prompt: Optional[str] = None
    order: Optional[int] = None
    status: Optional[SceneStatus] = None

class SceneResponse(SceneBase):
    id: UUID4
    project_id: UUID4
    status: SceneStatus
    video_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class SceneDetail(SceneResponse):
    code: Optional[str] = None 