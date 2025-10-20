from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from shared_libs.schemas.base import BaseSchema
import enum

class RoleUtilisateur(str, enum.Enum):
    ADMINISTRATEUR = "administrateur"
    SERVICE_HOSPITALIER = "service_hospitalier"
    PATIENT = "patient"

class UtilisateurCreate(BaseModel):
    email: EmailStr
    mot_de_passe: str
    nom_complet: str
    telephone: str
    role: RoleUtilisateur
    
    @validator('mot_de_passe')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Le mot de passe doit contenir au moins 8 caractères')
        return v

class UtilisateurUpdate(BaseModel):
    nom_complet: Optional[str] = None
    telephone: Optional[str] = None
    est_actif: Optional[bool] = None

class UtilisateurResponse(BaseSchema):
    email: str
    nom_complet: str
    telephone: str
    role: RoleUtilisateur
    dernier_acces: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    mot_de_passe: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"