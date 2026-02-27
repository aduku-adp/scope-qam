"""Health service."""

from __future__ import annotations

import os
from pathlib import Path

import psycopg2

from api.health.models import HealthModel
from helpers.constants import PG_DATABASE, PG_HOST, PG_PASSWORD, PG_PORT, PG_USER


class HealthService:
    """Checks DB connectivity and corporate data directory readability."""

    def __init__(self, corporates_dir: str | None = None):
        self.corporates_dir = corporates_dir or os.environ.get("CORPORATES_DATA_DIR", "/data/corporates")

    def _check_database(self) -> tuple[bool, str]:
        try:
            with psycopg2.connect(
                host=PG_HOST,
                port=PG_PORT,
                dbname=PG_DATABASE,
                user=PG_USER,
                password=PG_PASSWORD,
                connect_timeout=3,
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1;")
                    cur.fetchone()
            return True, "ok"
        except Exception as exc:  # pragma: no cover - exercised by UT via monkeypatch
            return False, str(exc)

    def _check_corporates_dir(self) -> tuple[bool, str, int]:
        path = Path(self.corporates_dir)
        if not path.exists():
            return False, f"directory not found: {path}", 0
        if not path.is_dir():
            return False, f"not a directory: {path}", 0
        if not os.access(path, os.R_OK | os.X_OK):
            return False, f"directory not readable: {path}", 0

        count = sum(1 for item in path.iterdir() if item.is_file() and item.suffix.lower() in {".xlsm", ".xlsx"})
        return True, "ok", count

    def get_health(self) -> HealthModel:
        database_ok, database_message = self._check_database()
        corporates_dir_ok, corporates_dir_message, files_count = self._check_corporates_dir()
        return HealthModel(
            healthy=database_ok and corporates_dir_ok,
            database_ok=database_ok,
            corporates_dir_ok=corporates_dir_ok,
            corporates_dir_path=self.corporates_dir,
            corporates_files_count=files_count,
            database_message=database_message,
            corporates_dir_message=corporates_dir_message,
        )

