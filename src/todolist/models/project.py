from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from ..db.base import Base
from ..utils.config import Config


class Project(Base):
    """
    SQLAlchemy ORM model for Project entity
    Maps to 'projects' table in database
    """
    
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(Config.MAX_PROJECT_NAME_LENGTH), unique=True, nullable=False)
    description = Column(String, nullable=False)  # حذف محدودیت طول برای SQLite
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # One-to-many relationship with Task
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def update(self, name: str, description: str):
        """Update project information"""
        self.name = name
        self.description = description
        self.updated_at = datetime.now()
    
    def __str__(self):
        return f"Project(id={self.id}, name='{self.name}')"
    
    def __repr__(self):
        return self.__str__()