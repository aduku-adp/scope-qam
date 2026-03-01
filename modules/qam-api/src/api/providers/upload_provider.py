"""Upload provider - Postgres implementation."""

from __future__ import annotations

from psycopg2.extensions import connection as PgConnection
from psycopg2.extras import RealDictCursor

from api.upload.models import UploadDetailsModel, UploadModel, UploadStatsModel


class NotFound(Exception):
    """Raised when an upload event or linked upload asset does not exist."""

    pass


class UploadProvider:
    """Upload provider for observability audit tables."""

    def __init__(self, connection: PgConnection):
        """Instantiate provider with an open PostgreSQL connection."""
        self.conn = connection

    def list(self) -> list[UploadModel]:
        """List upload events ordered by ingestion recency."""
        query = """
            SELECT
                fie.event_id::text AS upload_id,
                fie.run_id::text AS run_id,
                pr.pipeline_name,
                fie.source_file_path,
                fie.source_filename,
                fie.source_modified_at_utc,
                fie.file_size_bytes,
                fie.file_hash,
                fie.record_hash,
                fie.document_version,
                fie.status,
                fie.warning_count,
                fie.error_count,
                fie.warning_message,
                fie.error_message,
                fie.ingested_at
            FROM obs.file_ingestion_events fie
            LEFT JOIN obs.pipeline_runs pr
                ON pr.run_id = fie.run_id
            ORDER BY fie.ingested_at DESC, fie.event_id DESC
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()
        return [UploadModel(**row) for row in rows]

    def get(self, upload_id: str) -> UploadModel:
        """Get one upload event by UUID identifier."""
        query = """
            SELECT
                fie.event_id::text AS upload_id,
                fie.run_id::text AS run_id,
                pr.pipeline_name,
                fie.source_file_path,
                fie.source_filename,
                fie.source_modified_at_utc,
                fie.file_size_bytes,
                fie.file_hash,
                fie.record_hash,
                fie.document_version,
                fie.status,
                fie.warning_count,
                fie.error_count,
                fie.warning_message,
                fie.error_message,
                fie.ingested_at
            FROM obs.file_ingestion_events fie
            LEFT JOIN obs.pipeline_runs pr
                ON pr.run_id = fie.run_id
            WHERE fie.event_id = %s::uuid
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (upload_id,))
            row = cur.fetchone()
        if not row:
            raise NotFound(f"Upload {upload_id} not found")
        return UploadModel(**row)

    def get_details(self, upload_id: str) -> UploadDetailsModel:
        """Get one upload with data quality and lineage traces."""
        upload = self.get(upload_id)
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                    rule_id,
                    severity,
                    status,
                    violations,
                    details,
                    created_at
                FROM obs.data_quality_rule_results
                WHERE event_id = %s::uuid
                ORDER BY created_at ASC
                """,
                (upload_id,),
            )
            dq_rows = cur.fetchall()
            cur.execute(
                """
                SELECT
                    id::text AS lineage_id,
                    source_system,
                    source_file_path,
                    extracted_payload_hash,
                    target_table,
                    target_row_id::text AS target_row_id,
                    target_record_hash,
                    created_at
                FROM obs.lineage_events
                WHERE event_id = %s::uuid
                ORDER BY created_at ASC
                """,
                (upload_id,),
            )
            lineage_rows = cur.fetchall()
        return UploadDetailsModel(
            upload=upload,
            data_quality_results=[dict(row) for row in dq_rows],
            lineage_events=[dict(row) for row in lineage_rows],
        )

    def get_file_info(self, upload_id: str) -> tuple[str, str]:
        """Return source file path and name for download endpoint resolution."""
        upload = self.get(upload_id)
        if not upload.source_file_path or not upload.source_filename:
            raise NotFound(f"No source file found for upload {upload_id}")
        return upload.source_file_path, upload.source_filename

    def stats(self) -> UploadStatsModel:
        """Return aggregate upload metrics and status distribution."""
        query_totals = """
            SELECT
                COUNT(*)::int AS total_uploads,
                COUNT(*) FILTER (WHERE status = 'inserted')::int AS successful_uploads,
                COUNT(*) FILTER (WHERE status <> 'inserted')::int AS failed_uploads,
                COALESCE(SUM(warning_count), 0)::int AS total_warnings,
                COALESCE(SUM(error_count), 0)::int AS total_errors,
                AVG(file_size_bytes)::float AS avg_file_size_bytes,
                MAX(ingested_at) AS latest_upload_at
            FROM obs.file_ingestion_events
        """
        query_by_status = """
            SELECT status, COUNT(*)::int AS cnt
            FROM obs.file_ingestion_events
            GROUP BY status
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query_totals)
            totals_row = cur.fetchone() or {}
            cur.execute(query_by_status)
            status_rows = cur.fetchall()

        uploads_by_status = {row["status"]: row["cnt"] for row in status_rows if row.get("status")}
        return UploadStatsModel(
            total_uploads=totals_row.get("total_uploads", 0),
            successful_uploads=totals_row.get("successful_uploads", 0),
            failed_uploads=totals_row.get("failed_uploads", 0),
            total_warnings=totals_row.get("total_warnings", 0),
            total_errors=totals_row.get("total_errors", 0),
            avg_file_size_bytes=totals_row.get("avg_file_size_bytes"),
            latest_upload_at=totals_row.get("latest_upload_at"),
            uploads_by_status=uploads_by_status,
        )
