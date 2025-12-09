from typing import List, Optional
from sqlalchemy.orm import Session

from .base import BaseRepository
from ..models.task import Task
from ..exceptions.repository_exceptions import NotFoundError


class TaskRepository(BaseRepository[Task]):
    """Repository for Task entities using SQLAlchemy"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def add(self, task: Task) -> Task:
        """Add a new task to database"""
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get(self, id: int) -> Optional[Task]:
        """Get task by ID"""
        return self.db.query(Task).filter(Task.id == id).first()
    
    def get_by_project_id(self, project_id: int) -> List[Task]:
        """Get all tasks for a specific project"""
        return self.db.query(Task).filter(Task.project_id == project_id).all()
    
    def get_by_status(self, project_id: int, status: str) -> List[Task]:
        """Get tasks by status for a project"""
        return self.db.query(Task).filter(
            Task.project_id == project_id,
            Task.status == status
        ).all()
    
    def get_overdue_tasks(self, project_id: Optional[int] = None) -> List[Task]:
        """Get overdue tasks (deadline passed and status not 'done')"""
        from datetime import datetime
        query = self.db.query(Task).filter(
            Task.deadline < datetime.now(),
            Task.status != 'done'
        )
        
        if project_id:
            query = query.filter(Task.project_id == project_id)
        
        return query.all()
    
    def get_all(self) -> List[Task]:
        """Get all tasks"""
        return self.db.query(Task).all()
    
    def update(self, task: Task) -> Task:
        """Update task in database"""
        existing = self.get(task.id)
        if not existing:
            raise NotFoundError("Task", task.id)
        
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def delete(self, id: int) -> bool:
        """Delete task by ID"""
        task = self.get(id)
        if not task:
            return False
        
        self.db.delete(task)
        self.db.commit()
        return True
    
    def count(self) -> int:
        """Get total number of tasks"""
        return self.db.query(Task).count()
    
    def count_by_project(self, project_id: int) -> int:
        """Count tasks for a specific project"""
        return self.db.query(Task).filter(Task.project_id == project_id).count()