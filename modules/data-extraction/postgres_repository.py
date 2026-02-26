"""Postgres persistence and incremental-read operations."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import psycopg2
from psycopg2.extras import Json

from config import DbConfig
from pipeline_types import FileProcessLog, PipelineRunMetrics


class PostgresRepository:
    def __init__(self, db_config: DbConfig) -> None:
        self.db_config = db_config

    def _conn_str(self) -> str:
        return (
            f"host={self.db_config.host} "
            f"port={self.db_config.port} "
            f"dbname={self.db_config.dbname} "
            f"user={self.db_config.user} "
            f"password={self.db_config.password}"
        )

    @staticmethod
    def build_source_file_fields(source_file: str | Path) -> tuple[str, str | None]:
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
        source_path = Path(source_file).resolve()
        try:
            stats = source_path.stat()
            return datetime.fromtimestamp(stats.st_mtime, tz=UTC)
        except FileNotFoundError:
            return None

    @staticmethod
    def build_company_key(company_name: str | None, country: str | None) -> str:
        key_material = f"{company_name or ''}|{country or ''}"
        return hashlib.md5(key_material.encode("utf-8")).hexdigest()

    def get_incremental_cutoff(self) -> datetime | None:
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

    def _ensure_rating_assessments_schema(self, cur) -> None:
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
                company_key TEXT NOT NULL,
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
                UNIQUE (company_key, document_version)
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
            "ALTER TABLE raw.rating_assessments_history ADD COLUMN IF NOT EXISTS company_key TEXT;",
            "ALTER TABLE raw.rating_assessments_history ADD COLUMN IF NOT EXISTS corporate_sector TEXT;",
            "ALTER TABLE raw.rating_assessments_history ADD COLUMN IF NOT EXISTS segmentation_criteria TEXT;",
            "ALTER TABLE raw.rating_assessments_history DROP COLUMN IF EXISTS industry;",
            "CREATE UNIQUE INDEX IF NOT EXISTS uq_rating_assessments_history_company_version ON raw.rating_assessments_history (company_key, document_version);",
            "ALTER TABLE raw.rating_assessments_history ADD COLUMN IF NOT EXISTS source_file_path TEXT;",
            "ALTER TABLE raw.rating_assessments_history ADD COLUMN IF NOT EXISTS source_modified_at_utc TIMESTAMPTZ;",
            "ALTER TABLE raw.rating_assessments_history DROP COLUMN IF EXISTS extracted_at;",
            "ALTER TABLE raw.rating_assessments_history DROP COLUMN IF EXISTS rating_date;",
        ]:
            cur.execute(statement)

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

    def ensure_rating_assessments_schema(self) -> None:
        with psycopg2.connect(self._conn_str()) as conn:
            with conn.cursor() as cur:
                self._ensure_rating_assessments_schema(cur)
            conn.commit()

    def insert_rating_assessment(self, source_file: str, payload: dict) -> str | None:
        sql_insert = """
        WITH next_version AS (
            SELECT COALESCE(MAX(document_version), 0) + 1 AS version
            FROM raw.rating_assessments_history
            WHERE company_key = %s
        )
        INSERT INTO raw.rating_assessments_history (
            record_hash,
            company_key,
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
        RETURNING id;
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
        company_key = self.build_company_key(company_name, country)
        source_file_path, source_modified_at_utc = self.build_source_file_fields(source_file)
        canonical_payload = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        record_hash = hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()

        with psycopg2.connect(self._conn_str()) as conn:
            with conn.cursor() as cur:
                self._ensure_rating_assessments_schema(cur)
                cur.execute(
                    sql_insert,
                    (
                        company_key,
                        record_hash,
                        company_key,
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
                inserted_id = str(row[0]) if row else None
                cur.execute(
                    """
                    UPDATE raw.rating_assessments_history
                    SET segmentation_criteria = company_information ->> 'segmentation_criteria'
                    WHERE segmentation_criteria IS NULL
                      AND company_information ? 'segmentation_criteria';
                    """
                )
            conn.commit()

        return inserted_id

    def insert_run_log(self, metrics: PipelineRunMetrics, duration_seconds: float) -> None:
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
        with psycopg2.connect(self._conn_str()) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                row = cur.fetchone()
                if not row or row[0] is None:
                    return 0
                return int(row[0])
