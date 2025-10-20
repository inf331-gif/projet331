# service-medical/src/models.py
from sqlalchemy import Column, String, DateTime, Text, JSON, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from shared_libs.model import BaseModel
import enum

class StatutValidation(enum.Enum):
    EN_ATTENTE = "en_attente"
    VALIDE = "valide"
    CORRIGE = "corrige"

class DossierMedical(BaseModel):
    __tablename__ = "dossiers_medicaux"
    
    patient_id = Column(String(36), nullable=False, index=True)
    date_creation = Column(DateTime, nullable=False)
    date_mise_a_jour = Column(DateTime, nullable=False)
    
    consultations = relationship(
            "Consultation", 
            back_populates="dossier_medical",
            cascade="all, delete-orphan",
            lazy="selectin"
        )

class Consultation(BaseModel):
    __tablename__ = "consultations"
    
    dossier_medical_id = Column(String(36), ForeignKey("dossiers_medicaux.id"), nullable=False)
    etablissement_id = Column(String(36), nullable=False, index=True)
    service_hospitalier_id = Column(String(36), nullable=False, index=True)
    
    date_consultation = Column(DateTime, nullable=False)
    symptomes = Column(Text)
    diagnostic = Column(Text)
    traitement_prescrit = Column(Text)
    observations = Column(Text)
    temperature = Column(String(10))
    
    url_image_originale = Column(String(500))
    donnees_extraites_json = Column(JSON)
    score_confiance_ocr = Column(String(10))
    statut_validation = Column(SQLEnum(StatutValidation), default=StatutValidation.EN_ATTENTE)
    
    dossier_medical = relationship(
            "DossierMedical", 
            back_populates="consultations",
            lazy="joined"
        )