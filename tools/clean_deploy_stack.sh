#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS_DIR="$ROOT_DIR/tools"
AIRFLOW_IMAGE_NAME="${AIRFLOW_IMAGE_NAME:-scope-qam-airflow:local}"

cd "$ROOT_DIR"
export AIRFLOW_IMAGE_NAME

# Build airflow image
echo "Build airflow image"
"$TOOLS_DIR/build_airflow.sh"

# Build qam-api image
echo "Build qam-api image"
"$TOOLS_DIR/build_qam_api.sh"

# Clean the stack
echo "Clean the stack"
docker compose down --volumes --remove-orphans
rm -rf "$ROOT_DIR/data/pg_data_qam"
mkdir "$ROOT_DIR/data/pg_data_qam"


# Initialize airflow
echo "Initialize airflow"
docker compose up airflow-init
docker compose down --volumes --remove-orphans

# Depoy the stack
echo "Depoy the stack"
docker compose up -d

echo "API deployed. UI: http://localhost:8501"
echo "Airflow deployed. UI: http://localhost:8080"
