#!/bin/bash

# Obtener la ruta del script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Ir al directorio padre (donde está docker-compose.yml)
cd "$SCRIPT_DIR/.." || {
    echo "No se pudo acceder al directorio padre del script."
    exit 1
}

find . -type d -name "__pycache__" -exec rm -rf {}