# service-utilisateurs/src/schemas.py
from pydantic import BaseModel, validator
from typing import Optional
from shared_libs.schemas.base import BaseSchema
import enum
from datetime import datetime

class Sexe(str, enum.Enum):
    M = "M"
    F = "F"

class TypeZone(str, enum.Enum):
    URBAIN = "urbain"
    RURAL = "rural"

class TypeEtablissement(str, enum.Enum):
    PUBLIC = "public"
    PRIVE = "prive"

class PatientCreate(BaseModel):
    utilisateur_id: str
    date_naissance: datetime
    sexe: Sexe
    region: str
    type_zone: TypeZone

class PatientResponse(BaseSchema):
    utilisateur_id: str
    date_naissance: str
    sexe: Sexe
    region: str
    type_zone: TypeZone

class EtablissementCreate(BaseModel):
    nom: str
    adresse: str
    region: str
    type: TypeEtablissement

class EtablissementResponse(BaseSchema):
    nom: str
    adresse: str
    region: str
    type: TypeEtablissement

class ServiceHospitalierCreate(BaseModel):
    utilisateur_id: str
    etablissement_id: str
    fonction: str
    specialite: Optional[str] = None
    matricule: Optional[str] = None

class ServiceHospitalierResponse(BaseSchema):
    utilisateur_id: str
    etablissement_id: str
    fonction: str
    specialite: Optional[str] = None
    matricule: Optional[str] = None