from typing import List, Optional
from sqlalchemy.orm import Session

from ..models.project import Project
from ..repositories.project_repository import ProjectRepository
from ..repositories.task_repository import TaskRepository
from ..exceptions.service_exceptions import ValidationError
from ..utils.config import Config


class ProjectService:
    """
    Service layer for project management operations
    Now uses Repository Pattern with dependency injection
    """
    
    def __init__(self, project_repo: ProjectRepository, task_repo: TaskRepository):
        self.project_repo = project_repo
        self.task_repo = task_repo
    
    def create_project(self, name: str, description: str) -> Project:
        """
        Create a new project with validation
        """
        # Check maximum projects limit
        if self.project_repo.count() >= Config.MAX_NUMBER_OF_PROJECTS:
            raise ValidationError(f"Cannot create more than {Config.MAX_NUMBER_OF_PROJECTS} projects")
        
        project = Project(name=name, description=description)
        return self.project_repo.add(project)
    
    def get_project(self, project_id: int) -> Optional[Project]:
        """Get project by ID"""
        return self.project_repo.get(project_id)
    
    def get_all_projects(self) -> List[Project]:
        """Get all projects"""
        return self.project_repo.get_all()
    
    def update_project(self, project_id: int, name: str, description: str) -> Project:
        """
        Update project information
        """
        project = self.project_repo.get(project_id)
        if not project:
            raise ValidationError("Project not found")
        
        project.update(name, description)
        return self.project_repo.update(project)
    
    def delete_project(self, project_id: int) -> bool:
        """
        Delete project (cascade delete handled by SQLAlchemy)
        """
        return self.project_repo.delete(project_id)
    
    def project_exists(self, project_id: int) -> bool:
        """Check if project exists"""
        return self.project_repo.get(project_id) is not None
    
    def get_project_stats(self, project_id: int) -> dict:
        """Get statistics for a project"""
        project = self.get_project(project_id)
        if not project:
            raise ValidationError("Project not found")
        
        tasks = self.task_repo.get_by_project_id(project_id)
        status_count = {}
        for status in Config.VALID_TASK_STATUSES:
            status_count[status] = len([task for task in tasks if task.status == status])
        
        return {
            "total_tasks": len(tasks),
            "status_count": status_count,
            "project": project
        }