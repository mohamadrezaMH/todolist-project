from .base import Base
from .session import engine


def init_database():
    """Create all tables in the database"""
    # Import models inside function to avoid circular imports
    from ..models.project import Project
    from ..models.task import Task
    
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


if __name__ == "__main__":
    init_database()