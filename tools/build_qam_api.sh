#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGE_NAME="${QAM_API_IMAGE_NAME:-scope-qam-api:local}"
DOCKERFILE_PATH="${DOCKERFILE_PATH:-$ROOT_DIR/modules/qam-api/Dockerfile}"
BUILD_CONTEXT="${BUILD_CONTEXT:-$ROOT_DIR/modules/qam-api}"

echo "Building qam-api image:"
echo "  image      : $IMAGE_NAME"
echo "  dockerfile : $DOCKERFILE_PATH"
echo "  context    : $BUILD_CONTEXT"

docker build \
  -f "$DOCKERFILE_PATH" \
  -t "$IMAGE_NAME" \
  "$BUILD_CONTEXT"

echo "Built image $IMAGE_NAME"

docker compose up  qam-api -d
