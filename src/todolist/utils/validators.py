from datetime import datetime
from typing import Optional
from .config import Config


class ValidationError(Exception):
    """Custom validation error"""

    pass


def validate_text_length(text: str, field_name: str, min_length: int, max_length: int):
    """Validate text length"""
    if not text or len(text.strip()) == 0:
        raise ValidationError(f"{field_name} cannot be empty")
    
    if len(text) > max_length:
        raise ValidationError(f"{field_name} cannot exceed {max_length} characters")
    
    if len(text) < min_length:
        raise ValidationError(f"{field_name} must be at least {min_length} characters")


def validate_status(status: str):
    """Validate task status"""
    if status not in Config.VALID_TASK_STATUSES:
        valid_statuses = ", ".join(Config.VALID_TASK_STATUSES)
        raise ValidationError(f"Status must be one of: {valid_statuses}")


def validate_deadline(deadline: Optional[datetime]):
    """Validate deadline date"""
    if deadline and deadline < datetime.now():
        raise ValidationError("Deadline cannot be in the past")


def validate_unique_name(existing_names: list, new_name: str, item_type: str = "item"):
    """Validate unique name"""
    if new_name in existing_names:
        raise ValidationError(f"{item_type} name must be unique")