#!/bin/bash

# Usage: ./install_apps.sh <container_name> <site_name> <app1> <app2> ...
CONTAINER_NAME=$1
SITE_NAME=$2
shift 2
APPS="$@"

if [ -z "$SITE_NAME" ] || [ -z "$APPS" ]; then
    echo "Site name and at least one app name are required."
    exit 1
fi

echo "Installing apps for site: $SITE_NAME"

# Install apps
docker exec -it $SITE_NAME-backend-1 bench --site frontend install-app $APPS

echo "Apps installed for site: $SITE_NAME"
