#!/bin/bash

# Rebuild the image to pick up any Dockerfile changes
echo "Building Docker image..."
docker build -t mkdocs-site .

echo "Starting MkDocs server..."
docker run --rm -it \
    -p 8000:8000 \
    -v $(pwd):/docs \
    mkdocs-site
