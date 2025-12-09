from typing import List, Optional
from sqlalchemy.orm import Session

from .base import BaseRepository
from ..models.project import Project
from ..exceptions.repository_exceptions import NotFoundError, DuplicateError


class ProjectRepository(BaseRepository[Project]):
    """Repository for Project entities using SQLAlchemy"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def add(self, project: Project) -> Project:
        """Add a new project to database"""
        # Check for duplicate name
        if self.get_by_name(project.name):
            raise DuplicateError("Project", "name", project.name)
        
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def get(self, id: int) -> Optional[Project]:
        """Get project by ID"""
        return self.db.query(Project).filter(Project.id == id).first()
    
    def get_by_name(self, name: str) -> Optional[Project]:
        """Get project by name"""
        return self.db.query(Project).filter(Project.name == name).first()
    
    def get_all(self) -> List[Project]:
        """Get all projects"""
        return self.db.query(Project).all()
    
    def update(self, project: Project) -> Project:
        """Update project in database"""
        # Check if project exists
        existing = self.get(project.id)
        if not existing:
            raise NotFoundError("Project", project.id)
        
        # Check for duplicate name (excluding current project)
        duplicate = self.get_by_name(project.name)
        if duplicate and duplicate.id != project.id:
            raise DuplicateError("Project", "name", project.name)
        
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def delete(self, id: int) -> bool:
        """Delete project by ID"""
        project = self.get(id)
        if not project:
            return False
        
        self.db.delete(project)
        self.db.commit()
        return True
    
    def count(self) -> int:
        """Get total number of projects"""
        return self.db.query(Project).count()