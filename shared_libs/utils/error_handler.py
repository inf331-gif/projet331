from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Union, Dict, Any
import logging
from .response_formatter import APIResponse

class ErrorHandler:
    """
    Gestionnaire d'erreurs global pour tous les microservices - Version corrigée
    """
    
    def __init__(self, app: FastAPI = None):
        if app:
            self.setup_global_handlers(app)
    
    def setup_global_handlers(self, app: FastAPI):
        """Configurer les handlers d'erreur globaux"""
        
        @app.exception_handler(HTTPException)
        async def http_exception_handler(request: Request, exc: HTTPException):
            """Handler pour HTTPException - CORRIGÉ"""
            return JSONResponse(
                status_code=exc.status_code,
                content=APIResponse.error_response(
                    message=exc.detail,
                    errors=[exc.detail]
                ).dict()
            )
        
        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            """Handler pour erreurs de validation"""
            errors = []
            for error in exc.errors():
                field = " -> ".join(str(loc) for loc in error["loc"])
                errors.append(f"{field}: {error['msg']}")
            
            return JSONResponse(
                status_code=422,
                content=APIResponse.validation_error_response(
                    message="Erreur de validation des données",
                    field_errors={error["loc"][-1]: [error["msg"]] for error in exc.errors()}
                ).dict()
            )
        
        @app.exception_handler(Exception)
        async def general_exception_handler(request: Request, exc: Exception):
            """Handler pour toutes les autres exceptions - CORRIGÉ"""
            # Ne pas logger les erreurs d'authentification normales
            if not isinstance(exc, HTTPException) or exc.status_code != 401:
                logging.error(f"Erreur non gérée: {str(exc)}", exc_info=True)
            
            return JSONResponse(
                status_code=500,
                content=APIResponse.error_response(
                    message="Erreur interne du serveur",
                    errors=["Une erreur interne est survenue"]
                ).dict()
            )