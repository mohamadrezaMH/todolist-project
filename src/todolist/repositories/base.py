from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')


class BaseRepository(Generic[T], ABC):
    """Abstract base class for all repositories"""
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """Add a new entity"""
        pass
    
    @abstractmethod
    def get(self, id: int) -> Optional[T]:
        """Get entity by ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities"""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Update existing entity"""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """Delete entity by ID"""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Get total count of entities"""
        pass