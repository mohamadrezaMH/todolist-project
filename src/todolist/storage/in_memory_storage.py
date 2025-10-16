from typing import Dict, List, Optional, TypeVar, Generic
from ..models.project import Project
from ..models.task import Task

T = TypeVar("T")


class InMemoryStorage(Generic[T]):
    """
    Generic in-memory storage for any type of object
    Provides basic CRUD operations
    """

    def __init__(self):
        self._data: Dict[int, T] = {}
        self._next_id = 1

    def get_next_id(self) -> int:
        """Generate next available ID"""
        id_ = self._next_id
        self._next_id += 1
        return id_

    def add(self, item: T) -> int:
        """Add item to storage and return assigned ID"""
        item.id = self.get_next_id()
        self._data[item.id] = item
        return item.id

    def get(self, id_: int) -> Optional[T]:
        """Get item by ID"""
        return self._data.get(id_)

    def get_all(self) -> List[T]:
        """Get all items"""
        return list(self._data.values())

    def update(self, item: T) -> bool:
        """Update existing item"""
        if item.id in self._data:
            self._data[item.id] = item
            return True
        return False

    def delete(self, id_: int) -> bool:
        """Delete item by ID"""
        if id_ in self._data:
            del self._data[id_]
            return True
        return False

    def count(self) -> int:
        """Get total number of items"""
        return len(self._data)


class ProjectStorage(InMemoryStorage[Project]):
    """Specialized storage for Project objects"""

    def get_by_name(self, name: str) -> Optional[Project]:
        """Get project by name"""
        for project in self._data.values():
            if project.name == name:
                return project
        return None

    def get_all_names(self) -> List[str]:
        """Get all project names"""
        return [project.name for project in self._data.values()]


class TaskStorage(InMemoryStorage[Task]):
    """Specialized storage for Task objects"""

    def get_by_project_id(self, project_id: int) -> List[Task]:
        """Get all tasks for a specific project"""
        return [task for task in self._data.values() if task.project_id == project_id]

    def delete_by_project_id(self, project_id: int) -> int:
        """Delete all tasks for a specific project (cascade delete)"""
        tasks_to_delete = [
            task_id
            for task_id, task in self._data.items()
            if task.project_id == project_id
        ]
        for task_id in tasks_to_delete:
            del self._data[task_id]
        return len(tasks_to_delete)
