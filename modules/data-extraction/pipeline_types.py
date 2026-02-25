"""Shared types for pipeline orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class FileProcessLog:
    source_file_path: str
    source_filename: str
    status: str
    warning_message: str | None = None
    error_message: str | None = None


@dataclass
class PipelineRunMetrics:
    run_id: str
    started_at: datetime
    files_processed: int = 0
    rows_inserted: int = 0
    rows_skipped: int = 0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    extraction_failures: int = 0
    validation_failures: int = 0
    load_failures: int = 0

    def completeness_rate(self) -> float:
        if self.files_processed <= 0:
            return 0.0
        return round(
            (self.files_processed - self.validation_failures) / self.files_processed,
            4,
        )

    def validity_rate(self) -> float:
        if self.files_processed <= 0:
            return 0.0
        failed = self.extraction_failures + self.validation_failures + self.load_failures
        return round((self.files_processed - failed) / self.files_processed, 4)
