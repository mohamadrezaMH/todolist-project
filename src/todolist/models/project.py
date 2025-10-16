from datetime import datetime
from typing import List, Optional


class Project:
    """Project model for todo list project management"""
    
    def __init__(self, name: str, description: str):
        self.id: Optional[int] = None
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.tasks: List['Task'] = []
    
    def update(self, name: str, description: str):
        """Update project information"""
        self.name = name
        self.description = description
        self.updated_at = datetime.now()
    
    def __str__(self):
        return f"Project(id={self.id}, name='{self.name}', tasks_count={len(self.tasks)})"
    
    def __repr__(self):
        return self.__str__()