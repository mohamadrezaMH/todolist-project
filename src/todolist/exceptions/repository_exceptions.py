from .base import BaseError


class RepositoryError(BaseError):
    """Base exception for repository layer errors"""
    pass


class NotFoundError(RepositoryError):
    """Raised when an entity is not found"""
    
    def __init__(self, entity_type: str, entity_id: int = None):
        message = f"{entity_type} not found"
        if entity_id:
            message = f"{entity_type} with id {entity_id} not found"
        super().__init__(message, {"entity_type": entity_type, "entity_id": entity_id})


class DuplicateError(RepositoryError):
    """Raised when a duplicate entity is detected"""
    
    def __init__(self, entity_type: str, field: str, value: str):
        message = f"{entity_type} with {field} '{value}' already exists"
        super().__init__(message, {"entity_type": entity_type, "field": field, "value": value})