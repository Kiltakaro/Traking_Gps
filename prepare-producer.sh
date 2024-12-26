#!/bin/bash

show_help() {
    echo "Usage: $0 [option]"
    echo "Options:"
    echo "  --help        Show this help message"
    echo "  1             prepare producer1 in the producer1 VM"
    echo "  2             prepare producer2 in the producer2 VM"
}

prepare_producer1() {
    echo "preparing producer1..."
    docker build -t kafka-producer Producer/producer1/
}

prepare_producer2() {
    echo "preparing producer2..."
    docker build -t kafka-producer Producer/producer2/
}

if [ "$1" == "--help" ]; then
    show_help
elif [ "$1" == "1" ]; then
    prepare_producer1
elif [ "$1" == "2" ]; then
    prepare_producer2
else
    echo "Invalid option. Use --help for usage information."
    exit 1
fi