#!/bin/bash

# Obtener la ruta del script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Ir al directorio padre (donde está docker-compose.yml)
cd "$SCRIPT_DIR/.." || {
    echo "No se pudo acceder al directorio padre del script."
    exit 1
}

docker-compose restart web