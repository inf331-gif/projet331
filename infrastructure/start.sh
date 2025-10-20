#!/bin/bash

echo " Démarrage du Système Hospitalier Digital..."
echo "=============================================="

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo " Docker n'est pas installé"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo " Docker Compose n'est pas installé"
    exit 1
fi

echo " Docker et Docker Compose sont installés"

# Construire les images
echo "Construction des images Docker..."
docker-compose build

# Démarrer les services
echo " Démarrage des services..."
docker-compose up -d

echo " Attente du démarrage (30 secondes)..."
sleep 30

echo " Vérification des services..."
docker-compose ps

echo ""
echo " Système démarré avec succès!"
echo "================================"
echo "API Gateway: http://localhost:8080"
echo "Documentation: http://localhost:8080/docs"
echo "Auth: http://localhost:8001"
echo "Medical: http://localhost:8003"
echo "ML: http://localhost:8004"
echo "OCR: http://localhost:8005"
echo "Blockchain: http://localhost:8002"
echo "Users: http://localhost:8006"