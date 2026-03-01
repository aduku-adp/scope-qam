#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS_DIR="$ROOT_DIR/tools"
AIRFLOW_IMAGE_NAME="${AIRFLOW_IMAGE_NAME:-scope-qam-airflow:local}"

cd "$ROOT_DIR"
export AIRFLOW_IMAGE_NAME

"$TOOLS_DIR/build_airflow.sh"
"$TOOLS_DIR/build_qam_api.sh"
docker compose down --volumes --remove-orphans
docker compose up


echo "API deployed. UI: http://localhost:8501"
echo "Airflow deployed. UI: http://localhost:8080"
