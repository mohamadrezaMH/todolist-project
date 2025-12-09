from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ..db.base import Base
from ..utils.validators import validate_text_length, validate_status, validate_deadline
from ..utils.config import Config


class Task(Base):
    """
    SQLAlchemy ORM model for Task entity
    Maps to 'tasks' table in database
    """
    
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(Config.MAX_TASK_TITLE_LENGTH), nullable=False)
    description = Column(String(Config.MAX_TASK_DESCRIPTION_LENGTH), nullable=False)
    status = Column(String(20), default="todo", nullable=False)
    deadline = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # Foreign key to Project
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    
    # Many-to-one relationship with Project
    project = relationship("Project", back_populates="tasks")
    
    def __init__(self, title: str, description: str, deadline: Optional[datetime] = None):
        self._validate_inputs(title, description, deadline)
        self.title = title
        self.description = description
        self.status = "todo"  # default status
        self.deadline = deadline
    
    def _validate_inputs(self, title: str, description: str, deadline: Optional[datetime]):
        """Validate task inputs"""
        validate_text_length(title, "Task title", 1, Config.MAX_TASK_TITLE_LENGTH)
        validate_text_length(description, "Task description", 1, Config.MAX_TASK_DESCRIPTION_LENGTH)
        validate_deadline(deadline)
    
    def change_status(self, status: str):
        """Change task status"""
        validate_status(status)
        self.status = status
        self.updated_at = datetime.now()
    
    def update(self, title: str, description: str, status: str, deadline: Optional[datetime] = None):
        """Update task information"""
        self._validate_inputs(title, description, deadline)
        validate_status(status)
        
        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline
        self.updated_at = datetime.now()
    
    def __str__(self):
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"
    
    def __repr__(self):
        return self.__str__()