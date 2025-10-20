# service-utilisateurs/src/models.py
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from shared_libs.model import BaseModel
import enum

class Sexe(enum.Enum):
    M = "M"
    F = "F"

class TypeZone(enum.Enum):
    URBAIN = "urbain"
    RURAL = "rural"

class TypeEtablissement(enum.Enum):
    PUBLIC = "public"
    PRIVE = "prive"

class Patient(BaseModel):
    __tablename__ = "patients"
    
    utilisateur_id = Column(String(36), unique=True, nullable=False, index=True)
    date_naissance = Column(DateTime, nullable=False)
    sexe = Column(SQLEnum(Sexe), nullable=False)
    region = Column(String(100), nullable=False)
    type_zone = Column(SQLEnum(TypeZone), nullable=False)

class Etablissement(BaseModel):
    __tablename__ = "etablissements"
    
    nom = Column(String(255), nullable=False)
    adresse = Column(String(500), nullable=False)
    region = Column(String(100), nullable=False)
    type = Column(SQLEnum(TypeEtablissement), nullable=False)

class ServiceHospitalier(BaseModel):
    __tablename__ = "services_hospitaliers"
    
    utilisateur_id = Column(String(36), unique=True, nullable=False, index=True)
    etablissement_id = Column(String(36), nullable=False, index=True)
    fonction = Column(String(100), nullable=False)
    specialite = Column(String(100))
    matricule = Column(String(50))