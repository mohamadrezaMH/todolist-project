from .base import Base
from .session import engine
from ..models.project import Project
from ..models.task import Task


def init_database():
    """Create all tables in the database"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_database()