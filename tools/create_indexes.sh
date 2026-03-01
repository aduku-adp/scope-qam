#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SQL_DIR="$ROOT_DIR/tools/sql/indexes"
ENV_FILE="$ROOT_DIR/.env"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

PG_HOST="${PG_HOST:-localhost}"
PG_PORT="${PG_PORT:-5432}"
PG_USER="${PG_USER:-postgres}"
PG_PASSWORD="${PG_PASSWORD:-postgres}"
DB_NAME="${DB_NAME:-qam_db}"

if ! command -v psql >/dev/null 2>&1; then
  echo "Error: psql command not found. Install PostgreSQL client tools first."
  exit 1
fi

if [[ ! -d "$SQL_DIR" ]]; then
  echo "Error: SQL directory not found: $SQL_DIR"
  exit 1
fi

mapfile -t SQL_FILES < <(find "$SQL_DIR" -maxdepth 1 -type f -name "*.sql" | sort)

if [[ ${#SQL_FILES[@]} -eq 0 ]]; then
  echo "No SQL files found in $SQL_DIR"
  exit 0
fi

export PGPASSWORD="$PG_PASSWORD"

echo "Applying index scripts to $DB_NAME on $PG_HOST:$PG_PORT as $PG_USER"
for sql_file in "${SQL_FILES[@]}"; do
  echo "Running: $sql_file"
  psql \
    --host "$PG_HOST" \
    --port "$PG_PORT" \
    --username "$PG_USER" \
    --dbname "$DB_NAME" \
    --set ON_ERROR_STOP=1 \
    --file "$sql_file"
done

echo "Completed index script execution."
