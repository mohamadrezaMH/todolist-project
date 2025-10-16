from datetime import datetime
from typing import List, Optional
from ..models.task import Task
from ..storage.in_memory_storage import TaskStorage
from ..utils.validators import ValidationError
from ..utils.config import Config


class TaskService:
    """
    Service layer for task management operations
    Handles business logic and validation
    """
    
    def __init__(self, task_storage: TaskStorage, project_service: 'ProjectService'):
        self.task_storage = task_storage
        self.project_service = project_service
    
    def create_task(self, project_id: int, title: str, description: str, 
                   deadline: Optional[datetime] = None) -> Task:
        """
        Create a new task in specified project
        """
        # Check if project exists
        if not self.project_service.project_exists(project_id):
            raise ValidationError("Project not found")
        
        # Check maximum tasks limit for project
        project_tasks = self.task_storage.get_by_project_id(project_id)
        if len(project_tasks) >= Config.MAX_NUMBER_OF_TASKS:
            raise ValidationError(f"Cannot create more than {Config.MAX_NUMBER_OF_TASKS} tasks in a project")
        
        task = Task(title, description, deadline)
        task.project_id = project_id
        task_id = self.task_storage.add(task)
        task.id = task_id
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        return self.task_storage.get(task_id)
    
    def get_tasks_by_project(self, project_id: int) -> List[Task]:
        """Get all tasks for a project"""
        if not self.project_service.project_exists(project_id):
            raise ValidationError("Project not found")
        return self.task_storage.get_by_project_id(project_id)
    
    def get_tasks_by_status(self, project_id: int, status: str) -> List[Task]:
        """Get tasks by status in a project"""
        validate_status(status)
        tasks = self.get_tasks_by_project(project_id)
        return [task for task in tasks if task.status == status]
    
    def update_task(self, task_id: int, title: str, description: str, 
                   status: str, deadline: Optional[datetime] = None) -> Task:
        """
        Update task information
        """
        task = self.task_storage.get(task_id)
        if not task:
            raise ValidationError("Task not found")
        
        task.update(title, description, status, deadline)
        self.task_storage.update(task)
        return task
    
    def change_task_status(self, task_id: int, status: str) -> Task:
        """
        Change task status only
        """
        task = self.task_storage.get(task_id)
        if not task:
            raise ValidationError("Task not found")
        
        task.change_status(status)
        self.task_storage.update(task)
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID"""
        return self.task_storage.delete(task_id)
    
    def get_overdue_tasks(self, project_id: int) -> List[Task]:
        """Get overdue tasks for a project"""
        tasks = self.get_tasks_by_project(project_id)
        now = datetime.now()
        return [task for task in tasks if task.deadline and task.deadline < now]