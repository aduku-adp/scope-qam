"""Company API controller."""

import logging
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query
from helpers.formatter import ErrorModel, OutputModel, format_response
from api.company.models import (
    CompanyComparisonDiffModel,
    CompanyHistoryPointModel,
    CompanyModel,
)
from api.company.service import CompanyService


LOGGER = logging.getLogger(__name__)
COMPANY_TAG = "Company Endpoints"


def build(
    router: APIRouter,
    service: CompanyService,
) -> None:
    """Register company endpoints on the shared API router."""
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
        "/companies/compare",
        tags=[COMPANY_TAG],
        responses={
            400: {"description": "Invalid request", "model": ErrorModel},
            500: {"description": "Server error", "model": ErrorModel},
            404: {"description": "Not Found", "model": ErrorModel},
        },
        response_model_exclude_none=True,
    )
    async def compare_companies(
        company_ids: Annotated[
            str,
            Query(
                description="Comma-separated company ids to compare.",
                examples=["company_a,company_b"],
            ),
        ],
        as_of_date: Annotated[
            datetime | None,
            Query(
                description="Optional point-in-time filter in ISO-8601 format.",
                examples=["2026-02-25T00:00:00Z"],
            ),
        ] = None,
    ) -> OutputModel[list[CompanyComparisonDiffModel]]:
        """Compare companies and return only column-level differences."""
        LOGGER.debug("controller.get: Compare companies")

        parsed_ids = [item.strip() for item in company_ids.split(",") if item.strip()]
        if not parsed_ids:
            raise HTTPException(
                status_code=400, detail="company_ids must include at least one id"
            )

        try:
            compared = service.compare_companies_with_diffs(
                parsed_ids, as_of_date=as_of_date
            )
        except Exception as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        return format_response(compared)

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

    @router.get(
        "/companies/{company_id}/versions",
        tags=[COMPANY_TAG],
        responses={
            500: {"description": "Server error", "model": ErrorModel},
            404: {"description": "Not Found", "model": ErrorModel},
        },
        response_model_exclude_none=True,
    )
    async def get_company_versions(
        company_id: Annotated[
            str,
            Path(description="Company id", examples=["company_b"]),
        ],
    ) -> OutputModel[list[CompanyModel]]:
        """Get all versions for a company."""
        LOGGER.debug("controller.get: Get all versions for a company")

        try:
            versions = service.get_company_versions(company_id)
        except Exception as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        return format_response(versions)

    @router.get(
        "/companies/{company_id}/history",
        tags=[COMPANY_TAG],
        responses={
            500: {"description": "Server error", "model": ErrorModel},
            404: {"description": "Not Found", "model": ErrorModel},
        },
        response_model_exclude_none=True,
    )
    async def get_company_history(
        company_id: Annotated[
            str,
            Path(description="Company id", examples=["company_b"]),
        ],
        column_name: Annotated[
            str,
            Query(
                description="Level-1 selector: root column name or top-level block name (e.g. industry_risk_score, credit_metrics).",
                examples=["industry_risk_score"],
            ),
        ],
        metric_name: Annotated[
            str | None,
            Query(
                description="Optional Level-2 selector (e.g. credit_metrics.liquidity -> metric_name=liquidity).",
                examples=["liquidity"],
            ),
        ] = None,
        year_label: Annotated[
            str | None,
            Query(
                description="Optional Level-3 selector (e.g. credit_metrics.liquidity.year_label -> year_label=2025).",
                examples=["2025"],
            ),
        ] = None,
    ) -> OutputModel[list[CompanyHistoryPointModel]]:
        """Get filtered time-series points for one company."""
        LOGGER.debug("controller.get: Get time-series history for a company")

        try:
            history = service.get_company_history(
                company_id,
                column_name=column_name,
                metric_name=metric_name,
                year_label=year_label,
            )
        except Exception as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        return format_response(history)
