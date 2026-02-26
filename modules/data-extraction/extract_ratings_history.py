#!/usr/bin/env python3
"""Entrypoint for ratings extraction pipeline."""

from __future__ import annotations

from business_rules import BusinessRuleEngine
from config import AppConfig, ConfigLoader, DbConfig, default_app_config
from excel_extractor import MasterSheetExtractor
from pipeline import RatingsExtractionPipeline
from postgres_repository import PostgresRepository


def parse_env_file(env_path):
    """Backward-compatible helper."""
    return ConfigLoader.parse_env_file(env_path)


def load_db_config(env_path):
    """Backward-compatible helper."""
    return ConfigLoader.load_db_config(env_path)


def ensure_table_and_insert(source_file: str, payload: dict, db_config: DbConfig) -> str | None:
    """Backward-compatible helper used by tests and callers."""
    inserted = PostgresRepository(db_config).insert_rating_assessment(source_file, payload)
    return str(inserted["id"]) if inserted else None


def build_app() -> tuple[RatingsExtractionPipeline, AppConfig]:
    app_config = default_app_config()
    db_config = ConfigLoader.load_db_config(app_config.env_file)
    extractor = MasterSheetExtractor(
        target_sheet_name=app_config.target_sheet_name,
        data_only=app_config.data_only,
    )
    repository = PostgresRepository(db_config)
    business_rules = BusinessRuleEngine(app_config.rules_file)
    pipeline = RatingsExtractionPipeline(
        app_config=app_config,
        extractor=extractor,
        repository=repository,
        business_rules=business_rules,
    )
    return pipeline, app_config


def main() -> None:
    pipeline, _app_config = build_app()
    pipeline.run()


if __name__ == "__main__":
    main()
