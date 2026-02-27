"""FastAPI application wiring."""

from __future__ import annotations

import logging

import psycopg2
from fastapi import APIRouter, FastAPI

from api.company import controller as company_controller
from api.company.service import CompanyService
from api.providers.company_provider import CompanyProvider
from helpers.constants import (
    API_DESCRIPTION,
    API_TITLE,
    API_VERSION,
    API_VERSION_PATH,
    PG_DATABASE,
    PG_HOST,
    PG_PASSWORD,
    PG_PORT,
    PG_USER,
)

LOGGER = logging.getLogger(__name__)


def _build_company_service() -> CompanyService:
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD,
    )
    # Prevent idle-in-transaction sessions for read-only API queries.
    conn.set_session(readonly=True, autocommit=True)
    return CompanyService(company_provider=CompanyProvider(connection=conn))


def make_app(is_local_runtime: bool = False) -> FastAPI:
    """Create and wire the FastAPI application."""
    _ = is_local_runtime
    LOGGER.info("Creating FastAPI app.")

    app = FastAPI(
        title=API_TITLE,
        description=API_DESCRIPTION,
        version=API_VERSION,
    )

    service = _build_company_service()
    router = APIRouter()
    company_controller.build(router=router, service=service)
    app.include_router(router, prefix=f"/{API_VERSION_PATH}")

    return app
