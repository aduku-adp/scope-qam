"""Upload audit response models."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class UploadModel(BaseModel):
    """Upload metadata model."""

    upload_id: str = Field(description="Upload event identifier.", examples=["uuid"])
    run_id: str | None = Field(default=None, description="Pipeline run identifier.")
    pipeline_name: str | None = Field(default=None)
    source_file_path: str | None = Field(default=None)
    source_filename: str | None = Field(default=None)
    source_modified_at_utc: datetime | None = Field(default=None)
    file_size_bytes: int | None = Field(default=None)
    file_hash: str | None = Field(default=None)
    record_hash: str | None = Field(default=None)
    document_version: int | None = Field(default=None)
    status: str | None = Field(default=None)
    warning_count: int | None = Field(default=None)
    error_count: int | None = Field(default=None)
    warning_message: str | None = Field(default=None)
    error_message: str | None = Field(default=None)
    ingested_at: datetime | None = Field(default=None)


class UploadDetailsModel(BaseModel):
    """Upload details with quality and lineage traces."""

    upload: UploadModel
    data_quality_results: list[dict[str, Any]] = Field(default_factory=list)
    lineage_events: list[dict[str, Any]] = Field(default_factory=list)


class UploadStatsModel(BaseModel):
    """Upload statistics and metrics."""

    total_uploads: int
    successful_uploads: int
    failed_uploads: int
    total_warnings: int
    total_errors: int
    avg_file_size_bytes: float | None = None
    latest_upload_at: datetime | None = None
    uploads_by_status: dict[str, int] = Field(default_factory=dict)

