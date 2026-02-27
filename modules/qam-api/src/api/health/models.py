"""Health response models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class HealthModel(BaseModel):
    """Service health status."""

    healthy: bool = Field(description="Overall service health.")
    database_ok: bool = Field(description="Postgres connectivity check result.")
    corporates_dir_ok: bool = Field(description="Corporate data directory readability check result.")
    corporates_dir_path: str = Field(description="Path checked for corporate files.")
    corporates_files_count: int = Field(description="Number of files discovered in corporates dir.")
    database_message: str = Field(description="Database check details.")
    corporates_dir_message: str = Field(description="Directory check details.")

