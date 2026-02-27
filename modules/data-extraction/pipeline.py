"""Pipeline orchestration for rating extraction."""

from __future__ import annotations

import hashlib
import json
import random
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path
from zipfile import BadZipFile

from pydantic import ValidationError

from business_rules import BusinessRuleEngine
from config import AppConfig
from excel_extractor import MasterSheetExtractor
from pipeline_types import FileProcessLog, PipelineRunMetrics
from postgres_repository import PostgresRepository
from validation_models import validate_extracted_payload

try:  # pragma: no cover - import fallback for tests without psycopg2 installed.
    from psycopg2 import InterfaceError as PgInterfaceError
    from psycopg2 import OperationalError as PgOperationalError
except Exception:  # pragma: no cover
    PgOperationalError = RuntimeError  # type: ignore[assignment]
    PgInterfaceError = ConnectionError  # type: ignore[assignment]


class CompanyExtractionPipeline:
    def __init__(
        self,
        app_config: AppConfig,
        extractor: MasterSheetExtractor,
        repository: PostgresRepository,
        business_rules: BusinessRuleEngine | None = None,
    ) -> None:
        self.app_config = app_config
        self.extractor = extractor
        self.repository = repository
        self.business_rules = business_rules
        self.pipeline_name = "extract_company_history"
        self.retry_attempts = 4
        self.retry_base_seconds = 1.0
        self.retry_max_seconds = 8.0

    def _with_retry(self, operation_name: str, func, *args, **kwargs):
        """Retry transient failures with exponential backoff + jitter."""
        transient_exceptions = (
            PgOperationalError,
            PgInterfaceError,
            ConnectionError,
            TimeoutError,
        )
        attempt = 0
        while True:
            try:
                return func(*args, **kwargs)
            except transient_exceptions as exc:
                attempt += 1
                if attempt >= self.retry_attempts:
                    raise
                base = min(self.retry_base_seconds * (2 ** (attempt - 1)), self.retry_max_seconds)
                jitter = random.uniform(0.0, 0.25)
                sleep_for = base + jitter
                print(
                    f"{operation_name} transient failure (attempt {attempt}/{self.retry_attempts - 1}): "
                    f"{exc}. Retrying in {sleep_for:.2f}s."
                )
                time.sleep(sleep_for)

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

        raw_cutoff = self._with_retry("get_incremental_cutoff", self.repository.get_incremental_cutoff)
        state_cutoff = self._with_retry(
            "get_pipeline_state_cutoff",
            self.repository.get_pipeline_state_cutoff,
            self.pipeline_name,
        )

        # If raw is empty, force full reload from DATA_DIR even if pipeline_state exists.
        if raw_cutoff is None:
            return [path for path, _ in with_modified]

        cutoff = max(raw_cutoff, state_cutoff) if state_cutoff is not None else raw_cutoff

        return [
            path for path, modified_at in with_modified if modified_at is not None and modified_at >= cutoff
        ]

    def _file_hash(self, path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def run(self) -> None:
        metrics = PipelineRunMetrics(
            run_id=str(uuid.uuid4()),
            started_at=datetime.now(UTC),
        )
        file_logs: list[FileProcessLog] = []
        max_processed_modified_at: datetime | None = None

        try:
            self._with_retry(
                "ensure_rating_assessments_schema",
                self.repository.ensure_rating_assessments_schema,
            )
            self._with_retry("ensure_observability_schema", self.repository.ensure_observability_schema)
            self._with_retry(
                "insert_pipeline_run_start",
                self.repository.insert_pipeline_run_start,
                run_id=metrics.run_id,
                pipeline_name=self.pipeline_name,
                started_at=metrics.started_at,
            )
        except Exception as exc:
            message = f"Schema/backfill step failed: {exc}"
            print(message)
            metrics.errors.append(message)

        workbook_paths = self._discover_incremental_files()
        files_discovered = len(workbook_paths)
        if not workbook_paths:
            print("No files to process for incremental load.")

        for workbook_path in workbook_paths:
            metrics.files_processed += 1
            source_file_path = str(workbook_path.resolve())
            source_modified_at = self.repository.get_source_modified_at_utc(workbook_path)
            if source_modified_at and (
                max_processed_modified_at is None or source_modified_at > max_processed_modified_at
            ):
                max_processed_modified_at = source_modified_at

            file_size = workbook_path.stat().st_size if workbook_path.exists() else None
            file_hash = self._file_hash(workbook_path)

            file_log = FileProcessLog(
                source_file_path=source_file_path,
                source_filename=workbook_path.name,
                status="pending",
            )

            try:
                raw_payload = self._with_retry(
                    "extract_workbook",
                    self.extractor.extract_workbook,
                    workbook_path,
                )
            except BadZipFile:
                message = f"Skipped invalid Excel file (not a zip workbook): {workbook_path}"
                print(message)
                metrics.rows_skipped += 1
                metrics.extraction_failures += 1
                metrics.errors.append(message)
                file_log.status = "invalid_file"
                file_log.error_message = message
                file_logs.append(file_log)
                event_id = self.repository.insert_file_ingestion_event(
                    metrics.run_id,
                    source_file_path=source_file_path,
                    source_filename=workbook_path.name,
                    source_modified_at_utc=source_modified_at,
                    file_size_bytes=file_size,
                    file_hash=file_hash,
                    record_hash=None,
                    document_version=None,
                    status=file_log.status,
                    warning_message=None,
                    error_message=message,
                )
                self.repository.insert_data_quality_results(
                    metrics.run_id,
                    event_id,
                    "file",
                    [],
                    details={"type": "extraction_error", "message": message},
                )
                self.repository.upsert_processed_file(
                    metrics.run_id, source_file_path, source_modified_at, file_hash, file_log.status
                )
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
                event_id = self.repository.insert_file_ingestion_event(
                    metrics.run_id,
                    source_file_path=source_file_path,
                    source_filename=workbook_path.name,
                    source_modified_at_utc=source_modified_at,
                    file_size_bytes=file_size,
                    file_hash=file_hash,
                    record_hash=None,
                    document_version=None,
                    status=file_log.status,
                    warning_message=None,
                    error_message=message,
                )
                self.repository.insert_data_quality_results(
                    metrics.run_id,
                    event_id,
                    "file",
                    [],
                    details={"type": "extraction_error", "message": message},
                )
                self.repository.upsert_processed_file(
                    metrics.run_id, source_file_path, source_modified_at, file_hash, file_log.status
                )
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
                event_id = self.repository.insert_file_ingestion_event(
                    metrics.run_id,
                    source_file_path=source_file_path,
                    source_filename=workbook_path.name,
                    source_modified_at_utc=source_modified_at,
                    file_size_bytes=file_size,
                    file_hash=file_hash,
                    record_hash=None,
                    document_version=None,
                    status=file_log.status,
                    warning_message=None,
                    error_message=message,
                )
                self.repository.insert_data_quality_results(
                    metrics.run_id,
                    event_id,
                    "file",
                    [],
                    details={"type": "schema_validation_error", "errors": exc.errors()},
                )
                self.repository.upsert_processed_file(
                    metrics.run_id, source_file_path, source_modified_at, file_hash, file_log.status
                )
                continue

            rule_outcomes = []
            if self.business_rules is not None:
                rule_outcomes = self.business_rules.evaluate_payload(payload)
                rule_errors = [o.message for o in rule_outcomes if o.status == "fail"]
                rule_warnings = [o.message for o in rule_outcomes if o.status == "warn"]

                if rule_warnings:
                    metrics.warnings.extend(rule_warnings)
                    file_log.warning_message = " | ".join(rule_warnings)

                if rule_errors:
                    message = (
                        f"Business-rule validation failed for {workbook_path.name}: "
                        f"{' | '.join(rule_errors)}"
                    )
                    print(message)
                    metrics.rows_skipped += 1
                    metrics.validation_failures += 1
                    metrics.errors.append(message)
                    file_log.status = "validation_failed"
                    file_log.error_message = message
                    file_logs.append(file_log)
                    event_id = self.repository.insert_file_ingestion_event(
                        metrics.run_id,
                        source_file_path=source_file_path,
                        source_filename=workbook_path.name,
                        source_modified_at_utc=source_modified_at,
                        file_size_bytes=file_size,
                        file_hash=file_hash,
                        record_hash=None,
                        document_version=None,
                        status=file_log.status,
                        warning_message=file_log.warning_message,
                        error_message=message,
                    )
                    self.repository.insert_data_quality_results(
                        metrics.run_id, event_id, "file", rule_outcomes
                    )
                    self.repository.upsert_processed_file(
                        metrics.run_id, source_file_path, source_modified_at, file_hash, file_log.status
                    )
                    continue

            try:
                inserted = self._with_retry(
                    "insert_rating_assessment",
                    self.repository.insert_rating_assessment,
                    str(workbook_path),
                    payload,
                )
            except Exception as exc:
                message = f"Load failed for {workbook_path.name}: {exc}"
                print(message)
                metrics.rows_skipped += 1
                metrics.load_failures += 1
                metrics.errors.append(message)
                file_log.status = "load_failed"
                file_log.error_message = message
                file_logs.append(file_log)
                event_id = self.repository.insert_file_ingestion_event(
                    metrics.run_id,
                    source_file_path=source_file_path,
                    source_filename=workbook_path.name,
                    source_modified_at_utc=source_modified_at,
                    file_size_bytes=file_size,
                    file_hash=file_hash,
                    record_hash=None,
                    document_version=None,
                    status=file_log.status,
                    warning_message=file_log.warning_message,
                    error_message=message,
                )
                self.repository.insert_data_quality_results(
                    metrics.run_id,
                    event_id,
                    "file",
                    rule_outcomes,
                    details={"type": "load_error", "message": message},
                )
                self.repository.upsert_processed_file(
                    metrics.run_id, source_file_path, source_modified_at, file_hash, file_log.status
                )
                continue

            if inserted is None:
                message = f"Skipped duplicate (same record_hash) for {workbook_path.name}"
                print(message)
                metrics.rows_skipped += 1
                self.repository.upsert_processed_file(
                    metrics.run_id, source_file_path, source_modified_at, file_hash, "skipped_duplicate"
                )
                continue

            metrics.rows_inserted += 1
            file_log.status = "inserted"
            file_logs.append(file_log)

            event_id = self.repository.insert_file_ingestion_event(
                metrics.run_id,
                source_file_path=source_file_path,
                source_filename=workbook_path.name,
                source_modified_at_utc=source_modified_at,
                file_size_bytes=file_size,
                file_hash=file_hash,
                record_hash=inserted.get("record_hash"),
                document_version=inserted.get("document_version"),
                status=file_log.status,
                warning_message=file_log.warning_message,
                error_message=None,
            )
            self.repository.insert_data_quality_results(
                metrics.run_id, event_id, "file", rule_outcomes
            )
            canonical_payload = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
            self.repository.insert_lineage_event(
                metrics.run_id,
                event_id,
                source_file_path,
                hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest(),
                inserted.get("id"),
                inserted.get("record_hash"),
            )
            self.repository.upsert_processed_file(
                metrics.run_id, source_file_path, source_modified_at, file_hash, file_log.status
            )
            print(
                f"Inserted row id={inserted.get('id')} into raw.rating_assessments_history "
                f"for {workbook_path.name}"
            )

        duration_seconds = (datetime.now(UTC) - metrics.started_at).total_seconds()
        run_status = "success" if len(metrics.errors) == 0 else "failed"

        try:
            self.repository.update_pipeline_run_end(
                run_id=metrics.run_id,
                metrics=metrics,
                duration_seconds=duration_seconds,
                files_discovered=files_discovered,
                status=run_status,
            )
            self.repository.upsert_pipeline_state(
                pipeline_name=self.pipeline_name,
                run_id=metrics.run_id,
                last_successful_run_at=datetime.now(UTC) if run_status == "success" else None,
                max_source_modified_at_utc=max_processed_modified_at,
                processed_files_count_increment=metrics.files_processed,
            )
        except Exception as exc:
            print(f"Failed to persist observability state for run_id={metrics.run_id}: {exc}")

        pipeline_run_event = {
            "run_id": metrics.run_id,
            "pipeline_name": self.pipeline_name,
            "started_at": metrics.started_at.isoformat(),
            "duration": duration_seconds,
            "files_discovered": files_discovered,
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
            "status": run_status,
        }
        print("Pipeline run event (obs.pipeline_runs):")
        print(json.dumps(pipeline_run_event, indent=2, ensure_ascii=True))
