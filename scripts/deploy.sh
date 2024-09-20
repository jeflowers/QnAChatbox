#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Check if NVIDIA_API_KEY is set
if [ -z "$NVIDIA_API_KEY" ]; then
    echo "Error: NVIDIA_API_KEY is not set. Please set it in your .env file or export it."
    exit 1
fi

# Build the Docker image
echo "Building Docker image..."
docker build -t nvidia-rag-qa-chat .

# Stop the existing container if it's running
echo "Stopping existing container (if any)..."
docker stop nvidia-rag-qa-chat-container 2>/dev/null || true
docker rm nvidia-rag-qa-chat-container 2>/dev/null || true

# Run the new container
echo "Starting new container..."
docker run -d --name nvidia-rag-qa-chat-container -p 7860:7860 -e NVIDIA_API_KEY=$NVIDIA_API_KEY nvidia-rag-qa-chat

echo "Deployment complete. Application should be accessible at http://localhost:7860"