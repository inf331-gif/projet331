import logging
import json
import os
import sys
from datetime import datetime,timezone
from typing import Dict, Any, Optional
from pathlib import Path

class StructuredLogger:
    """
    Logger structuré pour microservices avec format JSON
    Compatible avec Elasticsearch, Loki, etc.
    """
    
    def __init__(self, service_name: str, log_level: str = None):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self._setup_logger(log_level)
    
    def _setup_logger(self, log_level: str = None):
        """Configurer le logger avec format JSON"""
        if self.logger.handlers:
            return  # Déjà configuré
            
        # Niveau de log
        level = getattr(logging, log_level or os.getenv("LOG_LEVEL", "INFO"))
        self.logger.setLevel(level)
        
        # Formateur JSON
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "service": "%(name)s", "level": "%(levelname)s", "message": "%(message)s", "data": %(data)s}',
            datefmt='%Y-%m-%dT%H:%M:%SZ'
        )
        
        # Handler console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Handler fichier (optionnel)
        log_file = os.getenv("LOG_FILE")
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def _create_log_record(self, level: str, message: str, extra_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Créer un enregistrement de log structuré"""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
            "service": self.service_name,
            "level": level,
            "message": message,
            "data": extra_data or {}
        }
    
    def info(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """Log niveau info"""
        log_record = self._create_log_record("INFO", message, extra_data)
        self.logger.info(message, extra={"data": json.dumps(log_record["data"])})
    
    def error(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """Log niveau error"""
        log_record = self._create_log_record("ERROR", message, extra_data)
        self.logger.error(message, extra={"data": json.dumps(log_record["data"])})
    
    def warning(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """Log niveau warning"""
        log_record = self._create_log_record("WARNING", message, extra_data)
        self.logger.warning(message, extra={"data": json.dumps(log_record["data"])})
    
    def debug(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """Log niveau debug"""
        log_record = self._create_log_record("DEBUG", message, extra_data)
        self.logger.debug(message, extra={"data": json.dumps(log_record["data"])})
    
    def audit(self, action: str, user_id: str, resource: str, details: Dict[str, Any]):
        """Log d'audit spécialisé"""
        audit_data = {
            "action": action,
            "user_id": user_id,
            "resource": resource,
            "details": details
        }
        self.info(f"Audit: {action} on {resource}", audit_data)
    
    def performance(self, operation: str, duration_ms: float, extra_data: Optional[Dict[str, Any]] = None):
        """Log de performance"""
        perf_data = {
            "operation": operation,
            "duration_ms": duration_ms,
            **(extra_data or {})
        }
        self.info(f"Performance: {operation} - {duration_ms}ms", perf_data)

# Instance globale pour import facile
def get_logger(service_name: str) -> StructuredLogger:
    return StructuredLogger(service_name)