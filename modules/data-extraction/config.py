"""Configuration loading for rating extraction pipeline."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DbConfig:
    """Database connection settings for the extraction pipeline."""

    host: str
    port: int
    user: str
    password: str
    dbname: str


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration for extraction, validation, and file discovery."""

    project_root: Path
    data_dir: Path
    env_file: Path
    rules_file: Path
    target_sheet_name: str = "MASTER"
    data_only: bool = True
    excel_extensions: tuple[str, ...] = (".xlsm", ".xlsx", ".xltm", ".xltx")


class ConfigLoader:
    """Load application and database configuration from env and .env files."""

    @staticmethod
    def parse_env_file(env_path: Path) -> dict[str, str]:
        """Parse key/value pairs from an env file into a dictionary."""
        values: dict[str, str] = {}
        if not env_path.exists():
            return values

        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
        return values

    @classmethod
    def load_db_config(cls, env_path: Path) -> DbConfig:
        """Build a :class:`DbConfig` using env vars first, then .env fallback."""
        file_values = cls.parse_env_file(env_path)

        def get_value(*keys: str, default: str | None = None) -> str:
            for key in keys:
                if os.getenv(key):
                    return os.getenv(key, "")
                if key in file_values:
                    return file_values[key]
            if default is None:
                raise ValueError(
                    f"Missing required DB config. Checked keys: {', '.join(keys)}"
                )
            return default

        return DbConfig(
            host=get_value("PG_HOST", default="postgres"),
            port=int(get_value("PG_PORT", default="5432")),
            user=get_value("PG_USER", default="postgres"),
            password=get_value("PG_PASSWORD", default="postgres"),
            dbname=get_value("DB_NAME", "PG_DATABASE", default="qam_db"),
        )


def default_app_config() -> AppConfig:
    """Return the default app configuration for local and container execution."""
    project_root = Path(__file__).resolve().parents[2]
    return AppConfig(
        project_root=project_root,
        data_dir=project_root / "data" / "corporates",
        env_file=project_root / ".env",
        rules_file=project_root / "modules" / "data-extraction" / "business_rules.yml",
    )
