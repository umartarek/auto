#!/bin/bash

# Usage: ./migrate.sh <site_name>
SITE_NAME=$1

if [ -z "$SITE_NAME" ]; then
    echo "Site name is required."
    exit 1
fi

echo "Starting migration for site: $SITE_NAME"

# Run migration
docker exec -it $SITE_NAME-backend-1 bench --site frontend migrate

echo "Migration completed for site: $SITE_NAME"
