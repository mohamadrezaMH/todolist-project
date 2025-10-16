from typing import List, Optional
from ..models.project import Project
from ..storage.in_memory_storage import ProjectStorage, TaskStorage
from ..utils.validators import ValidationError, validate_unique_name
from ..utils.config import Config


class ProjectService:
    """
    Service layer for project management operations
    Handles business logic and validation
    """

    def __init__(self, project_storage: ProjectStorage, task_storage: TaskStorage):
        self.project_storage = project_storage
        self.task_storage = task_storage

    def create_project(self, name: str, description: str) -> Project:
        """
        Create a new project with validation
        """
        # Check maximum projects limit
        if self.project_storage.count() >= Config.MAX_NUMBER_OF_PROJECTS:
            raise ValidationError(
                f"Cannot create more than {Config.MAX_NUMBER_OF_PROJECTS} " f"projects"
            )

        # Check unique name
        existing_names = self.project_storage.get_all_names()
        validate_unique_name(existing_names, name, "project")

        project = Project(name, description)
        project_id = self.project_storage.add(project)
        project.id = project_id
        return project

    def get_project(self, project_id: int) -> Optional[Project]:
        """Get project by ID"""
        return self.project_storage.get(project_id)

    def get_all_projects(self) -> List[Project]:
        """Get all projects"""
        return self.project_storage.get_all()

    def update_project(self, project_id: int, name: str, description: str) -> Project:
        """
        Update project information
        """
        project = self.project_storage.get(project_id)
        if not project:
            raise ValidationError("Project not found")

        # Check unique name (excluding current project)
        existing_names = [
            proj.name
            for proj in self.project_storage.get_all()
            if proj.id != project_id
        ]
        validate_unique_name(existing_names, name, "project")

        project.update(name, description)
        self.project_storage.update(project)
        return project

    def delete_project(self, project_id: int) -> bool:
        """
        Delete project and all its tasks (cascade delete)
        """
        project = self.project_storage.get(project_id)
        if not project:
            return False

        # Cascade delete tasks
        self.task_storage.delete_by_project_id(project_id)

        # Delete project
        success = self.project_storage.delete(project_id)

        return success

    def project_exists(self, project_id: int) -> bool:
        """Check if project exists"""
        return self.project_storage.get(project_id) is not None

    def get_project_stats(self, project_id: int) -> dict:
        """Get statistics for a project"""
        project = self.get_project(project_id)
        if not project:
            raise ValidationError("Project not found")

        tasks = self.task_storage.get_by_project_id(project_id)
        status_count = {}
        for status in Config.VALID_TASK_STATUSES:
            status_count[status] = len(
                [task for task in tasks if task.status == status]
            )

        return {
            "total_tasks": len(tasks),
            "status_count": status_count,
            "project": project,
        }
