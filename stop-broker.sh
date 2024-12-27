#!/bin/bash

# Check if the --help option is provided
if [ "$1" == "--help" ]; then
    echo "Usage: $0 [-v] [--help]"
    echo "  -v      Remove volumes"
    echo "  --help  Display this help message"
    exit 0
fi
# Check if the -v option is provided
if [ "$1" == "-v" ]; then
    echo "Stopping containers and removing volumes..."
    docker-compose down -v
else
    echo "Stopping containers..."
    docker-compose down
fi