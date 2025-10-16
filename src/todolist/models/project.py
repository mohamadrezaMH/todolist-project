from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .task import Task
from ..utils.validators import validate_text_length
from ..utils.config import Config


class Project:
    """Project model for todo list project management"""

    def __init__(self, name: str, description: str):
        self._validate_inputs(name, description)

        self.id: Optional[int] = None
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.tasks: List["Task"] = []

    def _validate_inputs(self, name: str, description: str):
        """Project input validation"""
        validate_text_length(name, "نام پروژه", 1, Config.MAX_PROJECT_NAME_LENGTH)
        validate_text_length(
            description, "توضیحات پروژه", 1, Config.MAX_PROJECT_DESCRIPTION_LENGTH
        )

    def update(self, name: str, description: str):
        """Update project information"""
        self._validate_inputs(name, description)
        self.name = name
        self.description = description
        self.updated_at = datetime.now()

    def __str__(self):
        return (
            f"Project(id={self.id}, name='{self.name}', "
            f"tasks_count={len(self.tasks)})"
        )

    def __repr__(self):
        return self.__str__()
