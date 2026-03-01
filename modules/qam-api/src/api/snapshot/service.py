"""Snapshot service."""

from datetime import date

from api.providers.snapshot_provider import SnapshotProvider
from api.snapshot.models import SnapshotModel


class SnapshotService:
    """Application service for snapshot read/query operations."""

    def __init__(self, snapshot_provider: SnapshotProvider):
        """Instantiate snapshot service with its persistence provider."""
        self.snapshot_provider = snapshot_provider

    def list_snapshots(
        self,
        *,
        company_id: str | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
        sector: str | None = None,
        country: str | None = None,
        currency: str | None = None,
    ) -> list[SnapshotModel]:
        """List snapshots with optional API filters."""
        return self.snapshot_provider.list(
            company_id=company_id,
            from_date=from_date,
            to_date=to_date,
            sector=sector,
            country=country,
            currency=currency,
        )

    def get_snapshot(self, snapshot_id: str) -> SnapshotModel:
        """Get one snapshot row by identifier."""
        return self.snapshot_provider.get(snapshot_id)

    def get_latest_snapshots(self) -> list[SnapshotModel]:
        """Get latest active snapshot row for each company."""
        return self.snapshot_provider.latest()
