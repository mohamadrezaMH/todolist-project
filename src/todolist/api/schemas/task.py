from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from ...utils.config import Config


class TaskBase(BaseModel):
    """Base schema for task data"""
    title: str = Field(..., min_length=1, max_length=Config.MAX_TASK_TITLE_LENGTH)
    description: str = Field(..., min_length=1, max_length=Config.MAX_TASK_DESCRIPTION_LENGTH)
    status: str = Field(default="todo", pattern="^(todo|doing|done)$")
    deadline: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    project_id: int
    deadline: Optional[datetime] = None


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=Config.MAX_TASK_TITLE_LENGTH)
    description: Optional[str] = Field(None, min_length=1, max_length=Config.MAX_TASK_DESCRIPTION_LENGTH)
    status: Optional[str] = Field(None, pattern="^(todo|doing|done)$")
    deadline: Optional[datetime] = None


class TaskStatusUpdate(BaseModel):
    """Schema for updating only task status"""
    status: str = Field(..., pattern="^(todo|doing|done)$")


class TaskResponse(TaskBase):
    """Schema for task response"""
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)