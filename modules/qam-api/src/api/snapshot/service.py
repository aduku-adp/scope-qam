"""Snapshot service."""

from datetime import date

from api.providers.snapshot_provider import SnapshotProvider
from api.snapshot.models import SnapshotModel


class SnapshotService:
    """Snapshot service."""

    def __init__(self, snapshot_provider: SnapshotProvider):
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
        """List snapshots with optional filters."""
        return self.snapshot_provider.list(
            company_id=company_id,
            from_date=from_date,
            to_date=to_date,
            sector=sector,
            country=country,
            currency=currency,
        )

    def get_snapshot(self, snapshot_id: str) -> SnapshotModel:
        """Get a specific snapshot."""
        return self.snapshot_provider.get(snapshot_id)

    def get_latest_snapshots(self) -> list[SnapshotModel]:
        """Get latest snapshot for each company."""
        return self.snapshot_provider.latest()

