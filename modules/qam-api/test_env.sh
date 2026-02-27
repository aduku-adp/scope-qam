#!/usr/bin/env bash

export SERVICE_URL="${SERVICE_URL:-http://localhost:8000}"
export IDENTITY="${IDENTITY:-local-test-identity}"

export PG_HOST="${PG_HOST:-localhost}"
export PG_PORT="${PG_PORT:-5432}"
export PG_USER="${PG_USER:-postgres}"
export PG_PASSWORD="${PG_PASSWORD:-postgres}"
export DB_NAME="${DB_NAME:-qam_db}"
