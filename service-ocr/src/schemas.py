# service-ocr/src/schemas.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from shared_libs.schemas.base import BaseSchema
import enum

class MoteurOCR(str, enum.Enum):
    TROCR = "tror"
    EASY_OCR = "easy_ocr"

class OCRProcessRequest(BaseModel):
    consultation_id: str
    image_url: str
    moteur_suggestion: Optional[MoteurOCR] = None

class OCRProcessResponse(BaseSchema):
    consultation_id: str
    texte_extrait: str
    donnees_structurees: Dict[str, Any]
    moteur_utilise: MoteurOCR
    confiance_globale: float
    temps_traitement: int

class TraitementOCRResponse(BaseSchema):
    consultation_id: str
    nom_fichier_original: str
    type_fichier: str
    taille_fichier: int
    temps_traitement: Optional[int] = None
    moteur_ocr_selectionne: Optional[MoteurOCR] = None
    confiance_globale: Optional[str] = None