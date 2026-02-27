"""Common models for payload and response."""

from typing import Optional

# pylint: disable=invalid-name, no-self-argument
from pydantic import BaseModel, Field, model_validator


from datetime import datetime


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
