#!/bin/bash
set -e

# Configurações
DATE=$(date +"%Y-%m-%d_%H-%M")
BACKUP_DIR="/backups"
FILENAME="eventos_db_backup_$DATE.sql"

# Parâmetros do banco
PGHOST=db
PGPORT=5432
PGUSER=eventos_user
PGPASSWORD=eventos_pass
PGDATABASE=eventos_db

# Garante que a pasta existe
mkdir -p "$BACKUP_DIR"

# Faz o backup
PGPASSWORD=$PGPASSWORD pg_dump -h $PGHOST -p $PGPORT -U $PGUSER $PGDATABASE > "$BACKUP_DIR/$FILENAME"

echo "Backup salvo em $BACKUP_DIR/$FILENAME"