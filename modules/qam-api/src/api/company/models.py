"""Pydantic models for company endpoints."""

from datetime import date, datetime
from typing import Any, Optional

# pylint: disable=invalid-name, no-self-argument
from pydantic import BaseModel, Field, model_validator


class CompanyModel(BaseModel):
    """Company payload model backed by `reports.rep_company`."""

    rep_company_key: Optional[str] = Field(
        description="Primary key of reports.rep_company row.",
        examples=["a9f1f3e4..."],
        default=None,
    )

    company_id: str = Field(
        description="Business identifier of the company.",
        examples=["COMP123"],
    )

    company_name: Optional[str] = Field(
        description="Official name of the company.",
        examples=["ACME Corporation"],
        default=None,
    )

    country: Optional[str] = Field(
        description="Country where the company operates or is registered.",
        examples=["DE"],
        default=None,
    )

    corporate_sector: Optional[str] = Field(
        description="Corporate sector of the company.",
        examples=["Industrial"],
        default=None,
    )

    reporting_currency: Optional[str] = Field(
        description="Currency used for financial reporting.",
        examples=["EUR"],
        default=None,
    )

    accounting_principles: Optional[str] = Field(
        description="Accounting principles applied by the company.",
        examples=["IFRS"],
        default=None,
    )

    fiscal_year_end: Optional[str] = Field(
        description="Fiscal year end date (MM-DD format).",
        examples=["12-31"],
        default=None,
    )

    industry_classification: Optional[str] = Field(
        description="Industry classification of the company.",
        examples=["Consumer Goods"],
        default=None,
    )

    industry_risk_score: Optional[str] = Field(
        description="Industry risk score classification.",
        examples=["Medium"],
        default=None,
    )

    industry_weight: Optional[str] = Field(
        description="Industry weights from all industry-risk rows, pipe-delimited.",
        examples=["0.25 | 0.75"],
        default=None,
    )

    segmentation_criteria: Optional[str] = Field(
        description="Segmentation criteria used for grouping companies.",
        examples=["Enterprise"],
        default=None,
    )

    rating_methodologies_applied: Optional[str] = Field(
        description="Rating methodologies applied to the company.",
        examples=["Corporate Rating v2"],
        default=None,
    )

    document_version: Optional[int] = Field(
        description="Version number of the company document.",
        examples=[1],
        default=None,
        ge=1,
    )

    start_at: Optional[datetime] = Field(
        description="Start timestamp of the SCD validity period.",
        examples=["2024-01-01T00:00:00Z"],
        default=None,
    )

    end_at: Optional[datetime] = Field(
        description="End timestamp of the SCD validity period.",
        examples=["2025-01-01T00:00:00Z"],
        default=None,
    )

    is_active: bool = Field(
        description="Indicates whether the company record is active.",
        examples=[True],
        default=True,
    )

    source_modified_date_key: Optional[int] = Field(default=None)
    source_modified_date: Optional[date] = Field(default=None)
    source_file_path: Optional[str] = Field(default=None)
    source_modified_at_utc: Optional[datetime] = Field(default=None)
    ingested_at: Optional[datetime] = Field(default=None)

    business_risk_score: Optional[str] = Field(default=None)
    financial_risk_score: Optional[str] = Field(default=None)
    blended_industry_risk_profile: Optional[str] = Field(default=None)
    competitive_positioning: Optional[str] = Field(default=None)
    market_share: Optional[str] = Field(default=None)
    diversification: Optional[str] = Field(default=None)
    operating_profitability: Optional[str] = Field(default=None)
    sector_company_specific_factors_1: Optional[str] = Field(default=None)
    sector_company_specific_factors_2: Optional[str] = Field(default=None)
    leverage: Optional[str] = Field(default=None)
    interest_cover: Optional[str] = Field(default=None)
    cash_flow_cover: Optional[str] = Field(default=None)
    liquidity_adjustment_notches: Optional[int] = Field(default=None)

    credit_metrics: Optional[list[dict[str, Any]]] = Field(default=None)

    @model_validator(mode="after")
    def validate_scd_dates(self) -> "CompanyModel":
        """Ensure SCD validity logic is consistent."""

        if self.start_at and self.end_at:
            if self.end_at <= self.start_at:
                raise ValueError("end_at must be greater than start_at")

        if self.is_active and self.end_at is not None:
            raise ValueError("Active records should not have end_at defined")

        return self

    @model_validator(mode="after")
    def validate_document_version(self) -> "CompanyModel":
        """Ensure document_version is coherent with SCD logic."""

        if self.document_version is not None and self.document_version < 1:
            raise ValueError("document_version must be >= 1")

        return self


class CompanyHistoryPointModel(BaseModel):
    """Normalized time-series point used by `/companies/{company_id}/history`."""

    timeseries_key: str = Field(
        description="Unique key for the normalized time-series point.",
        examples=["5a9036bc3f490fd304f4c2c292e6388f"],
    )

    company_id: str = Field(
        description="Business identifier of the company.",
        examples=["company_b"],
    )

    document_version: int = Field(
        description="Version number associated with this time-series point.",
        examples=[2],
        ge=1,
    )

    event_time: datetime = Field(
        description="Timestamp of the time-series event.",
        examples=["2026-02-25T22:37:26.360512Z"],
    )
    column_name: str = Field(
        description="Requested column/block name used as level-1 selector.",
        examples=["industry_risk_score"],
    )
    metric_name: str = Field(
        description="Optional level-2 metric identifier.",
        examples=["scope_adjusted_debt_ebitda"],
    )
    series_value: str = Field(
        description="Series value represented as text.",
        examples=["18.49"],
    )
    year_label: Optional[str] = Field(default=None)
    is_estimate: Optional[bool] = Field(default=None)


class CompanyComparisonDiffModel(BaseModel):
    """Diff payload for one compared column."""

    column: str = Field(
        description="Column name that differs across compared companies.",
        examples=["country"],
    )
    values_by_company_id: dict[str, Any] = Field(
        description="Per-company value for this column.",
        examples=[{"company_a": "DE", "company_b": "CH"}],
    )


class CompanyCompareResultModel(BaseModel):
    """Legacy comparison payload shape kept for backward compatibility."""

    companies: list[CompanyModel]
    diffs: list[CompanyComparisonDiffModel]
