"""Snapshot provider - Postgres implementation."""

from __future__ import annotations

from datetime import date

from psycopg2.extensions import connection as PgConnection
from psycopg2.extras import RealDictCursor

from api.snapshot.models import SnapshotModel


class NotFound(Exception):
    pass


class SnapshotProvider:
    """Snapshot provider for snapshots.snap_company table."""

    def __init__(self, connection: PgConnection):
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
        """List snapshots with optional filters."""
        query = """
            SELECT *
            FROM snapshots.snap_company
            WHERE 1 = 1
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
            "snapshot_created_at DESC, document_version DESC"
        )

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, tuple(params))
            rows = cur.fetchall()

        return [SnapshotModel(**row) for row in rows]

    def get(self, snapshot_id: str) -> SnapshotModel:
        """Get one snapshot by snapshot_id."""
        query = """
            SELECT *
            FROM snapshots.snap_company
            WHERE snapshot_id = %s
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (snapshot_id,))
            row = cur.fetchone()

        if not row:
            raise NotFound(f"Snapshot {snapshot_id} not found")

        return SnapshotModel(**row)

    def latest(self) -> list[SnapshotModel]:
        """Get latest snapshot for each company."""
        query = """
            SELECT DISTINCT ON (company_id) *
            FROM snapshots.snap_company
            ORDER BY company_id ASC, source_modified_at_utc DESC, snapshot_created_at DESC, document_version DESC
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

        return [SnapshotModel(**row) for row in rows]
