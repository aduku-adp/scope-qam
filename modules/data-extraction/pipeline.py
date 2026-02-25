"""Pipeline orchestration for rating extraction."""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from pathlib import Path
from zipfile import BadZipFile

from pydantic import ValidationError

from config import AppConfig
from excel_extractor import MasterSheetExtractor
from pipeline_types import FileProcessLog, PipelineRunMetrics
from postgres_repository import PostgresRepository
from validation_models import validate_extracted_payload


class RatingsExtractionPipeline:
    def __init__(
        self,
        app_config: AppConfig,
        extractor: MasterSheetExtractor,
        repository: PostgresRepository,
    ) -> None:
        self.app_config = app_config
        self.extractor = extractor
        self.repository = repository

    def _discover_incremental_files(self) -> list[Path]:
        data_dir = self.app_config.data_dir.resolve()
        if not data_dir.exists() or not data_dir.is_dir():
            raise FileNotFoundError(f"Data directory not found: {data_dir}")

        candidate_paths = [
            p
            for p in data_dir.iterdir()
            if p.is_file()
            and p.suffix.lower() in self.app_config.excel_extensions
            and not p.name.startswith("~$")
        ]
        if not candidate_paths:
            raise FileNotFoundError(f"No Excel files found in {data_dir}")

        with_modified = [
            (path, self.repository.get_source_modified_at_utc(path)) for path in candidate_paths
        ]
        with_modified.sort(key=lambda item: item[1] or datetime.min.replace(tzinfo=UTC))

        cutoff = self.repository.get_incremental_cutoff()
        if cutoff is None:
            return [path for path, _ in with_modified]

        return [
            path for path, modified_at in with_modified if modified_at is not None and modified_at >= cutoff
        ]

    def run(self) -> None:
        metrics = PipelineRunMetrics(
            run_id=str(uuid.uuid4()),
            started_at=datetime.now(UTC),
        )
        file_logs: list[FileProcessLog] = []

        workbook_paths = self._discover_incremental_files()
        if not workbook_paths:
            print("No files to process for incremental load.")

        for workbook_path in workbook_paths:
            metrics.files_processed += 1
            file_log = FileProcessLog(
                source_file_path=str(workbook_path.resolve()),
                source_filename=workbook_path.name,
                status="pending",
            )

            try:
                raw_payload = self.extractor.extract_workbook(workbook_path)
            except BadZipFile:
                message = f"Skipped invalid Excel file (not a zip workbook): {workbook_path}"
                print(message)
                metrics.rows_skipped += 1
                metrics.extraction_failures += 1
                metrics.errors.append(message)
                file_log.status = "invalid_file"
                file_log.error_message = message
                file_logs.append(file_log)
                continue
            except Exception as exc:
                message = f"Extraction failed for {workbook_path.name}: {exc}"
                print(message)
                metrics.rows_skipped += 1
                metrics.extraction_failures += 1
                metrics.errors.append(message)
                file_log.status = "extraction_failed"
                file_log.error_message = message
                file_logs.append(file_log)
                continue

            try:
                payload = validate_extracted_payload(raw_payload)
            except ValidationError as exc:
                message = f"Validation failed for {workbook_path.name}: {exc.errors()}"
                print(message)
                metrics.rows_skipped += 1
                metrics.validation_failures += 1
                metrics.errors.append(message)
                file_log.status = "validation_failed"
                file_log.error_message = message
                file_logs.append(file_log)
                continue

            try:
                inserted_id = self.repository.insert_rating_assessment(str(workbook_path), payload)
            except Exception as exc:
                message = f"Load failed for {workbook_path.name}: {exc}"
                print(message)
                metrics.rows_skipped += 1
                metrics.load_failures += 1
                metrics.errors.append(message)
                file_log.status = "load_failed"
                file_log.error_message = message
                file_logs.append(file_log)
                continue

            if inserted_id is None:
                message = f"Skipped duplicate (same record_hash) for {workbook_path.name}"
                print(message)
                metrics.rows_skipped += 1
                continue

            metrics.rows_inserted += 1
            file_log.status = "inserted"
            file_logs.append(file_log)
            print(
                f"Inserted row id={inserted_id} into raw.rating_assessments_history for {workbook_path.name}"
            )

        duration_seconds = (datetime.now(UTC) - metrics.started_at).total_seconds()

        try:
            self.repository.insert_run_log(metrics=metrics, duration_seconds=duration_seconds)
        except Exception as exc:
            print(f"Failed to persist run log for run_id={metrics.run_id}: {exc}")

        try:
            self.repository.insert_file_logs(run_id=metrics.run_id, file_logs=file_logs)
        except Exception as exc:
            print(f"Failed to persist file logs for run_id={metrics.run_id}: {exc}")

        run_log_payload = {
            "run_id": metrics.run_id,
            "started_at": metrics.started_at.isoformat(),
            "duration": duration_seconds,
            "files_processed": metrics.files_processed,
            "rows_inserted": metrics.rows_inserted,
            "rows_skipped": metrics.rows_skipped,
            "extraction_failures": metrics.extraction_failures,
            "validation_failures": metrics.validation_failures,
            "load_failures": metrics.load_failures,
            "warnings": len(metrics.warnings),
            "errors": len(metrics.errors),
            "completeness_rate": metrics.completeness_rate(),
            "validity_rate": metrics.validity_rate(),
        }
        print("Run log:")
        print(json.dumps(run_log_payload, indent=2, ensure_ascii=True))
