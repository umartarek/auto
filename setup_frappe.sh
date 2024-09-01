#!/bin/bash

# Define the path to the port log file
PORT_FILE="current_port.txt"

# Check if the port file exists; if not, create it with a default port (e.g., 1001)
if [ ! -f $PORT_FILE ]; then
    echo "1000" > $PORT_FILE
fi

# Read the current port from the file
CURRENT_PORT=$(cat $PORT_FILE)

# Increment the port number
NEW_PORT=$((CURRENT_PORT + 1))

# Save the new port back to the file
echo $NEW_PORT > $PORT_FILE

# Export the port as an environment variable
export FRONTEND_PORT=$NEW_PORT

# Log the new port to the console
echo "Updated port to $NEW_PORT"

# Get the site name from the argument
SITE_NAME=$1

# Run the Docker command to set up Frappe
docker compose -p $SITE_NAME -f pwd.yml up -d
# sleep 10
# docker compose -f pwd.yml --project-name $SITE_NAME restart 

# Create a text file to define projects
touch sites/$SITE_NAME.txt
touch sites/$SITE_NAME-date.txt

# Write the port number and timestamp to the text file
echo $NEW_PORT > sites/$SITE_NAME.txt
echo date sites/$SITE_NAME-date.txt
