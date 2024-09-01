#!/bin/bash

# Usage: ./clear_cache.sh <site_name>
SITE_NAME=$1

if [ -z "$SITE_NAME" ]; then
    echo "Site name is required."
    exit 1
fi

echo "Clearing cache for site: $SITE_NAME"

# Clear cache
docker exec -it $SITE_NAME-backend-1 bench --site frontend clear-cache

echo "Cache cleared for site: $SITE_NAME"
