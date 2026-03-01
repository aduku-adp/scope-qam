"""Postgres persistence and incremental-read operations."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path

import psycopg2
from psycopg2.extras import Json

from config import DbConfig
from business_rules import RuleOutcome
from pipeline_types import FileProcessLog, PipelineRunMetrics


class PostgresRepository:
    """Repository for raw ingestion, observability, and pipeline state in Postgres."""

    def __init__(self, db_config: DbConfig) -> None:
        """Instantiate repository with database connectivity settings."""
        self.db_config = db_config

    def _conn_str(self) -> str:
        """Build a psycopg2 DSN string from :class:`DbConfig`."""
        return (
            f"host={self.db_config.host} "
            f"port={self.db_config.port} "
            f"dbname={self.db_config.dbname} "
            f"user={self.db_config.user} "
            f"password={self.db_config.password}"
        )

    @staticmethod
    def build_source_file_fields(source_file: str | Path) -> tuple[str, str | None]:
        """Return absolute source path and UTC modified timestamp as ISO text."""
        source_path = Path(source_file).resolve()
        source_modified_at_utc: str | None = None
        try:
            stats = source_path.stat()
            source_modified_at_utc = datetime.fromtimestamp(stats.st_mtime, tz=UTC).isoformat()
        except FileNotFoundError:
            pass
        return str(source_path), source_modified_at_utc

    @staticmethod
    def get_source_modified_at_utc(source_file: str | Path) -> datetime | None:
        """Return UTC last-modified timestamp for a source file, if available."""
        source_path = Path(source_file).resolve()
        try:
            stats = source_path.stat()
            return datetime.fromtimestamp(stats.st_mtime, tz=UTC)
        except FileNotFoundError:
            return None

    @staticmethod
    def build_company_id(company_name: str | None) -> str:
        """Normalize company name into a stable snake_case business identifier."""
        base = (company_name or "").strip().lower()
        normalized = re.sub(r"[^a-z0-9]+", "_", base)
        normalized = re.sub(r"_+", "_", normalized).strip("_")
        return normalized or "unknown_company"

    def get_incremental_cutoff(self) -> datetime | None:
        """Read the max source timestamp from raw history for incremental loads."""
        sql = "SELECT MAX(source_modified_at_utc) FROM raw.rating_assessments_history;"
        try:
            with psycopg2.connect(self._conn_str()) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    row = cur.fetchone()
                    return row[0] if row and row[0] is not None else None
        except psycopg2.Error as exc:
            if getattr(exc, "pgcode", None) == "42P01":
                return None
            raise

    def get_pipeline_state_cutoff(self, pipeline_name: str) -> datetime | None:
        """Read persisted incremental cutoff from `obs.pipeline_state`."""
        sql = """
        SELECT max_source_modified_at_utc
        FROM obs.pipeline_state
        WHERE pipeline_name = %s;
        """
        try:
            with psycopg2.connect(self._conn_str()) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (pipeline_name,))
                    row = cur.fetchone()
                    return row[0] if row and row[0] is not None else None
        except psycopg2.Error as exc:
            if getattr(exc, "pgcode", None) in {"42P01", "3F000"}:
                return None
            raise

    def _ensure_rating_assessments_schema(self, cur) -> None:
        """Create and evolve `raw.rating_assessments_history` and related indexes."""
        def _column_data_type(column_name: str) -> str | None:
            cur.execute(
                """
                SELECT data_type
                FROM information_schema.columns
                WHERE table_schema = 'raw'
                  AND table_name = 'rating_assessments_history'
                  AND column_name = %s;
                """,
                (column_name,),
            )
            row = cur.fetchone()
            return row[0] if row else None

        cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
        cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS raw.rating_assessments_history (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                record_hash TEXT NOT NULL UNIQUE,
                company_information JSONB NOT NULL,
                methodology JSONB NOT NULL,
                industry_risk JSONB NOT NULL,
                business_risk_profile JSONB NOT NULL,
                financial_risk_profile JSONB NOT NULL,
                credit_metrics JSONB NOT NULL,
                extracted_payload JSONB NOT NULL,
                company_id TEXT NOT NULL,
                document_version INTEGER NOT NULL,
                company_name TEXT NOT NULL,
                country TEXT,
                corporate_sector TEXT,
                segmentation_criteria TEXT,
                business_risk_score TEXT,
                financial_risk_score TEXT,
                source_file_path TEXT,
                source_modified_at_utc TIMESTAMPTZ,
                ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                UNIQUE (company_id, document_version)
            );
            """
        )

        for statement in [
            "ALTER TABLE raw.rating_assessments_history ADD COLUMN IF NOT EXISTS company_information JSONB;",
            "ALTER TABLE raw.rating_assessments_history ADD COLUMN IF NOT EXISTS extracted_payload JSONB;",
            "ALTER TABLE raw.rating_assessments_history DROP COLUMN IF EXISTS file_metadata;",
            "ALTER TABLE raw.rating_assessments_history DROP COLUMN IF EXISTS source_system;",
            "ALTER TABLE raw.rating_assessments_history ADD COLUMN IF NOT EXISTS document_version INTEGER;",
            "ALTER TABLE raw.rating_assessments_history ADD COLUMN IF NOT EXISTS company_name TEXT;",
            "ALTER TABLE raw.rating_assessments_history ADD COLUMN IF NOT EXISTS company_id TEXT;",
            "ALTER TABLE raw.rating_assessments_history ADD COLUMN IF NOT EXISTS corporate_sector TEXT;",
            "ALTER TABLE raw.rating_assessments_history ADD COLUMN IF NOT EXISTS segmentation_criteria TEXT;",
            "ALTER TABLE raw.rating_assessments_history DROP COLUMN IF EXISTS industry;",
            "CREATE UNIQUE INDEX IF NOT EXISTS uq_rating_assessments_history_company_version ON raw.rating_assessments_history (company_id, document_version);",
            "ALTER TABLE raw.rating_assessments_history ADD COLUMN IF NOT EXISTS source_file_path TEXT;",
            "ALTER TABLE raw.rating_assessments_history ADD COLUMN IF NOT EXISTS source_modified_at_utc TIMESTAMPTZ;",
            "ALTER TABLE raw.rating_assessments_history DROP COLUMN IF EXISTS extracted_at;",
            "ALTER TABLE raw.rating_assessments_history DROP COLUMN IF EXISTS rating_date;",
            "CREATE INDEX IF NOT EXISTS idx_rating_assessments_history_source_modified_at ON raw.rating_assessments_history (source_modified_at_utc DESC);",
            "CREATE INDEX IF NOT EXISTS idx_rating_assessments_history_company_source_modified ON raw.rating_assessments_history (company_id, source_modified_at_utc DESC);",
            "CREATE INDEX IF NOT EXISTS idx_rating_assessments_history_source_file_path ON raw.rating_assessments_history (source_file_path);",
            "CREATE INDEX IF NOT EXISTS idx_rating_assessments_history_ingested_at ON raw.rating_assessments_history (ingested_at DESC);",
        ]:
            cur.execute(statement)
        cur.execute(
            """
            ALTER TABLE raw.rating_assessments_history
            DROP CONSTRAINT IF EXISTS rating_assessments_history_company_key_document_version_key;
            """
        )
        cur.execute(
            """
            ALTER TABLE raw.rating_assessments_history
            DROP CONSTRAINT IF EXISTS rating_assessments_history_company_id_document_version_key;
            """
        )
        cur.execute(
            """
            ALTER TABLE raw.rating_assessments_history
            ADD CONSTRAINT rating_assessments_history_company_id_document_version_key
            UNIQUE (company_id, document_version);
            """
        )

        jsonb_columns = [
            "company_information",
            "methodology",
            "industry_risk",
            "business_risk_profile",
            "financial_risk_profile",
            "credit_metrics",
        ]
        for column_name in jsonb_columns:
            data_type = _column_data_type(column_name)
            if data_type is None:
                continue
            if data_type.lower() == "jsonb":
                continue
            cur.execute(
                f"""
                ALTER TABLE raw.rating_assessments_history
                ALTER COLUMN {column_name} TYPE JSONB
                USING {column_name}::jsonb;
                """
            )

        cur.execute(
            """
            UPDATE raw.rating_assessments_history
            SET segmentation_criteria = COALESCE(
                segmentation_criteria,
                company_information ->> 'segmentation_criteria',
                CASE
                    WHEN jsonb_typeof(industry_risk) = 'object'
                        THEN industry_risk ->> 'segmentation_criteria'
                    ELSE NULL
                END
            )
            WHERE segmentation_criteria IS NULL
              AND (
                  company_information ? 'segmentation_criteria'
                  OR (
                      jsonb_typeof(industry_risk) = 'object'
                      AND industry_risk ? 'segmentation_criteria'
                  )
              );
            """
        )
        cur.execute(
            """
            UPDATE raw.rating_assessments_history
            SET company_id = nullif(
                btrim(lower(regexp_replace(company_name, '[^a-zA-Z0-9]+', '_', 'g')), '_'),
                ''
            )
            WHERE (company_id IS NULL OR company_id = '')
              AND company_name IS NOT NULL;
            """
        )
        cur.execute(
            """
            UPDATE raw.rating_assessments_history
            SET company_information = jsonb_set(
                company_information,
                '{segmentation_criteria}',
                to_jsonb(segmentation_criteria),
                true
            )
            WHERE segmentation_criteria IS NOT NULL
              AND NOT (company_information ? 'segmentation_criteria');
            """
        )

    def _ensure_observability_schema(self, cur) -> None:
        """Create and evolve observability tables and performance indexes."""
        cur.execute("CREATE SCHEMA IF NOT EXISTS obs;")
        cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS obs.pipeline_runs (
                run_id UUID PRIMARY KEY,
                pipeline_name TEXT NOT NULL,
                started_at TIMESTAMPTZ NOT NULL,
                ended_at TIMESTAMPTZ,
                status TEXT NOT NULL,
                duration_seconds DOUBLE PRECISION,
                files_discovered INTEGER NOT NULL DEFAULT 0,
                files_processed INTEGER NOT NULL DEFAULT 0,
                rows_inserted INTEGER NOT NULL DEFAULT 0,
                rows_skipped INTEGER NOT NULL DEFAULT 0,
                warnings INTEGER NOT NULL DEFAULT 0,
                errors INTEGER NOT NULL DEFAULT 0,
                extraction_failures INTEGER NOT NULL DEFAULT 0,
                validation_failures INTEGER NOT NULL DEFAULT 0,
                load_failures INTEGER NOT NULL DEFAULT 0,
                completeness_rate DOUBLE PRECISION,
                validity_rate DOUBLE PRECISION,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS obs.file_ingestion_events (
                event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                run_id UUID NOT NULL REFERENCES obs.pipeline_runs(run_id),
                source_file_path TEXT NOT NULL,
                source_filename TEXT NOT NULL,
                source_modified_at_utc TIMESTAMPTZ,
                file_size_bytes BIGINT,
                file_hash TEXT,
                record_hash TEXT,
                document_version INTEGER,
                status TEXT NOT NULL,
                warning_count INTEGER NOT NULL DEFAULT 0,
                error_count INTEGER NOT NULL DEFAULT 0,
                warning_message TEXT,
                error_message TEXT,
                ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS obs.data_quality_rule_results (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                run_id UUID NOT NULL REFERENCES obs.pipeline_runs(run_id),
                event_id UUID REFERENCES obs.file_ingestion_events(event_id),
                scope TEXT NOT NULL,
                rule_id TEXT NOT NULL,
                severity TEXT NOT NULL,
                status TEXT NOT NULL,
                violations INTEGER NOT NULL DEFAULT 0,
                fail_threshold INTEGER,
                warn_threshold INTEGER,
                details JSONB,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS obs.lineage_events (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                run_id UUID NOT NULL REFERENCES obs.pipeline_runs(run_id),
                event_id UUID REFERENCES obs.file_ingestion_events(event_id),
                source_system TEXT NOT NULL DEFAULT 'excel_master_extractor',
                source_file_path TEXT NOT NULL,
                extracted_payload_hash TEXT,
                target_table TEXT NOT NULL,
                target_row_id UUID,
                target_record_hash TEXT,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS obs.pipeline_state (
                pipeline_name TEXT PRIMARY KEY,
                last_successful_run_id UUID,
                last_successful_run_at TIMESTAMPTZ,
                max_source_modified_at_utc TIMESTAMPTZ,
                processed_files_count BIGINT NOT NULL DEFAULT 0,
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS obs.processed_files (
                source_file_path TEXT NOT NULL,
                source_modified_at_utc TIMESTAMPTZ NOT NULL,
                file_hash TEXT NOT NULL,
                first_run_id UUID NOT NULL REFERENCES obs.pipeline_runs(run_id),
                last_run_id UUID NOT NULL REFERENCES obs.pipeline_runs(run_id),
                times_seen INTEGER NOT NULL DEFAULT 1,
                last_status TEXT NOT NULL,
                PRIMARY KEY (source_file_path, source_modified_at_utc, file_hash)
            );
            """
        )
        for statement in [
            "CREATE INDEX IF NOT EXISTS idx_pipeline_runs_name_started ON obs.pipeline_runs (pipeline_name, started_at DESC);",
            "CREATE INDEX IF NOT EXISTS idx_pipeline_runs_status_started ON obs.pipeline_runs (status, started_at DESC);",
            "CREATE INDEX IF NOT EXISTS idx_file_ingestion_events_ingested ON obs.file_ingestion_events (ingested_at DESC, event_id DESC);",
            "CREATE INDEX IF NOT EXISTS idx_file_ingestion_events_run ON obs.file_ingestion_events (run_id);",
            "CREATE INDEX IF NOT EXISTS idx_file_ingestion_events_status ON obs.file_ingestion_events (status);",
            "CREATE INDEX IF NOT EXISTS idx_file_ingestion_events_source_modified ON obs.file_ingestion_events (source_modified_at_utc DESC);",
            "CREATE INDEX IF NOT EXISTS idx_data_quality_results_event_created ON obs.data_quality_rule_results (event_id, created_at);",
            "CREATE INDEX IF NOT EXISTS idx_data_quality_results_run_created ON obs.data_quality_rule_results (run_id, created_at);",
            "CREATE INDEX IF NOT EXISTS idx_lineage_events_event_created ON obs.lineage_events (event_id, created_at);",
            "CREATE INDEX IF NOT EXISTS idx_lineage_events_run_created ON obs.lineage_events (run_id, created_at);",
            "CREATE INDEX IF NOT EXISTS idx_processed_files_last_run ON obs.processed_files (last_run_id);",
            "CREATE INDEX IF NOT EXISTS idx_processed_files_source_modified ON obs.processed_files (source_modified_at_utc DESC);",
        ]:
            cur.execute(statement)

    def ensure_rating_assessments_schema(self) -> None:
        """Ensure raw ingestion schema exists and is up to date."""
        with psycopg2.connect(self._conn_str()) as conn:
            with conn.cursor() as cur:
                self._ensure_rating_assessments_schema(cur)
            conn.commit()

    def ensure_observability_schema(self) -> None:
        """Ensure observability schema exists and is up to date."""
        with psycopg2.connect(self._conn_str()) as conn:
            with conn.cursor() as cur:
                self._ensure_observability_schema(cur)
            conn.commit()

    def insert_rating_assessment(self, source_file: str, payload: dict) -> dict | None:
        """Insert one extracted record into raw history with idempotent conflict handling."""
        sql_insert = """
        WITH next_version AS (
            SELECT COALESCE(MAX(document_version), 0) + 1 AS version
            FROM raw.rating_assessments_history
            WHERE company_id = %s
        )
        INSERT INTO raw.rating_assessments_history (
            record_hash,
            company_id,
            document_version,
            company_information,
            methodology,
            industry_risk,
            business_risk_profile,
            financial_risk_profile,
            credit_metrics,
            extracted_payload,
            company_name,
            country,
            corporate_sector,
            segmentation_criteria,
            business_risk_score,
            financial_risk_score,
            source_file_path,
            source_modified_at_utc
        )
        SELECT
            %s,
            %s,
            next_version.version,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        FROM next_version
        ON CONFLICT (record_hash) DO NOTHING
        RETURNING id, document_version, record_hash;
        """

        company_information = payload.get("company_information", {})
        methodology = payload.get("company_information", {}).get("methodology") or payload.get(
            "methodology", {}
        )
        industry_risk = payload.get("company_information", {}).get("industry_risk") or payload.get(
            "industry_risk", {}
        )
        business_risk_profile = payload.get("business_risk_profile", {})
        financial_risk_profile = payload.get("financial_risk_profile", {})
        credit_metrics = payload.get("credit_metrics", [])
        company_name = company_information.get("name")
        country = company_information.get("country_of_origin")
        corporate_sector = company_information.get("corporate_sector")
        segmentation_criteria = company_information.get("segmentation_criteria")
        company_id = self.build_company_id(company_name)
        source_file_path, source_modified_at_utc = self.build_source_file_fields(source_file)
        canonical_payload = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        record_hash = hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()

        with psycopg2.connect(self._conn_str()) as conn:
            with conn.cursor() as cur:
                self._ensure_rating_assessments_schema(cur)
                cur.execute(
                    sql_insert,
                    (
                        company_id,
                        record_hash,
                        company_id,
                        Json(company_information),
                        Json(methodology),
                        Json(industry_risk),
                        Json(business_risk_profile),
                        Json(financial_risk_profile),
                        Json(credit_metrics),
                        Json(payload),
                        company_name,
                        country,
                        corporate_sector,
                        segmentation_criteria,
                        business_risk_profile.get("overall_score"),
                        financial_risk_profile.get("overall_score"),
                        source_file_path,
                        source_modified_at_utc,
                    ),
                )
                row = cur.fetchone()
                inserted = (
                    {
                        "id": str(row[0]),
                        "document_version": int(row[1]),
                        "record_hash": str(row[2]),
                    }
                    if row
                    else None
                )
                cur.execute(
                    """
                    UPDATE raw.rating_assessments_history
                    SET segmentation_criteria = company_information ->> 'segmentation_criteria'
                    WHERE segmentation_criteria IS NULL
                      AND company_information ? 'segmentation_criteria';
                    """
                )
            conn.commit()

        return inserted

    def insert_pipeline_run_start(self, run_id: str, pipeline_name: str, started_at: datetime) -> None:
        """Insert or reset a pipeline run row at run start."""
        sql = """
        INSERT INTO obs.pipeline_runs (run_id, pipeline_name, started_at, status)
        VALUES (%s, %s, %s, 'running')
        ON CONFLICT (run_id) DO UPDATE
        SET pipeline_name = EXCLUDED.pipeline_name,
            started_at = EXCLUDED.started_at,
            status = 'running';
        """
        with psycopg2.connect(self._conn_str()) as conn:
            with conn.cursor() as cur:
                self._ensure_observability_schema(cur)
                cur.execute(sql, (run_id, pipeline_name, started_at.isoformat()))
            conn.commit()

    def update_pipeline_run_end(
        self,
        run_id: str,
        metrics: PipelineRunMetrics,
        duration_seconds: float,
        files_discovered: int,
        status: str,
    ) -> None:
        """Update pipeline run completion status and aggregate execution metrics."""
        sql = """
        UPDATE obs.pipeline_runs
        SET ended_at = NOW(),
            status = %s,
            duration_seconds = %s,
            files_discovered = %s,
            files_processed = %s,
            rows_inserted = %s,
            rows_skipped = %s,
            warnings = %s,
            errors = %s,
            extraction_failures = %s,
            validation_failures = %s,
            load_failures = %s,
            completeness_rate = %s,
            validity_rate = %s
        WHERE run_id = %s;
        """
        with psycopg2.connect(self._conn_str()) as conn:
            with conn.cursor() as cur:
                self._ensure_observability_schema(cur)
                cur.execute(
                    sql,
                    (
                        status,
                        duration_seconds,
                        files_discovered,
                        metrics.files_processed,
                        metrics.rows_inserted,
                        metrics.rows_skipped,
                        len(metrics.warnings),
                        len(metrics.errors),
                        metrics.extraction_failures,
                        metrics.validation_failures,
                        metrics.load_failures,
                        metrics.completeness_rate(),
                        metrics.validity_rate(),
                        run_id,
                    ),
                )
            conn.commit()

    def insert_file_ingestion_event(
        self,
        run_id: str,
        *,
        source_file_path: str,
        source_filename: str,
        source_modified_at_utc: datetime | None,
        file_size_bytes: int | None,
        file_hash: str | None,
        record_hash: str | None,
        document_version: int | None,
        status: str,
        warning_message: str | None,
        error_message: str | None,
    ) -> str:
        """Insert one per-file ingestion event and return its generated event id."""
        sql = """
        INSERT INTO obs.file_ingestion_events (
            run_id,
            source_file_path,
            source_filename,
            source_modified_at_utc,
            file_size_bytes,
            file_hash,
            record_hash,
            document_version,
            status,
            warning_count,
            error_count,
            warning_message,
            error_message
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING event_id;
        """
        with psycopg2.connect(self._conn_str()) as conn:
            with conn.cursor() as cur:
                self._ensure_observability_schema(cur)
                cur.execute(
                    sql,
                    (
                        run_id,
                        source_file_path,
                        source_filename,
                        source_modified_at_utc.isoformat() if source_modified_at_utc else None,
                        file_size_bytes,
                        file_hash,
                        record_hash,
                        document_version,
                        status,
                        1 if warning_message else 0,
                        1 if error_message else 0,
                        warning_message,
                        error_message,
                    ),
                )
                row = cur.fetchone()
            conn.commit()
        return str(row[0])

    def insert_data_quality_results(
        self,
        run_id: str,
        event_id: str | None,
        scope: str,
        results: list[RuleOutcome],
        details: dict | None = None,
    ) -> None:
        """Persist business-rule outcomes and optional details for audit/reporting."""
        if not results and not details:
            return
        sql = """
        INSERT INTO obs.data_quality_rule_results (
            run_id, event_id, scope, rule_id, severity, status, violations, details
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        with psycopg2.connect(self._conn_str()) as conn:
            with conn.cursor() as cur:
                self._ensure_observability_schema(cur)
                for result in results:
                    cur.execute(
                        sql,
                        (
                            run_id,
                            event_id,
                            scope,
                            result.rule_id,
                            result.level,
                            result.status,
                            result.violations,
                            Json(details) if details else None,
                        ),
                    )
            conn.commit()

    def insert_lineage_event(
        self,
        run_id: str,
        event_id: str | None,
        source_file_path: str,
        extracted_payload_hash: str | None,
        target_row_id: str | None,
        target_record_hash: str | None,
    ) -> None:
        """Persist lineage from source file payload to inserted raw target row."""
        sql = """
        INSERT INTO obs.lineage_events (
            run_id, event_id, source_file_path, extracted_payload_hash,
            target_table, target_row_id, target_record_hash
        )
        VALUES (%s, %s, %s, %s, 'raw.rating_assessments_history', %s, %s);
        """
        with psycopg2.connect(self._conn_str()) as conn:
            with conn.cursor() as cur:
                self._ensure_observability_schema(cur)
                cur.execute(
                    sql,
                    (
                        run_id,
                        event_id,
                        source_file_path,
                        extracted_payload_hash,
                        target_row_id,
                        target_record_hash,
                    ),
                )
            conn.commit()

    def upsert_processed_file(
        self,
        run_id: str,
        source_file_path: str,
        source_modified_at_utc: datetime | None,
        file_hash: str,
        status: str,
    ) -> None:
        """Upsert processed file fingerprint to support incremental idempotent runs."""
        if source_modified_at_utc is None:
            return
        sql = """
        INSERT INTO obs.processed_files (
            source_file_path, source_modified_at_utc, file_hash, first_run_id, last_run_id, last_status
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (source_file_path, source_modified_at_utc, file_hash)
        DO UPDATE
        SET last_run_id = EXCLUDED.last_run_id,
            times_seen = obs.processed_files.times_seen + 1,
            last_status = EXCLUDED.last_status;
        """
        with psycopg2.connect(self._conn_str()) as conn:
            with conn.cursor() as cur:
                self._ensure_observability_schema(cur)
                cur.execute(
                    sql,
                    (
                        source_file_path,
                        source_modified_at_utc.isoformat(),
                        file_hash,
                        run_id,
                        run_id,
                        status,
                    ),
                )
            conn.commit()

    def upsert_pipeline_state(
        self,
        pipeline_name: str,
        run_id: str,
        last_successful_run_at: datetime | None,
        max_source_modified_at_utc: datetime | None,
        processed_files_count_increment: int,
    ) -> None:
        """Upsert incremental pipeline cursor and processed file counters."""
        sql = """
        INSERT INTO obs.pipeline_state (
            pipeline_name,
            last_successful_run_id,
            last_successful_run_at,
            max_source_modified_at_utc,
            processed_files_count,
            updated_at
        )
        VALUES (%s, %s, %s, %s, %s, NOW())
        ON CONFLICT (pipeline_name) DO UPDATE
        SET last_successful_run_id = EXCLUDED.last_successful_run_id,
            last_successful_run_at = EXCLUDED.last_successful_run_at,
            max_source_modified_at_utc = GREATEST(
                COALESCE(obs.pipeline_state.max_source_modified_at_utc, EXCLUDED.max_source_modified_at_utc),
                COALESCE(EXCLUDED.max_source_modified_at_utc, obs.pipeline_state.max_source_modified_at_utc)
            ),
            processed_files_count = obs.pipeline_state.processed_files_count + EXCLUDED.processed_files_count,
            updated_at = NOW();
        """
        with psycopg2.connect(self._conn_str()) as conn:
            with conn.cursor() as cur:
                self._ensure_observability_schema(cur)
                cur.execute(
                    sql,
                    (
                        pipeline_name,
                        run_id,
                        last_successful_run_at.isoformat() if last_successful_run_at else None,
                        max_source_modified_at_utc.isoformat() if max_source_modified_at_utc else None,
                        processed_files_count_increment,
                    ),
                )
            conn.commit()

    def insert_run_log(self, metrics: PipelineRunMetrics, duration_seconds: float) -> None:
        """Write backward-compatible run summary into legacy `sys.run_logs`."""
        sql_schema = "CREATE SCHEMA IF NOT EXISTS sys;"
        sql_table = """
        CREATE TABLE IF NOT EXISTS sys.run_logs (
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            run_id UUID NOT NULL,
            started_at TIMESTAMPTZ NOT NULL,
            duration DOUBLE PRECISION NOT NULL,
            files_processed INTEGER NOT NULL,
            rows_inserted INTEGER NOT NULL,
            rows_skipped INTEGER NOT NULL,
            extraction_failures INTEGER NOT NULL,
            validation_failures INTEGER NOT NULL,
            load_failures INTEGER NOT NULL,
            warnings INTEGER NOT NULL,
            errors INTEGER NOT NULL,
            completeness_rate DOUBLE PRECISION NOT NULL,
            validity_rate DOUBLE PRECISION NOT NULL
        );
        """
        sql_insert = """
        INSERT INTO sys.run_logs (
            run_id,
            started_at,
            duration,
            files_processed,
            rows_inserted,
            rows_skipped,
            extraction_failures,
            validation_failures,
            load_failures,
            warnings,
            errors,
            completeness_rate,
            validity_rate
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        with psycopg2.connect(self._conn_str()) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_schema)
                cur.execute(sql_table)
                for statement in [
                    "ALTER TABLE sys.run_logs ADD COLUMN IF NOT EXISTS rows_inserted INTEGER;",
                    "ALTER TABLE sys.run_logs ADD COLUMN IF NOT EXISTS rows_skipped INTEGER;",
                    "ALTER TABLE sys.run_logs ADD COLUMN IF NOT EXISTS extraction_failures INTEGER;",
                    "ALTER TABLE sys.run_logs ADD COLUMN IF NOT EXISTS validation_failures INTEGER;",
                    "ALTER TABLE sys.run_logs ADD COLUMN IF NOT EXISTS load_failures INTEGER;",
                    "ALTER TABLE sys.run_logs ADD COLUMN IF NOT EXISTS warnings INTEGER;",
                    "ALTER TABLE sys.run_logs ADD COLUMN IF NOT EXISTS errors INTEGER;",
                    "ALTER TABLE sys.run_logs ADD COLUMN IF NOT EXISTS completeness_rate DOUBLE PRECISION;",
                    "ALTER TABLE sys.run_logs ADD COLUMN IF NOT EXISTS validity_rate DOUBLE PRECISION;",
                    "ALTER TABLE sys.run_logs DROP COLUMN IF EXISTS rows_extracted;",
                    "ALTER TABLE sys.run_logs DROP COLUMN IF EXISTS task_name;",
                    "ALTER TABLE sys.run_logs DROP COLUMN IF EXISTS warning_count;",
                    "ALTER TABLE sys.run_logs DROP COLUMN IF EXISTS error_count;",
                ]:
                    cur.execute(statement)

                cur.execute(
                    sql_insert,
                    (
                        metrics.run_id,
                        metrics.started_at.isoformat(),
                        duration_seconds,
                        metrics.files_processed,
                        metrics.rows_inserted,
                        metrics.rows_skipped,
                        metrics.extraction_failures,
                        metrics.validation_failures,
                        metrics.load_failures,
                        len(metrics.warnings),
                        len(metrics.errors),
                        metrics.completeness_rate(),
                        metrics.validity_rate(),
                    ),
                )
            conn.commit()

    def insert_file_logs(self, run_id: str, file_logs: list[FileProcessLog]) -> None:
        """Write backward-compatible per-file logs into legacy `sys.file_logs`."""
        if not file_logs:
            return

        sql_schema = "CREATE SCHEMA IF NOT EXISTS sys;"
        sql_table = """
        CREATE TABLE IF NOT EXISTS sys.file_logs (
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            run_id UUID NOT NULL,
            source_file_path TEXT NOT NULL,
            source_filename TEXT NOT NULL,
            status TEXT NOT NULL,
            warning_message TEXT,
            error_message TEXT
        );
        """
        sql_insert = """
        INSERT INTO sys.file_logs (
            run_id,
            source_file_path,
            source_filename,
            status,
            warning_message,
            error_message
        )
        VALUES (%s, %s, %s, %s, %s, %s);
        """

        with psycopg2.connect(self._conn_str()) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_schema)
                cur.execute(sql_table)
                cur.execute("ALTER TABLE sys.file_logs DROP COLUMN IF EXISTS task_name;")
                for entry in file_logs:
                    cur.execute(
                        sql_insert,
                        (
                            run_id,
                            entry.source_file_path,
                            entry.source_filename,
                            entry.status,
                            entry.warning_message,
                            entry.error_message,
                        ),
                    )
            conn.commit()

    def query_violation_count(self, query: str) -> int:
        """Execute a scalar query and return an integer count value."""
        with psycopg2.connect(self._conn_str()) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                row = cur.fetchone()
                if not row or row[0] is None:
                    return 0
                return int(row[0])
