"""Pydantic schema validation for extracted rating payloads."""

from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr


class EntityInformation(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    name: StrictStr = Field(min_length=1)
    corporate_sector: StrictStr = Field(min_length=1)
    industry: StrictStr = Field(min_length=1)
    country_of_origin: StrictStr = Field(min_length=1)
    reporting_currency: StrictStr = Field(min_length=1)
    accounting_principles: StrictStr = Field(min_length=1)
    fiscal_year_end: StrictStr = Field(min_length=1)


class Methodology(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    rating_methodologies_applied: list[StrictStr] = Field(min_length=1)


class IndustryRisk(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    industry_classification: StrictStr = Field(min_length=1)
    industry_risk_score: StrictStr = Field(min_length=1)
    industry_weight: StrictFloat | None = None
    segmentation_criteria: StrictStr | None = None


class BusinessRiskComponents(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    blended_industry_risk_profile: StrictStr = Field(min_length=1)
    competitive_positioning: StrictStr = Field(min_length=1)
    market_share: StrictStr = Field(min_length=1)
    diversification: StrictStr = Field(min_length=1)
    operating_profitability: StrictStr = Field(min_length=1)
    sector_company_specific_factors_1: StrictStr | None = None
    sector_company_specific_factors_2: StrictStr | None = None


class BusinessRiskProfile(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    overall_score: StrictStr = Field(min_length=1)
    components: BusinessRiskComponents


class FinancialRiskComponents(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    leverage: StrictStr = Field(min_length=1)
    interest_cover: StrictStr = Field(min_length=1)
    cash_flow_cover: StrictStr = Field(min_length=1)
    liquidity_adjustment_notches: StrictInt | None = None


class FinancialRiskProfile(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    overall_score: StrictStr = Field(min_length=1)
    components: FinancialRiskComponents


class CreditMetricValue(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    year: StrictStr = Field(min_length=1)
    value: StrictFloat | None = None


class CreditMetric(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    metric: StrictStr = Field(min_length=1)
    values: list[CreditMetricValue]
    locked: bool


class RatingAssessmentPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    entity_information: EntityInformation
    methodology: Methodology
    industry_risk: IndustryRisk
    business_risk_profile: BusinessRiskProfile
    financial_risk_profile: FinancialRiskProfile
    credit_metrics: list[CreditMetric]
    rating_date: date | None = None


def validate_extracted_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize extracted payload using Pydantic."""
    return RatingAssessmentPayload.model_validate(payload).model_dump()
