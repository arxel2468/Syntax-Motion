from sqlalchemy import Column, String, Text, TIMESTAMP, UUID, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.db.database import Base

class SceneStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Scene(Base):
    __tablename__ = "scenes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"))
    prompt = Column(Text)
    code = Column(Text, nullable=True)
    video_url = Column(String, nullable=True)
    order = Column(Integer, default=0)
    status = Column(Enum(SceneStatus), default=SceneStatus.PENDING)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="scenes")
    video = relationship("Video", back_populates="scene", uselist=False, cascade="all, delete-orphan")
    voice_over = relationship("VoiceOver", back_populates="scene", uselist=False, cascade="all, delete-orphan") 