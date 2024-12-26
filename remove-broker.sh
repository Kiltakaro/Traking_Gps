#!/bin/bash

# Check if the -v option is provided
if [ "$1" == "-v" ]; then
    echo "Stopping containers and removing volumes..."
    docker-compose down -v
else
    echo "Stopping containers..."
    docker-compose down
fi