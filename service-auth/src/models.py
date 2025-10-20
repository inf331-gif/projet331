# service-auth/src/models.py
from sqlalchemy import Column, String, Enum as SQLEnum, DateTime
from shared_libs.model import BaseModel

import enum

class RoleUtilisateur(enum.Enum):
    ADMINISTRATEUR = "administrateur"
    SERVICE_HOSPITALIER = "service_hospitalier"
    PATIENT = "patient"

class Utilisateur(BaseModel):
    __tablename__ = "utilisateurs"
    
    email = Column(String(255), unique=True, nullable=False, index=True)
    mot_de_passe_hash = Column(String(255), nullable=False)
    nom_complet = Column(String(255), nullable=False)
    telephone = Column(String(20), nullable=False)
    role = Column(SQLEnum(RoleUtilisateur), nullable=False)
    dernier_acces = Column(DateTime, nullable=True)