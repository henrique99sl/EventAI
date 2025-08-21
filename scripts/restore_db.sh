#!/bin/bash
# Caminho do backup passado como argumento
BACKUP_FILE="$1"

if [ -z "$BACKUP_FILE" ]; then
  echo "Uso: $0 /caminho/do/backup.sql"
  exit 1
fi

docker-compose exec -T db psql -U eventos_user -d eventos_db < "$BACKUP_FILE"