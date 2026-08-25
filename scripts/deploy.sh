#!/bin/bash

# Build and push Docker images to registry
# Usage: ./scripts/deploy.sh <registry_url> <version>

REGISTRY=${1:-}
VERSION=${2:-latest}

if [ -z "$REGISTRY" ]; then
  echo "Usage: ./scripts/deploy.sh <registry_url> <version>"
  echo "Example: ./scripts/deploy.sh docker.io/username v1.0.0"
  exit 1
fi

echo "Building and pushing Docker images..."

# Backend
echo "Building backend..."
docker build -t $REGISTRY/ai-social-media-backend:$VERSION ./backend
docker push $REGISTRY/ai-social-media-backend:$VERSION

# Frontend
echo "Building frontend..."
docker build -t $REGISTRY/ai-social-media-frontend:$VERSION ./frontend
docker push $REGISTRY/ai-social-media-frontend:$VERSION

echo "Build and push complete!"
echo "Images:"
echo "  - $REGISTRY/ai-social-media-backend:$VERSION"
echo "  - $REGISTRY/ai-social-media-frontend:$VERSION"
