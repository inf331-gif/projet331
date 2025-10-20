from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import os
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import secrets

class TokenData(BaseModel):
    """Données du token JWT"""
    user_id: str
    email: str
    role: str
    exp: datetime

class JWTHandler:
    """
    Gestionnaire JWT complet - Équivalent Spring Security JwtService
    """
    
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", self._generate_secret_key())
        self.algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.refresh_token_expire_days = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", "7"))
        self.security = HTTPBearer()
    
    def _generate_secret_key(self) -> str:
        """Générer une clé secrète sécurisée"""
        return secrets.token_urlsafe(64)
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """
        Créer un token JWT d'accès
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({
            "exp": expire, 
            "type": "access",
            "iat": datetime.now(timezone.utc)  
        })
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Créer un token de rafraîchissement"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({
            "exp": expire, 
            "type": "refresh",
            "iat": datetime.now(timezone.utc) 
        })
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Vérifier et décoder un token JWT
        """
        try:
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm],
                options={"verify_exp": True} 
            )
            return payload
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token invalide: {str(e)}"
            )
    
    def extract_user_id(self, token: str) -> str:
        """Extraire l'ID utilisateur du token"""
        payload = self.verify_token(token)
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="User ID manquant dans le token")
        return user_id
    
    def extract_email(self, token: str) -> str:
        """Extraire l'email du token"""
        payload = self.verify_token(token)
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Email manquant dans le token")
        return email
    
    def is_token_expired(self, token: str) -> bool:
        """Vérifier si le token est expiré"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm], options={"verify_exp": False})
            exp_timestamp = payload.get("exp")
            if exp_timestamp is None:
                return True
            
            exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            return datetime.now(timezone.utc) > exp_datetime
            
        except Exception:
            return True
    
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> TokenData:
        """
        Dependency pour récupérer l'utilisateur courant
        """
        token = credentials.credentials
        
        if self.is_token_expired(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expiré"
            )
        
        try:
            payload = self.verify_token(token)
            user_id = payload.get("user_id")
            email = payload.get("email")
            role = payload.get("role")
            exp_timestamp = payload.get("exp")
            
            if user_id is None or email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token invalide: informations manquantes"
                )
            
            exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            
            return TokenData(
                user_id=user_id, 
                email=email, 
                role=role, 
                exp=exp_datetime
            )
            
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Erreur de validation du token: {str(e)}"
            )