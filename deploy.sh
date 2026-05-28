#!/bin/bash

echo "🚀 Pulling latest image..."
docker pull abhinav0824/mywebapp:latest

echo "🛑 Stopping old container..."
docker stop mywebapp-container || true

echo "🗑️ Removing old container..."
docker rm mywebapp-container || true

echo "🚀 Starting new container..."
docker run -d \
  --name mywebapp-container \
  -p 8000:8000 \
  --env-file .env \
  --restart always \
  abhinav0824/mywebapp:latest

echo "✅ Deployment complete!"
