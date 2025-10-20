#!/usr/bin/env python3
"""
Service Auth - Version corrigée avec gestion bcrypt
"""
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print(f" Project root: {project_root}")

# Maintenant les imports devraient fonctionner
try:
    from fastapi import FastAPI, Depends, HTTPException, status
    from pydantic import BaseModel, EmailStr
    from typing import Optional
    import uvicorn

    # Import de notre architecture
    from shared_libs.security.security_config import SecurityConfig
    from shared_libs.security.jwt_handler import JWTHandler, TokenData
    from shared_libs.security.password_hasher import PasswordHasher
    from shared_libs.utils.logger import get_logger
    from shared_libs.utils.response_formatter import APIResponse
    from shared_libs.utils.error_handler import ErrorHandler
    from shared_libs.utils.validators import DataValidator
    
    print(" Tous les imports réussis!")
    
except ImportError as e:
    print(f" Erreur d'import: {e}")
    sys.exit(1)

# Configuration
app = FastAPI(
    title="Auth Service - TEST",
    description="Service d'authentification pour tests",
    version="1.0.0"
)

# Initialisation des composants
try:
    security_config = SecurityConfig()
    jwt_handler = JWTHandler()
    password_hasher = PasswordHasher()
    logger = get_logger("auth-service-test")
    error_handler = ErrorHandler(app)
    data_validator = DataValidator()
    
    print(" Composants initialisés avec succès!")
    
except Exception as e:
    print(f" Erreur d'initialisation: {e}")
    sys.exit(1)

# Appliquer la sécurité
security_config.setup_security(app)

# Mock de base de données pour les tests
class MockUser:
    def __init__(self, id, email, password_hash, role, is_active=True):
        self.id = id
        self.email = email
        self.mot_de_passe_hash = password_hash
        self.role = role
        self.est_actif = is_active
        self.dernier_acces = None

# Données de test - Utiliser des mots de passe courts
try:
    test_users = [
        MockUser("user-123", "admin@hospital.com", password_hasher.hash_password("admin123"), "ADMINISTRATEUR"),
        MockUser("user-456", "medecin@hospital.com", password_hasher.hash_password("med123"), "MEDECIN"),
        MockUser("user-789", "patient@hospital.com", password_hasher.hash_password("pat123"), "PATIENT")
    ]
    print(" Utilisateurs de test créés!")
except Exception as e:
    print(f" Erreur création utilisateurs test: {e}")
    test_users = []

# Schemas pour les tests
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    nom_complet: str
    telephone: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Routes de test
@app.get("/")
async def root():
    """Route racine pour test"""
    return APIResponse.success_response(
        "Auth Service fonctionne!",
        data={
            "service": "auth",
            "status": "running",
            "version": "1.0.0"
        }
    )

@app.get("/health")
async def health_check():
    """Health check étendu"""
    health_data = {
        "service": "auth",
        "status": "healthy",
        "timestamp": "now",
        "components": {
            "jwt_handler": "ok",
            "password_hasher": "ok",
            "security_config": "ok",
            "logger": "ok"
        }
    }
    return health_data

@app.post("/auth/test/register", response_model=APIResponse)
async def test_register(user_data: UserRegister):
    """Test d'inscription"""
    try:
        logger.info("Test d'inscription", {"email": user_data.email, "role": user_data.role})
        
        # Validation des données
        if not data_validator.validate_email(user_data.email):
            return APIResponse.error_response("Format d'email invalide")
        
        # Vérifier la longueur du mot de passe
        if len(user_data.password) > 50:
            return APIResponse.error_response("Mot de passe trop long (max 50 caractères)")
        
        password_check = data_validator.validate_password_strength(user_data.password)
        if not password_check["is_valid"]:
            return APIResponse.error_response(
                "Mot de passe faible",
                errors=["Le mot de passe doit contenir au moins 8 caractères, majuscule, minuscule, chiffre et caractère spécial"]
            )
        
        # Vérifier si l'utilisateur existe déjà
        existing_user = next((u for u in test_users if u.email == user_data.email), None)
        if existing_user:
            return APIResponse.error_response("Un utilisateur avec cet email existe déjà")
        
        # Simuler la création d'utilisateur
        new_user_id = f"user-{len(test_users) + 1}"
        hashed_password = password_hasher.hash_password(user_data.password)
        new_user = MockUser(new_user_id, user_data.email, hashed_password, user_data.role)
        test_users.append(new_user)
        
        logger.info("Utilisateur test créé", {"user_id": new_user_id, "email": user_data.email})
        
        return APIResponse.success_response(
            "Utilisateur de test créé avec succès",
            data={
                "user_id": new_user_id,
                "email": user_data.email,
                "role": user_data.role
            }
        )
        
    except Exception as e:
        logger.error("Erreur test inscription", {"error": str(e)})
        return APIResponse.error_response("Erreur lors du test d'inscription")

