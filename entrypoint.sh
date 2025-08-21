#!/bin/bash
set -e

# Use variáveis de ambiente ou valores padrão
DB_HOST=${DB_HOST:-host.docker.internal}
DB_PORT=${DB_PORT:-5432}
DB_USER=${DB_USER:-eventos_user}

echo "-> Aguardando pela base de dados em $DB_HOST:$DB_PORT..."

# Espera até o Postgres estar acessível na porta correta
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 2
done

echo "-> Base de dados pronta!"

echo "-> Aplicando migrations (flask db upgrade)..."
flask db upgrade

echo "-> Iniciando Gunicorn"
exec gunicorn -b 0.0.0.0:8000 wsgi:app