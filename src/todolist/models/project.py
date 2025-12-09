from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from ..db.base import Base
from ..utils.validators import validate_text_length
from ..utils.config import Config


class Project(Base):
    """
    SQLAlchemy ORM model for Project entity
    Maps to 'projects' table in database
    """
    
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(Config.MAX_PROJECT_NAME_LENGTH), unique=True, nullable=False)
    description = Column(String(Config.MAX_PROJECT_DESCRIPTION_LENGTH), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # One-to-many relationship with Task
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    
    def __init__(self, name: str, description: str):
        self._validate_inputs(name, description)
        self.name = name
        self.description = description
    
    def _validate_inputs(self, name: str, description: str):
        """Validate project inputs"""
        validate_text_length(name, "Project name", 1, Config.MAX_PROJECT_NAME_LENGTH)
        validate_text_length(description, "Project description", 1, Config.MAX_PROJECT_DESCRIPTION_LENGTH)
    
    def update(self, name: str, description: str):
        """Update project information"""
        self._validate_inputs(name, description)
        self.name = name
        self.description = description
        self.updated_at = datetime.now()
    
    def __str__(self):
        return f"Project(id={self.id}, name='{self.name}', tasks_count={len(self.tasks) if self.tasks else 0})"
    
    def __repr__(self):
        return self.__str__()