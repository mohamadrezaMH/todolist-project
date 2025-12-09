from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..utils.config import Config
from typing import Iterator

engine = create_engine(
    Config.DATABASE_URL,
    echo=False,  # برای دیباگ می‌تونی True کنی
    future=True   # برای SQLAlchemy 2.0
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

def get_db() ->  Iterator[Session]:
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()