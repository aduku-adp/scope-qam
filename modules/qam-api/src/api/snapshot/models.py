"""Snapshot response models."""

from datetime import date
from datetime import datetime
from typing import Any
from typing import Optional

from pydantic import BaseModel, Field


class SnapshotModel(BaseModel):
    """Snapshot payload model backed by `snapshots.snap_company`."""

    snapshot_id: str = Field(
        description="Snapshot identifier.",
        examples=["3f21e9f3a856f188962bc1aac672fd2d"],
    )
    company_id: str = Field(
        description="Business identifier of the company.",
        examples=["company_b"],
    )
    snapshot_run_id: Optional[str] = None
    snapshot_created_at: Optional[datetime] = None
    snapshot_valid_from: Optional[datetime] = None
    snapshot_valid_to: Optional[datetime] = None
    assessment_key: Optional[str] = None
    record_hash: Optional[str] = None
    company_scd_key: Optional[str] = None
    company_name: Optional[str] = None
    country: Optional[str] = None
    corporate_sector: Optional[str] = None
    reporting_currency: Optional[str] = None
    accounting_principles: Optional[str] = None
    fiscal_year_end: Optional[str] = None
    industry_classification: Optional[str] = None
    industry_risk_score: Optional[str] = None
    industry_weight: Optional[str] = None
    segmentation_criteria: Optional[str] = None
    rating_methodologies_applied: Optional[str] = None
    document_version: Optional[int] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    is_active: Optional[bool] = None
    source_modified_date_key: Optional[int] = None
    source_modified_date: Optional[date] = None
    source_file_path: Optional[str] = None
    source_modified_at_utc: Optional[datetime] = None
    ingested_at: Optional[datetime] = None
    business_risk_score: Optional[str] = None
    financial_risk_score: Optional[str] = None
    blended_industry_risk_profile: Optional[str] = None
    competitive_positioning: Optional[str] = None
    market_share: Optional[str] = None
    diversification: Optional[str] = None
    operating_profitability: Optional[str] = None
    sector_company_specific_factors_1: Optional[str] = None
    sector_company_specific_factors_2: Optional[str] = None
    leverage: Optional[str] = None
    interest_cover: Optional[str] = None
    cash_flow_cover: Optional[str] = None
    liquidity_adjustment_notches: Optional[int] = None
    methodology_items: Optional[list[dict[str, Any]]] = None
    industry_risk_items: Optional[list[dict[str, Any]]] = None
    credit_metrics: Optional[list[dict[str, Any]]] = None
