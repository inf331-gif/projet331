import re
import uuid as uuid_lib
from typing import Any, Optional, List
from pydantic import BaseModel, validator, EmailStr
import phonenumbers
from datetime import datetime, date

class DataValidator:
    """
    Validateurs de données pour tous les microservices
    Validation centralisée des données métier
    """
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valider format email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str, country: str = "CM") -> bool:
        """Valider numéro de téléphone avec libphonenumber"""
        try:
            parsed_number = phonenumbers.parse(phone, country)
            return phonenumbers.is_valid_number(parsed_number)
        except:
            return False
    
    @staticmethod
    def validate_uuid(uuid_string: str) -> bool:
        """Valider format UUID"""
        try:
            uuid_lib.UUID(uuid_string)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_date_format(date_string: str, format: str = "%Y-%m-%d") -> bool:
        """Valider format de date"""
        try:
            datetime.strptime(date_string, format)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def sanitize_input(input_string: str) -> str:
        """Nettoyer les entrées utilisateur"""
        if not input_string:
            return ""
        
        # Supprimer les caractères dangereux
        dangerous_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'on\w+=',
            r'<.*?>'
        ]
        
        sanitized = input_string
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        return sanitized.strip()
    
    @staticmethod
    def validate_password_strength(password: str) -> dict:
        """Valider la force du mot de passe"""
        checks = {
            "length": len(password) >= 8,
            "uppercase": bool(re.search(r'[A-Z]', password)),
            "lowercase": bool(re.search(r'[a-z]', password)),
            "digit": bool(re.search(r'\d', password)),
            "special": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        }
        
        return {
            "is_valid": all(checks.values()),
            "checks": checks
        }

class MedicalDataValidator(DataValidator):
    """Validateurs spécifiques aux données médicales"""
    
    @staticmethod
    def validate_temperature(temp: float) -> bool:
        return 20.0 <= temp <= 45.0
    
    @staticmethod
    def validate_blood_pressure(systolic: int, diastolic: int) -> bool:
        return (50 <= systolic <= 250) and (30 <= diastolic <= 150)
    
    @staticmethod
    def validate_heart_rate(rate: int) -> bool:
        return 30 <= rate <= 200
    
    @staticmethod
    def validate_medical_notes(notes: str) -> bool:
        """Valider que les notes médicales ne contiennent pas de code malveillant"""
        dangerous_keywords = ['<script>', 'javascript:', 'onload=']
        return not any(keyword in notes.lower() for keyword in dangerous_keywords)