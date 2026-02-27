"""Qam API."""

import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path
from helpers.formatter import ErrorModel, OutputModel, format_response
from api.company.models import (
    CompanyModel,
)
from api.company.service import CompanyService


LOGGER = logging.getLogger(__name__)
COMPANY_TAG = "Company Endpoints"


def build(
    router: APIRouter,
    service: CompanyService,
) -> None:
    """Handle requests."""
    LOGGER.debug("Create %s controller", __name__)

    @router.get(
        "/companies",
        tags=[COMPANY_TAG],
        responses={
            500: {"description": "Server error", "model": ErrorModel},
            404: {"description": "Not Found", "model": ErrorModel},
        },
        response_model_exclude_none=True,
    )
    async def get_companies() -> OutputModel[list[CompanyModel]]:
        """List all companies with current metadata."""
        LOGGER.debug("controller.get: List all companies with current metadata")

        try:
            members = service.list_all()
        except Exception as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        return format_response(members)

    @router.get(
        "/companies/{company_id}",
        tags=[COMPANY_TAG],
        responses={
            500: {"description": "Server error", "model": ErrorModel},
            404: {"description": "Not Found", "model": ErrorModel},
        },
        response_model_exclude_none=True,
    )
    async def get_company(
        company_id: Annotated[
            str,
            Path(description="Company id", examples=["company_b"]),
        ],
    ) -> OutputModel[CompanyModel]:
        """Get company details (latest version)."""
        LOGGER.debug("controller.get: Get company details (latest version)")

        try:
            company = service.get_company(company_id)
        except Exception as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        return format_response(company)
