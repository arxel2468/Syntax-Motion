from sqlalchemy import Column, String, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.db.database import Base

class VoiceOver(Base):
    __tablename__ = "voice_overs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    scene_id = Column(UUID(as_uuid=True), ForeignKey("scenes.id", ondelete="CASCADE"))
    file_path = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    scene = relationship("Scene", back_populates="voice_over") 