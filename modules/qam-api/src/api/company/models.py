"""Common models for payload and response."""

from typing import Optional

# pylint: disable=invalid-name, no-self-argument
from pydantic import BaseModel, Field, model_validator


from datetime import date, datetime


class CompanyModel(BaseModel):
    """Company model."""

    company_scd_key: str = Field(
        description="Surrogate key for the company (SCD identifier).",
        examples=["COMP123_v1"],
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
    """Time-series point for company analysis."""

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

    source_modified_at_utc: Optional[datetime] = Field(default=None)
    event_time: datetime = Field(
        description="Timestamp of the time-series event.",
        examples=["2026-02-25T22:37:26.360512Z"],
    )
    source_file_path: Optional[str] = Field(default=None)
    source_modified_date_key: Optional[int] = Field(default=None)
    source_modified_date: Optional[date] = Field(default=None)
    dim_full_date: Optional[date] = Field(default=None)
    dim_year: Optional[int] = Field(default=None)
    dim_month: Optional[int] = Field(default=None)
    dim_day: Optional[int] = Field(default=None)
    dim_year_month: Optional[str] = Field(default=None)
    dim_quarter: Optional[int] = Field(default=None)
    series_type: str = Field(
        description="Series domain, e.g. rating or credit_metric.",
        examples=["credit_metric"],
    )
    series_name: str = Field(
        description="Series identifier/name.",
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
    values_by_company_id: dict[str, str | int | float | bool | datetime | None] = Field(
        description="Per-company value for this column.",
        examples=[{"company_a": "DE", "company_b": "CH"}],
    )


class CompanyCompareResultModel(BaseModel):
    """Comparison output containing selected companies and detected diffs."""

    companies: list[CompanyModel]
    diffs: list[CompanyComparisonDiffModel]
