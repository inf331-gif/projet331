from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Callable
from .jwt_handler import JWTHandler
from .service_authenticator import ServiceAuthenticator

class AuthMiddleware:
    """
    Middleware d'authentification - Version corrigée
    """
    
    def __init__(self):
        self.jwt_handler = JWTHandler()
        self.service_auth = ServiceAuthenticator()
        self.security = HTTPBearer(auto_error=False)
    
    async def __call__(self, request: Request, call_next):
        """Middleware principal"""
        # Vérifier si la route est publique
        if self._is_public_route(request):
            return await call_next(request)
        
        # Récupérer le token
        credentials: Optional[HTTPAuthorizationCredentials] = await self.security(request)
        
        if not credentials:
            raise HTTPException(
                status_code=401,
                detail="Header Authorization manquant"
            )
        
        # Valider le token
        try:
            token_data = await self.jwt_handler.get_current_user(credentials)
            request.state.user = token_data
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail=f"Erreur d'authentification: {str(e)}"
            )
        
        response = await call_next(request)
        return response
    
    def _is_public_route(self, request: Request) -> bool:
        """
        Vérifier si la route est publique - CORRIGÉ
        """
        public_paths = [
            "/health", 
            "/docs", 
            "/redoc", 
            "/openapi.json",
            "/favicon.ico",  #  Ajout favicon
            "/auth/",  #  Toutes les routes auth
            "/auth/test/",  #  Toutes les routes test auth
            "/medical/test/public",  #  Route publique médicale
        ]
        
        # Vérifier si le chemin commence par un des chemins publics
        path = request.url.path
        return any(path.startswith(public_path) for public_path in public_paths)
    
    def require_role(self, required_roles: list):
        """Dependency pour vérifier les rôles"""
        async def role_checker(user = Depends(self.jwt_handler.get_current_user)):
            if user.role not in required_roles:
                raise HTTPException(
                    status_code=403,
                    detail="Permissions insuffisantes"
                )
            return user
        return role_checker