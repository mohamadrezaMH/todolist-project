from datetime import datetime
from typing import Optional
from ..utils.validators import validate_text_length, validate_status, validate_deadline
from ..utils.config import Config


class Task:
    """Task model for managing tasks within projects"""

    def __init__(
        self, title: str, description: str, deadline: Optional[datetime] = None
    ):
        self._validate_inputs(title, description, deadline)

        self.id: Optional[int] = None
        self.project_id: Optional[int] = None
        self.title = title
        self.description = description
        self.status = "todo"  # Default value
        self.deadline = deadline
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def _validate_inputs(
        self, title: str, description: str, deadline: Optional[datetime]
    ):
        """Task input validation"""
        validate_text_length(title, "Task title", 1, Config.MAX_TASK_TITLE_LENGTH)
        validate_text_length(
            description, "Task description", 1, Config.MAX_TASK_DESCRIPTION_LENGTH
        )
        validate_deadline(deadline)

    def change_status(self, status: str):
        """Change task status"""
        validate_status(status)
        self.status = status
        self.updated_at = datetime.now()

    def update(
        self,
        title: str,
        description: str,
        status: str,
        deadline: Optional[datetime] = None,
    ):
        """Update complete task information"""
        self._validate_inputs(title, description, deadline)
        validate_status(status)

        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline
        self.updated_at = datetime.now()

    def __str__(self):
        return f"Task(id={self.id}, title='{self.title}', " f"status='{self.status}')"

    def __repr__(self):
        return self.__str__()
