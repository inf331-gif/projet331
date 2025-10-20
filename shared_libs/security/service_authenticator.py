import httpx
from fastapi import HTTPException, Header, Depends
from typing import Optional, Dict, Any
import os

class ServiceAuthenticator:
    """
        Authentification et autorisation pour les communications inter-services
        Utilise API Keys et JWT pour sécuriser les appels
    """
    
    def __init__(self):
        self.service_api_keys = {
            "auth-service": os.getenv("AUTH_SERVICE_API_KEY", "auth-key-123"),
            "users-service": os.getenv("USERS_SERVICE_API_KEY", "users-key-123"),
            "medical-service": os.getenv("MEDICAL_SERVICE_API_KEY", "medical-key-123"),
            "ocr-service": os.getenv("OCR_SERVICE_API_KEY", "ocr-key-123"),
            "ml-service": os.getenv("ML_SERVICE_API_KEY", "ml-key-123"),
            "blockchain-service": os.getenv("BLOCKCHAIN_SERVICE_API_KEY", "blockchain-key-123"),
        }
    
    async def verify_service_api_key(self, x_api_key: str = Header(...)) -> str:
        """
        Middleware FastAPI pour vérifier les API Keys de service
        """
        for service_name, api_key in self.service_api_keys.items():
            if api_key == x_api_key:
                return service_name
        
        raise HTTPException(
            status_code=403,
            detail="API Key invalide pour l'accès au service"
        )
    
    async def make_authenticated_request(
        self, 
        service_url: str, 
        endpoint: str, 
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        service_name: str = "internal"
    ) -> httpx.Response:
        """
        Faire une requête authentifiée vers un autre service
        """
        headers = {
            "X-API-Key": self.service_api_keys.get(service_name, ""),
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            url = f"{service_url}{endpoint}"
            
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, timeout=30.0)
            elif method.upper() == "POST":
                response = await client.post(url, json=data, headers=headers, timeout=30.0)
            elif method.upper() == "PUT":
                response = await client.put(url, json=data, headers=headers, timeout=30.0)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers, timeout=30.0)
            else:
                raise ValueError(f"Méthode HTTP non supportée: {method}")
            
            return response