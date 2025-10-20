# shared-libs/database/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta
import os
from contextlib import contextmanager
from typing import Generator

Base: DeclarativeMeta = declarative_base()

class DatabaseManager:
    """Gestionnaire de base de données avancé avec context manager"""
    
    def __init__(self, database_url: str):
        self.engine = create_engine(
            database_url,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            echo=False  # Mettre à True pour le debug
        )
        self.SessionLocal = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=self.engine
        )
    
    def get_session(self):
        return self.SessionLocal()
    
    @contextmanager
    def session_scope(self) -> Generator:
        """Context manager pour la gestion automatique des sessions"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def create_tables(self):
        """Crée toutes les tables dans la base de données"""
        Base.metadata.create_all(bind=self.engine)
    
    def drop_tables(self):
        """Supprime toutes les tables (pour les tests)"""
        Base.metadata.drop_all(bind=self.engine)