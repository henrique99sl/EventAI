#!/bin/bash
BACKUP_FILE="$1"
DB_NAME="eventos_db"
DB_USER="eventos_user"

if [ -z "$BACKUP_FILE" ]; then
  echo "Uso: $0 /caminho/backup.sql"
  exit 1
fi

# Drop banco atual e recrie
docker-compose exec db psql -U $DB_USER -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"
docker-compose exec db psql -U $DB_USER -d postgres -c "CREATE DATABASE $DB_NAME;"

# Restaura backup
docker-compose exec -T db psql -U $DB_USER -d $DB_NAME < "$BACKUP_FILE"

# Testa se os dados voltaram (exemplo: conta usuários)
docker-compose exec db psql -U $DB_USER -d $DB_NAME -c "SELECT COUNT(*) AS total_usuarios FROM users;"