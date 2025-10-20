# service-ml/src/models.py
from sqlalchemy import Column, String, DateTime, Integer, Boolean, Text, Enum as SQLEnum, JSON
from shared_libs.model import BaseModel
import enum

class FrameworkML(enum.Enum):
    TENSORFLOW = "tensorflow"
    PYTORCH = "pytorch"

class ClassePaludisme(enum.Enum):
    POSITIF = "positif"
    NEGATIF = "negatif"

class NiveauConfiance(enum.Enum):
    FAIBLE = "faible"
    MOYEN = "moyen"
    ELEVE = "eleve"

class FormatExport(enum.Enum):
    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"
    EXCEL = "excel"

class ModeleCNN(BaseModel):
    __tablename__ = "modeles_cnn"
    
    version = Column(String(50), nullable=False)
    nom = Column(String(255), nullable=False)
    framework = Column(SQLEnum(FrameworkML), nullable=False)
    forme_entree = Column(String(100))
    precision = Column(String(10))
    rappel = Column(String(10))
    score_f1 = Column(String(10))
    date_entrainement = Column(DateTime)
    chemin_fichier = Column(String(500))
    est_actif = Column(Boolean, default=False)
    metriques_performance = Column(JSON)

class Prediction(BaseModel):
    __tablename__ = "predictions"
    
    patient_id = Column(String(36), nullable=False, index=True)
    modele_id = Column(String(36), nullable=False, index=True)
    donnees_entree_json = Column(JSON, nullable=False)
    probabilite_paludisme = Column(String(10), nullable=False)
    classe_predite = Column(SQLEnum(ClassePaludisme), nullable=False)
    niveau_confiance = Column(SQLEnum(NiveauConfiance), nullable=False)
    recommandation = Column(Text)
    temps_traitement = Column(String(10))
    resultat_feedback = Column(Boolean)
    commentaire_feedback = Column(Text)
    date_prediction = Column(DateTime)

class Dataset(BaseModel):
    __tablename__ = "datasets"
    
    modele_id = Column(String(36), nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text)
    date_creation = Column(DateTime)
    nombre_enregistrements = Column(Integer)
    niveau_k_anonymat = Column(Integer)
    est_anonymise = Column(Boolean, default=False)
    format_export = Column(SQLEnum(FormatExport))
    chemin_fichier = Column(String(500))