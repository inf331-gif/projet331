
"""
Script pour exécuter le service avec le bon PYTHONPATH
"""
import sys
import os

# Ajouter le chemin racine du projet au PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

# Maintenant importer et exécuter
from main import app
import uvicorn

if __name__ == "__main__":
    print(" Démarrage du Service Auth - TEST")
    print("=" * 50)
    print("URL: http://localhost:8001")
    print(" Documentation: http://localhost:8001/docs")
    print("Health: http://localhost:8001/health")
    print("=" * 50)
    
    uvicorn.run(
        "runner:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )