from sqlalchemy import Column, String, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.db.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="projects")
    scenes = relationship("Scene", back_populates="project", cascade="all, delete-orphan") 