#!/bin/bash

# Usage: ./backup.sh <site_name>
SITE_NAME=$1

if [ -z "$SITE_NAME" ]; then
    echo "Site name is required."
    exit 1
fi

echo "Starting backup for site: $SITE_NAME"

# Create backup directory if it doesn't exist
BACKUP_DIR="backups"
mkdir -p $BACKUP_DIR

# Run backup
docker exec -it $SITE_NAME-backend-1 bench --site frontend backup --with-files

# Move backup to the backups directory
docker cp frappe_app:/home/frappe/frappe-bench/sites/$SITE_NAME/private/backups $BACKUP_DIR/

echo "Backup completed for site: $SITE_NAME"
