#!/bin/bash
# Script de démarrage pour CloudJobHunt API avec uvicorn

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# Activer l'environnement virtuel s'il existe
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Exporter les variables d'environnement par défaut
export PYTHONUNBUFFERED=1
export APP_URL="https://cloudjobhunt.42web.io"
export DOMAIN_NAME="cloudjobhunt.42web.io"

# Variables de base de données (à adapter selon votre infra)
export DATABASE_HOST="${DATABASE_HOST:-localhost}"
export DATABASE_PORT="${DATABASE_PORT:-5432}"
export DATABASE_NAME="${DATABASE_NAME:-cloudjobhunt}"
export DATABASE_USER="${DATABASE_USER:-postgres}"
export DATABASE_PASSWORD="${DATABASE_PASSWORD:-postgres}"

# Clé secrète (ATTENTION: à générer et mettre en secret pour production)
export SECRET_KEY="${SECRET_KEY:-your-secret-key-change-in-production}"

echo "🚀 Démarrage CloudJobHunt API..."
echo "   Hôte: 0.0.0.0"
echo "   Port: 8000"
echo "   BDD: $DATABASE_HOST:$DATABASE_PORT/$DATABASE_NAME"

# Lancer uvicorn
exec uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --reload
