#!/bin/bash
if [[ "$1" == "--help" ]]; then
    echo "Usage: start-broker.sh [--help]"
    echo ""
    echo "Options:"
    echo "  --help    Show this help message"
    exit 0
fi
# Start the broker using docker-compose
docker-compose up