#!/bin/bash

# Stop the producer container
if [[ $1 == "--help" ]]; then
    echo "Usage: stop-producer.sh"
    echo ""
    echo "Stops the producer container."
    exit 0
fi
docker stop producer