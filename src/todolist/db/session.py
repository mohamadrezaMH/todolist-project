from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from typing import Iterator


DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///todolist.db"
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

def get_db() -> Iterator[Session]:
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()