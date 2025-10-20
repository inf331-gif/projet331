from pydantic import BaseModel as PydanticBaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

class BaseSchema(PydanticBaseModel):
    """Schéma de base Pydantic"""
    
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: Optional[bool] = True
    
    class Config:
        from_attributes = True
        json_encoders = {
            UUID: str,
            datetime: lambda dt: dt.isoformat()
        }