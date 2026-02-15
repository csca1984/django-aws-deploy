#!/bin/bash


# Salir si falla algo
set -e

POSTGRES_HOST=${POSTGRES_HOST:=db}
POSTGRES_PORT=${POSTGRES_PORT:=5432}

# Esperar a Postgres
echo "Esperando a que PostgreSQL esté disponible..."
until nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "PostgreSQL no está listo aún..."
  sleep 1
done

echo "PostgreSQL disponible!"

# Aplicar migraciones
echo "Aplicando migraciones de Django..."
python manage.py migrate --noinput

# Cargando datos iniciales
echo "Aplicando datos iniciales..."
python manage.py init_data


# Recolectar estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Crear superusuario si no existe
echo "Verificando superusuario..."
python manage.py create_superuser_if_not_exists


# Iniciar Gunicorn
echo "Iniciando Gunicorn..."
exec gunicorn boleto_enriquecido.wsgi:application --bind 0.0.0.0:9000