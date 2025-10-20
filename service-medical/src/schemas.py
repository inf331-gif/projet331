# service-medical/src/schemas.py
from pydantic import BaseModel, validator
from typing import Optional, Dict, Any
from shared_libs.schemas.base import BaseSchema
import enum
from datetime import datetime

class StatutValidation(str, enum.Enum):
    EN_ATTENTE = "en_attente"
    VALIDE = "valide"
    CORRIGE = "corrige"

class DossierMedicalCreate(BaseModel):
    patient_id: str

class DossierMedicalResponse(BaseSchema):
    patient_id: str
    date_creation: str
    date_mise_a_jour: str

class ConsultationCreate(BaseModel):
    dossier_medical_id: str
    etablissement_id: str
    service_hospitalier_id: str
    date_consultation: datetime
    symptomes: Optional[str] = None
    diagnostic: Optional[str] = None
    traitement_prescrit: Optional[str] = None
    observations: Optional[str] = None
    temperature: Optional[str] = None
    url_image_originale: Optional[str] = None

class ConsultationUpdate(BaseModel):
    symptomes: Optional[str] = None
    diagnostic: Optional[str] = None
    traitement_prescrit: Optional[str] = None
    observations: Optional[str] = None
    temperature: Optional[str] = None
    donnees_extraites_json: Optional[Dict[str, Any]] = None
    score_confiance_ocr: Optional[str] = None
    statut_validation: Optional[StatutValidation] = None

class ConsultationResponse(BaseSchema):
    dossier_medical_id: str
    etablissement_id: str
    service_hospitalier_id: str
    date_consultation: str
    symptomes: Optional[str] = None
    diagnostic: Optional[str] = None
    traitement_prescrit: Optional[str] = None
    observations: Optional[str] = None
    temperature: Optional[str] = None
    url_image_originale: Optional[str] = None
    donnees_extraites_json: Optional[Dict[str, Any]] = None
    score_confiance_ocr: Optional[str] = None
    statut_validation: StatutValidation