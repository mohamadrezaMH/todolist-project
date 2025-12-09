from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

from ...utils.config import Config


class ProjectBase(BaseModel):
    """Base schema for project data"""
    name: str = Field(..., min_length=1, max_length=Config.MAX_PROJECT_NAME_LENGTH)
    description: str = Field(..., min_length=1, max_length=Config.MAX_PROJECT_DESCRIPTION_LENGTH)


class ProjectCreate(ProjectBase):
    """Schema for creating a new project"""
    pass


class ProjectUpdate(ProjectBase):
    """Schema for updating a project"""
    name: Optional[str] = Field(None, min_length=1, max_length=Config.MAX_PROJECT_NAME_LENGTH)
    description: Optional[str] = Field(None, min_length=1, max_length=Config.MAX_PROJECT_DESCRIPTION_LENGTH)


class ProjectResponse(ProjectBase):
    """Schema for project response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ProjectStats(BaseModel):
    """Schema for project statistics"""
    project: ProjectResponse
    total_tasks: int
    status_count: dict[str, int]
    
    model_config = ConfigDict(from_attributes=True)