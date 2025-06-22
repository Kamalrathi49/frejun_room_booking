#!/bin/bash

set -e

echo "Stopping containers..."
docker-compose down -v

docker stop room_booking || true
docker rm room_booking || true

echo "Building services..."
docker-compose build

echo "Starting services..."
docker-compose up -d

echo "Deployment complete!"
echo "server running at: http://localhost:8000"
