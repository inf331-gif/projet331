from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import json

class SecurityConfig:
    """
        Configuration de sécurité principale - Équivalent SecurityConfiguration Spring
    """
    
    def __init__(self):
        #  Import ici pour éviter les circulaires
        from .jwt_handler import JWTHandler
        from .auth_middleware import AuthMiddleware
        from .service_authenticator import ServiceAuthenticator
        
        self.jwt_handler = JWTHandler()
        self.service_authenticator = ServiceAuthenticator()
        self.auth_middleware = AuthMiddleware()
    
    def setup_security(self, app: FastAPI):
        """
            Configurer la sécurité de l'application
        """
        #  Correction: Gérer CORS_ORIGINS comme string JSON
        cors_origins = os.getenv("CORS_ORIGINS", "[\"*\"]")
        try:
            origins_list = json.loads(cors_origins)
        except json.JSONDecodeError:
            origins_list = ["*"]
        
        # CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins_list,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Middleware d'authentification
        @app.middleware("http")
        async def authentication_middleware(request, call_next):
            return await self.auth_middleware(request, call_next)
        
        return app
    
    def get_auth_dependency(self):
        """
            Obtenir la dépendance d'authentification
        """
        return self.jwt_handler.get_current_user
    
    def get_role_dependency(self, required_roles: list):
        """
            Obtenir la dépendance de vérification de rôle
        """
        return self.auth_middleware.require_role(required_roles)