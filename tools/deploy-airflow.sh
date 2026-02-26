#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AIRFLOW_IMAGE_NAME="${AIRFLOW_IMAGE_NAME:-scope-qam-airflow:local}"

echo "Deploying Airflow with docker compose using image: $AIRFLOW_IMAGE_NAME"

cd "$ROOT_DIR"
export AIRFLOW_IMAGE_NAME

docker compose up -d

echo "Airflow deployed. UI: http://localhost:8080"
