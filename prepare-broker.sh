#!/bin/bash

# Check if the script received at least one argument
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <IPv4 address of the VM running the broker> [--no-cache]"
    exit 1
fi

if [ "$1" == "--help" ]; then
    echo "Usage: $0 <IPv4 address of the VM running the broker> [--no-cache]"
    exit 0
fi

IP_ADDRESS=$1
NO_CACHE=""

# Check for the --no-cache parameter
if [ "$#" -eq 2 ] && [ "$2" == "--no-cache" ]; then
    NO_CACHE="--no-cache"
fi

# Validate the IPv4 address format
if [[ ! $IP_ADDRESS =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Invalid IPv4 address format."
    exit 1
fi



# Define the path to the server.properties file
CONFIG_FILE="kafka_2.13-3.9.0/config/kraft/server.properties"

# Check if the config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Config file not found: $CONFIG_FILE"
    exit 1
fi

# Delete the existing advertised.listeners line (if any) and add the new one
sed -i '/^advertised.listeners=/d' "$CONFIG_FILE"
echo "advertised.listeners=PLAINTEXT://$IP_ADDRESS:9092,CONTROLLER://$IP_ADDRESS:9093" >> "$CONFIG_FILE"

# Define the path to the ip.js file
IP_JS_FILE="Backend/Front/ip.js"

# Check if the ip.js file exists
if [ ! -f "$IP_JS_FILE" ]; then
    echo "ip.js file not found: $IP_JS_FILE"
    exit 1
fi

# Delete the existing ip_broker line (if any) and add the new one
sed -i '/^export const ip_broker = /d' "$IP_JS_FILE"
echo "export const ip_broker = \"$IP_ADDRESS\";" >> "$IP_JS_FILE"


# Build the docker-compose
docker-compose build $NO_CACHE

echo "Broker preparation complete."