@app.post("/auth/test/login", response_model=APIResponse)
async def test_login(credentials: UserLogin):
    """Test de connexion"""
    try:
        logger.info("Test de connexion", {"email": credentials.email})
        
        # Vérifier la longueur du mot de passe
        if len(credentials.password) > 50:
            return APIResponse.error_response("Mot de passe trop long")
        
        # Trouver l'utilisateur
        user = next((u for u in test_users if u.email == credentials.email and u.est_actif), None)
        
        if not user or not password_hasher.verify_password(credentials.password, user.mot_de_passe_hash):
            logger.warning("Échec authentification test", {"email": credentials.email})
            return APIResponse.error_response("Email ou mot de passe incorrect")
        
        # Créer les tokens
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role
        }
        
        access_token = jwt_handler.create_access_token(token_data)
        refresh_token = jwt_handler.create_refresh_token(token_data)
        
        logger.info("Connexion test réussie", {"user_id": user.id, "email": user.email})
        
        return APIResponse.success_response(
            "Connexion test réussie",
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": jwt_handler.access_token_expire_minutes * 60,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role
                }
            }
        )
        
    except Exception as e:
        logger.error("Erreur test connexion", {"error": str(e)})
        return APIResponse.error_response("Erreur lors du test de connexion")

@app.get("/auth/test/verify-token")
async def test_verify_token(token: str):
    """Test de vérification de token"""
    try:
        payload = jwt_handler.verify_token(token)
        is_expired = jwt_handler.is_token_expired(token)
        
        return APIResponse.success_response(
            "Token vérifié avec succès",
            data={
                "token_valid": True,
                "is_expired": is_expired,
                "payload": payload
            }
        )
    except Exception as e:
        return APIResponse.error_response(
            "Token invalide",
            errors=[str(e)]
        )

@app.get("/auth/test/protected", response_model=APIResponse)
async def test_protected_route(current_user: TokenData = Depends(security_config.get_auth_dependency())):
    """Test de route protégée"""
    logger.info("Accès route protégée test", {"user_id": current_user.user_id, "role": current_user.role})
    
    return APIResponse.success_response(
        "Accès route protégée réussi!",
        data={
            "message": "Vous avez accès à cette route protégée",
            "user": {
                "id": current_user.user_id,
                "email": current_user.email,
                "role": current_user.role
            }
        }
    )

@app.get("/auth/test/admin-only", response_model=APIResponse)
async def test_admin_route(current_user: TokenData = Depends(security_config.get_role_dependency(["ADMINISTRATEUR"]))):
    """Test de route admin seulement"""
    return APIResponse.success_response(
        "Accès route admin réussi!",
        data={
            "message": "Vous êtes administrateur",
            "user": current_user.dict()
        }
    )

@app.get("/auth/test/public")
async def test_public_route():
    """Test de route publique"""
    return APIResponse.success_response(
        "Route publique accessible sans authentification",
        data={"public": True}
    )

# Tests de validation
@app.post("/auth/test/validation")
async def test_validation(email: str, phone: str, password: str):
    """Test des validateurs"""
    validation_results = {
        "email": data_validator.validate_email(email),
        "phone": data_validator.validate_phone(phone),
        "password_strength": data_validator.validate_password_strength(password),
        "sanitized_input": data_validator.sanitize_input("<script>alert('xss')</script>Test")
    }
    
    return APIResponse.success_response(
        "Tests de validation",
        data=validation_results
    )

if __name__ == "__main__":
    print(" Démarrage du Service Auth - TEST")
    print("=" * 50)
    print(" URL: http://localhost:8001")
    print(" Documentation: http://localhost:8001/docs")
    print("Health: http://localhost:8001/health")
    print("=" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )