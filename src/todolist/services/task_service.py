from datetime import datetime
from typing import List, Optional

from ..models.task import Task
from ..repositories.task_repository import TaskRepository
from ..exceptions.service_exceptions import ValidationError
from ..utils.config import Config


class TaskService:
    """
    Service layer for task management operations
    Now uses Repository Pattern with dependency injection
    """
    
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo
    
    def create_task(self, project_id: int, title: str, description: str, 
                   deadline: Optional[datetime] = None) -> Task:
        """
        Create a new task in specified project
        """
        # Note: Project existence check should be done by caller (service composition)
        
        # Check maximum tasks limit for project
        project_tasks_count = self.task_repo.count_by_project(project_id)
        if project_tasks_count >= Config.MAX_NUMBER_OF_TASKS:
            raise ValidationError(f"Cannot create more than {Config.MAX_NUMBER_OF_TASKS} tasks in a project")
        
        task = Task(title=title, description=description, deadline=deadline)
        task.project_id = project_id
        return self.task_repo.add(task)
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        return self.task_repo.get(task_id)
    
    def get_tasks_by_project(self, project_id: int) -> List[Task]:
        """Get all tasks for a project"""
        return self.task_repo.get_by_project_id(project_id)
    
    def update_task(self, task_id: int, title: str, description: str, 
                   status: str, deadline: Optional[datetime] = None) -> Task:
        """
        Update task information
        """
        task = self.task_repo.get(task_id)
        if not task:
            raise ValidationError("Task not found")
        
        task.update(title, description, status, deadline)
        return self.task_repo.update(task)
    
    def change_task_status(self, task_id: int, status: str) -> Task:
        """
        Change task status only
        """
        task = self.task_repo.get(task_id)
        if not task:
            raise ValidationError("Task not found")
        
        task.change_status(status)
        return self.task_repo.update(task)
    
    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID"""
        return self.task_repo.delete(task_id)
    
    def get_overdue_tasks(self, project_id: Optional[int] = None) -> List[Task]:
        """Get overdue tasks for a project or all projects"""
        return self.task_repo.get_overdue_tasks(project_id)