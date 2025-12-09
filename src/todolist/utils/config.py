import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Project settings management class from environment variables"""
    
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://todolist_user:todolist_password@localhost:5432/todolist"
    )
    
    # Application Limits
    MAX_NUMBER_OF_PROJECTS = int(os.getenv("MAX_NUMBER_OF_PROJECTS", "10"))
    MAX_NUMBER_OF_TASKS = int(os.getenv("MAX_NUMBER_OF_TASKS", "100"))
    
    # Text Length Limits
    MAX_PROJECT_NAME_LENGTH = 30
    MAX_PROJECT_DESCRIPTION_LENGTH = 150
    MAX_TASK_TITLE_LENGTH = 30
    MAX_TASK_DESCRIPTION_LENGTH = 150
    
    # Valid Task Statuses
    VALID_TASK_STATUSES = ["todo", "doing", "done"]