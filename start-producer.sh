# Check if the first parameter is provided and is a valid IP address
if [[ -z "$1" || ! "$1" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Usage: $0 <BROKER_IP>"
    exit 1
fi

# Set the BROKER_IP variable
BROKER_IP="$1"

# Run the Docker container
docker run --rm -e KAFKA_BROKER_IP="$BROKER_IP" --name producer kafka-producer