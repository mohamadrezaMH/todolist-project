from .base import BaseError


class ServiceError(BaseError):
    """Base exception for service layer errors"""
    pass


class ValidationError(ServiceError):
    """Raised when validation fails"""
    
    def __init__(self, message: str, field: str = None):
        details = {"field": field} if field else {}
        super().__init__(message, details)