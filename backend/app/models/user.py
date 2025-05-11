from sqlalchemy import Column, String, TIMESTAMP, UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan") 