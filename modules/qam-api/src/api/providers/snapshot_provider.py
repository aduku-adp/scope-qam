"""Snapshot provider - Postgres implementation."""

from __future__ import annotations

from datetime import date

from psycopg2.extensions import connection as PgConnection
from psycopg2.extras import RealDictCursor

from api.snapshot.models import SnapshotModel


class NotFound(Exception):
    """Raised when a requested snapshot cannot be found."""

    pass


class SnapshotProvider:
    """Snapshot provider for snapshots.snap_company table."""

    def __init__(self, connection: PgConnection):
        """Instantiate provider with an open PostgreSQL connection."""
        self.conn = connection

    def list(
        self,
        *,
        company_id: str | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
        sector: str | None = None,
        country: str | None = None,
        currency: str | None = None,
    ) -> list[SnapshotModel]:
        """List snapshot rows with optional business/date filters."""
        query = """
            SELECT
                sc.*,
                dbt_scd_id as snapshot_id,
                sc.snapshot_created_at,
                dbt_valid_from as snapshot_valid_from,
                dbt_valid_to as snapshot_valid_to
            FROM snapshots.snap_company sc
            WHERE dbt_scd_id IS NOT NULL
        """
        params: list[object] = []

        if company_id:
            query += " AND company_id = %s"
            params.append(company_id)
        if from_date:
            query += " AND source_modified_at_utc::date >= %s"
            params.append(from_date)
        if to_date:
            query += " AND source_modified_at_utc::date <= %s"
            params.append(to_date)
        if sector:
            query += " AND corporate_sector = %s"
            params.append(sector)
        if country:
            query += " AND country = %s"
            params.append(country)
        if currency:
            query += " AND reporting_currency = %s"
            params.append(currency)

        query += (
            " ORDER BY company_id ASC, source_modified_at_utc DESC, "
            "dbt_valid_from DESC, document_version DESC"
        )

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, tuple(params))
            rows = cur.fetchall()

        return [SnapshotModel(**row) for row in rows]

    def get(self, snapshot_id: str) -> SnapshotModel:
        """Get one snapshot by dbt-generated snapshot identifier."""
        query = """
            SELECT
                sc.*,
                dbt_scd_id as snapshot_id,
                sc.snapshot_created_at,
                dbt_valid_from as snapshot_valid_from,
                dbt_valid_to as snapshot_valid_to
            FROM snapshots.snap_company sc
            WHERE dbt_scd_id = %s
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (snapshot_id,))
            row = cur.fetchone()

        if not row:
            raise NotFound(f"Snapshot {snapshot_id} not found")

        return SnapshotModel(**row)

    def latest(self) -> list[SnapshotModel]:
        """Get current active snapshot row for each company (`dbt_valid_to IS NULL`)."""
        query = """
            SELECT DISTINCT ON (company_id)
                sc.*,
                dbt_scd_id as snapshot_id,
                sc.snapshot_created_at,
                dbt_valid_from as snapshot_valid_from,
                dbt_valid_to as snapshot_valid_to
            FROM snapshots.snap_company sc
            WHERE dbt_valid_to IS NULL
              AND dbt_scd_id IS NOT NULL
            ORDER BY company_id ASC, source_modified_at_utc DESC, dbt_valid_from DESC, document_version DESC
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

        return [SnapshotModel(**row) for row in rows]
