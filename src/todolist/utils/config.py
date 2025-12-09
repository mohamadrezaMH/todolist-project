import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# مسیر دیتابیس SQLite
BASE_DIR = Path(__file__).parent.parent.parent
SQLITE_DB_PATH = BASE_DIR / "todolist.db"


class Config:
    """Configuration management class"""
    
    # Database URL - استفاده از SQLite برای سادگی
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{SQLITE_DB_PATH}"
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