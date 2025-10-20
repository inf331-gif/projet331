import os
import logging
from typing import Any, Dict, List
from dotenv import load_dotenv

# Charger les variables d'environnement depuis les fichiers .env
load_dotenv()

class ConfigManager:
    """
    Gestionnaire de configuration compatible avec tes fichiers .env actuels
    """

    _config_cache = {}

    @classmethod
    def get_service_config(cls, service_name: str) -> Dict[str, Any]:
        """Obtenir la configuration pour un service spécifique"""
        if service_name in cls._config_cache:
            return cls._config_cache[service_name]

        # Construction de la configuration
        config = {
            "SERVICE_NAME": service_name,
            "SERVICE_PORT": cls._get_int("SERVICE_PORT", cls._get_default_port(service_name)),
            "DEBUG": cls._get_bool("DEBUG", True),
            "ENVIRONMENT": os.getenv("ENVIRONMENT", "development"),
            "DATABASE_URL": cls._get_database_url(),
            "JWT_SECRET_KEY": os.getenv("JWT_SECRET_KEY", "fallback-jwt-secret-change-in-production"),
            "JWT_ALGORITHM": os.getenv("JWT_ALGORITHM", "HS256"),
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES": cls._get_int("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30),
            "API_KEY": os.getenv("API_KEY", f"{service_name}-default-key"),
        }

        # Ajouter la config spécifique
        config.update(cls._get_service_specific_config(service_name))

        cls._config_cache[service_name] = config
        return config

    @classmethod
    def _get_default_port(cls, service_name: str) -> int:
        ports = {
            "auth-service": 8001,
            "users-service": 8006,
            "medical-service": 8003,
            "ocr-service": 8005,
            "ml-service": 8004,
            "blockchain-service": 8002,
            "api-gateway": 8080,
        }
        return ports.get(service_name, 8000)

    @classmethod
    def _get_database_url(cls) -> str:
        """Retourne DATABASE_URL tel quel depuis le .env"""
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            logging.warning("DATABASE_URL non défini dans .env, fallback utilisé")
            db_url = "postgresql://user:pass@localhost:5432/db"
        return db_url

    @classmethod
    def _get_service_specific_config(cls, service_name: str) -> Dict[str, Any]:
        """Configuration spécifique à chaque service"""
        configs = {
            "auth-service": {
                "BCRYPT_ROUNDS": cls._get_int("BCRYPT_ROUNDS", 12),
                "JWT_REFRESH_TOKEN_EXPIRE_DAYS": cls._get_int("JWT_REFRESH_TOKEN_EXPIRE_DAYS", 7),
            },
            "medical-service": {
                "MAX_FILE_SIZE_MB": cls._get_int("MAX_FILE_SIZE_MB", 10),
                "ALLOWED_FILE_TYPES": cls._get_list("ALLOWED_FILE_TYPES", ["image/jpeg", "image/png", "application/pdf"]),
                "AUTH_SERVICE_URL": os.getenv("AUTH_SERVICE_URL"),
                "USERS_SERVICE_URL": os.getenv("USERS_SERVICE_URL"),
            },
            "ocr-service": {
                "OCR_ENGINE": os.getenv("OCR_ENGINE", "easyocr"),
                "DEFAULT_CONFIDENCE_THRESHOLD": cls._get_float("DEFAULT_CONFIDENCE_THRESHOLD", 0.7),
                "MEDICAL_SERVICE_URL": os.getenv("MEDICAL_SERVICE_URL"),
            },
            "ml-service": {
                "MODEL_CONFIDENCE_THRESHOLD": cls._get_float("MODEL_CONFIDENCE_THRESHOLD", 0.75),
                "BATCH_SIZE": cls._get_int("BATCH_SIZE", 32),
                "MEDICAL_SERVICE_URL": os.getenv("MEDICAL_SERVICE_URL"),
            },
            "api-gateway": {
                "AUTH_SERVICE_URL": os.getenv("AUTH_SERVICE_URL"),
                "USERS_SERVICE_URL": os.getenv("USERS_SERVICE_URL"),
                "MEDICAL_SERVICE_URL": os.getenv("MEDICAL_SERVICE_URL"),
                "OCR_SERVICE_URL": os.getenv("OCR_SERVICE_URL"),
                "ML_SERVICE_URL": os.getenv("ML_SERVICE_URL"),
                "BLOCKCHAIN_SERVICE_URL": os.getenv("BLOCKCHAIN_SERVICE_URL"),
            }
        }
        return configs.get(service_name, {})

    @classmethod
    def _get_int(cls, key: str, default: int) -> int:
        try:
            return int(os.getenv(key, default))
        except ValueError:
            return default

    @classmethod
    def _get_float(cls, key: str, default: float) -> float:
        try:
            return float(os.getenv(key, default))
        except ValueError:
            return default

    @classmethod
    def _get_bool(cls, key: str, default: bool) -> bool:
        val = os.getenv(key, str(default)).lower()
        return val in ['true', '1', 'yes', 'y']

    @classmethod
    def _get_list(cls, key: str, default: List[str]) -> List[str]:
        val = os.getenv(key)
        if not val:
            return default
        return [item.strip() for item in val.split(",")]

    @classmethod
    def print_config_status(cls):
        """Afficher le statut de la configuration"""
        services = [
            "auth-service", "users-service", "medical-service",
            "ocr-service", "ml-service", "blockchain-service", "api-gateway"
        ]

        print(" STATUT DE LA CONFIGURATION")
        print("=" * 50)

        for service in services:
            config = cls.get_service_config(service)
            print(f" {service}:")
            print(f"   Port: {config['SERVICE_PORT']}")
            print(f"   Database: {'ok' if config['DATABASE_URL'] else 'wrong'}")
            print(f"   JWT: {'ok' if config['JWT_SECRET_KEY'] else 'wrong'}")
            print()
