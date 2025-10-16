from datetime import datetime
from typing import Optional


class Task:
    """Task model for managing tasks within projects"""
    
    def __init__(self, title: str, description: str, deadline: Optional[datetime] = None):
        self.id: Optional[int] = None
        self.project_id: Optional[int] = None
        self.title = title
        self.description = description
        self.status = "todo"  # Default value
        self.deadline = deadline
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def change_status(self, status: str):
        """Change task status"""
        self.status = status
        self.updated_at = datetime.now()
    
    def update(self, title: str, description: str, status: str, deadline: Optional[datetime] = None):
        """Update complete task information"""
        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline
        self.updated_at = datetime.now()
    
    def __str__(self):
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"
    
    def __repr__(self):
        return self.__str__()