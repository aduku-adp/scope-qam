"""Configuration loading for rating extraction pipeline."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DbConfig:
    host: str
    port: int
    user: str
    password: str
    dbname: str


@dataclass(frozen=True)
class AppConfig:
    project_root: Path
    data_dir: Path
    env_file: Path
    target_sheet_name: str = "MASTER"
    data_only: bool = True
    excel_extensions: tuple[str, ...] = (".xlsm", ".xlsx", ".xltm", ".xltx")


class ConfigLoader:
    @staticmethod
    def parse_env_file(env_path: Path) -> dict[str, str]:
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
    project_root = Path(__file__).resolve().parents[2]
    return AppConfig(
        project_root=project_root,
        data_dir=project_root / "data",
        env_file=project_root / ".env",
    )
