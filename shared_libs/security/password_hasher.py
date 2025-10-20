from passlib.context import CryptContext
import os
import hashlib

class PasswordHasher:
    """
    Gestionnaire de hashage de mots de passe - Version corrigée
    """
    
    def __init__(self):
        # Utiliser un algorithme plus simple si bcrypt pose problème
        try:
            self.pwd_context = CryptContext(
                schemes=["bcrypt"],
                deprecated="auto",
                bcrypt__rounds=4  # Réduire pour les tests
            )
            self._test_bcrypt()
        except Exception:
            # Fallback vers pbkdf2_sha256 si bcrypt échoue
            self.pwd_context = CryptContext(
                schemes=["pbkdf2_sha256"],
                deprecated="auto",
                pbkdf2_sha256__default_rounds=30000
            )
            print("⚠️  Utilisation de pbkdf2_sha256 comme fallback")
    
    def _test_bcrypt(self):
        """Tester bcrypt avec un mot de passe court"""
        test_hash = self.pwd_context.hash("test")
        assert self.pwd_context.verify("test", test_hash)
    
    def hash_password(self, password: str) -> str:
        """
        Hasher un mot de passe de manière sécurisée
        """
        # Tronquer les mots de passe trop longs pour bcrypt
        if len(password) > 50:
            password = password[:50]
        
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Vérifier un mot de passe contre son hash
        """
        # Tronquer si nécessaire
        if len(plain_password) > 50:
            plain_password = plain_password[:50]
            
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def needs_rehash(self, hashed_password: str) -> bool:
        """Vérifier si un hash doit être re-hashé"""
        return self.pwd_context.needs_update(hashed_password)