from sqlalchemy import Column, String, TIMESTAMP, UUID, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.db.database import Base

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    scene_id = Column(UUID(as_uuid=True), ForeignKey("scenes.id", ondelete="CASCADE"))
    file_path = Column(String)
    duration = Column(Float, default=0.0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    scene = relationship("Scene", back_populates="video") 