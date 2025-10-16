from datetime import datetime
from typing import Optional
from .config import Config


class ValidationError(Exception):
    """Custom validation error"""

    pass


def validate_text_length(text: str, field_name: str, min_length: int, max_length: int):
    """Text length validation"""
    if not text or len(text.strip()) == 0:
        raise ValidationError(f"{field_name} نمی‌تواند خالی باشد")

    if len(text) > max_length:
        raise ValidationError(
            f"{field_name} نمی‌تواند بیشتر از {max_length} کاراکتر باشد"
        )

    if len(text) < min_length:
        raise ValidationError(f"{field_name} باید حداقل {min_length} کاراکتر باشد")


def validate_status(status: str):
    """Task status validation"""
    if status not in Config.VALID_TASK_STATUSES:
        valid_statuses = ", ".join(Config.VALID_TASK_STATUSES)
        raise ValidationError(f"وضعیت باید یکی از موارد زیر باشد: {valid_statuses}")


def validate_deadline(deadline: Optional[datetime]):
    """Deadline date validation"""
    if deadline and deadline < datetime.now():
        raise ValidationError("ددلاین نمی‌تواند در گذشته باشد")


def validate_unique_name(existing_names: list, new_name: str, item_type: str = "پروژه"):
    """Name uniqueness validation"""
    if new_name in existing_names:
        raise ValidationError(f"نام {item_type} باید یکتا باشد")
