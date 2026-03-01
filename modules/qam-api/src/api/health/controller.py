"""Health API controller."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from api.health.models import HealthModel
from api.health.service import HealthService
from helpers.formatter import ErrorModel, OutputModel, format_response

HEALTH_TAG = "Health Endpoints"


def build(router: APIRouter, service: HealthService) -> None:
    """Register health endpoints on the shared API router."""

    @router.get(
        "/health",
        tags=[HEALTH_TAG],
        responses={
            500: {"description": "Server error", "model": ErrorModel},
            503: {"description": "Service unhealthy", "model": ErrorModel},
        },
        response_model_exclude_none=True,
    )
    async def health() -> OutputModel[HealthModel]:
        """Return service health, using HTTP 503 when unhealthy."""
        payload = format_response(service.get_health())
        if not payload.data or not payload.data.healthy:
            return JSONResponse(status_code=503, content=payload.model_dump(mode="json"))
        return payload
