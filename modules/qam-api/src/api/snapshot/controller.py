"""Snapshot API controller."""

from datetime import date
import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query

from api.snapshot.models import SnapshotModel
from api.snapshot.service import SnapshotService
from helpers.formatter import ErrorModel, OutputModel, format_response

LOGGER = logging.getLogger(__name__)
SNAPSHOT_TAG = "Snapshot Endpoints"


def build(router: APIRouter, service: SnapshotService) -> None:
    """Build snapshot routes."""

    @router.get(
        "/snapshots",
        tags=[SNAPSHOT_TAG],
        responses={
            500: {"description": "Server error", "model": ErrorModel},
        },
        response_model_exclude_none=True,
    )
    async def list_snapshots(
        company_id: Annotated[str | None, Query(description="Filter by company id")] = None,
        from_date: Annotated[date | None, Query(description="Filter start date (inclusive)")] = None,
        to_date: Annotated[date | None, Query(description="Filter end date (inclusive)")] = None,
        sector: Annotated[str | None, Query(description="Filter by corporate sector")] = None,
        country: Annotated[str | None, Query(description="Filter by country")] = None,
        currency: Annotated[str | None, Query(description="Filter by reporting currency")] = None,
    ) -> OutputModel[list[SnapshotModel]]:
        """List all snapshots with filters."""
        snapshots = service.list_snapshots(
            company_id=company_id,
            from_date=from_date,
            to_date=to_date,
            sector=sector,
            country=country,
            currency=currency,
        )
        return format_response(snapshots)

    @router.get(
        "/snapshots/latest",
        tags=[SNAPSHOT_TAG],
        responses={
            500: {"description": "Server error", "model": ErrorModel},
        },
        response_model_exclude_none=True,
    )
    async def latest_snapshots() -> OutputModel[list[SnapshotModel]]:
        """Get latest snapshot for each company."""
        snapshots = service.get_latest_snapshots()
        return format_response(snapshots)

    @router.get(
        "/snapshots/{snapshot_id}",
        tags=[SNAPSHOT_TAG],
        responses={
            404: {"description": "Not Found", "model": ErrorModel},
            500: {"description": "Server error", "model": ErrorModel},
        },
        response_model_exclude_none=True,
    )
    async def get_snapshot(
        snapshot_id: Annotated[str, Path(description="Snapshot id")],
    ) -> OutputModel[SnapshotModel]:
        """Get one snapshot."""
        try:
            snapshot = service.get_snapshot(snapshot_id)
        except Exception as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        return format_response(snapshot)

