#!/bin/bash


DB_CONTAINER_NAME="rental_db"
DB_NAME="equipment_db"
DB_USER="postgres"
DB_PASSWORD="1234"
BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d%H%M%S)

# Создание бэкапа с использованием pg_dump
docker exec -t $DB_CONTAINER_NAME pg_dump -U $DB_USER -d $DB_NAME > $BACKUP_DIR/backup_$TIMESTAMP.sql

# Опционально: удаление старых бэкапов, если необходимо хранить только определенное количество
find $BACKUP_DIR -type f -name 'backup_*' -mtime +7 -exec rm {} \;
