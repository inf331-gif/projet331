from typing import Any, Dict, Optional, List
from pydantic import BaseModel
from datetime import datetime

class APIResponse(BaseModel):
    """
    Format standardisé des réponses API pour tous les microservices
    Assure la cohérence entre tous les services
    """
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: str = None
    
    def __init__(self, **data):
        if 'timestamp' not in data:
            data['timestamp'] = datetime.utcnow().isoformat() + 'Z'
        super().__init__(**data)
    
    @classmethod
    def success_response(cls, message: str, data: Any = None, metadata: Optional[Dict[str, Any]] = None):
        """Réponse de succès standardisée"""
        return cls(
            success=True,
            message=message,
            data=data,
            metadata=metadata
        )
    
    @classmethod
    def error_response(cls, message: str, errors: Optional[List[str]] = None, metadata: Optional[Dict[str, Any]] = None):
        """Réponse d'erreur standardisée"""
        return cls(
            success=False,
            message=message,
            errors=errors or [],
            metadata=metadata
        )
    
    @classmethod
    def paginated_response(cls, message: str, data: List[Any], page: int, page_size: int, total: int):
        """Réponse paginée standardisée"""
        metadata = {
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size
            }
        }
        return cls.success_response(message, data, metadata)
    
    @classmethod
    def created_response(cls, message: str, data: Any = None, resource_id: str = None):
        """Réponse pour création de ressource"""
        metadata = {"resource_id": resource_id} if resource_id else None
        return cls.success_response(message, data, metadata)
    
    @classmethod
    def validation_error_response(cls, message: str, field_errors: Dict[str, List[str]]):
        """Réponse pour erreurs de validation"""
        errors = [f"{field}: {', '.join(messages)}" for field, messages in field_errors.items()]
        return cls.error_response(message, errors)