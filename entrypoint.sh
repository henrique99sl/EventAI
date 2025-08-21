#!/bin/bash
set -e

echo "-> Aguardando pela base de dados em db:5433..."

# Espera até o Postgres estar acessível na porta 5433
until pg_isready -h db -p 5433 -U eventos_user; do
  sleep 2
done

echo "-> Base de dados pronta!"

echo "-> Aplicando migrations (flask db upgrade)..."
flask db upgrade

echo "-> Iniciando Gunicorn"
exec gunicorn -b 0.0.0.0:8000 wsgi:app