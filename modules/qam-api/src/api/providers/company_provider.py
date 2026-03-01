"""Company provider - Postgres implementation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from psycopg2.extensions import connection as PgConnection
from psycopg2.extras import RealDictCursor
from api.company.models import CompanyHistoryPointModel, CompanyModel


class NotFound(Exception):
    """Raised when a requested company resource does not exist."""

    pass


class Conflict(Exception):
    """Raised when a write operation would violate data consistency rules."""

    pass


@dataclass
class CompanyDB:
    """DB Company model (reports.rep_company)."""

    company_id: str
    rep_company_key: Optional[str] = None
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
    is_active: Optional[bool] = True
    source_modified_date_key: Optional[int] = None
    source_modified_date: Optional[datetime] = None
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
    credit_metrics: Optional[list[dict]] = None


class CompanyProvider:
    """Company provider for reports.rep_company table."""

    def __init__(self, connection: PgConnection):
        """Instantiate provider with an open PostgreSQL connection."""
        self.conn = connection

    def list(self, active_only: bool = False) -> list[CompanyModel]:
        """List companies from `reports.rep_company`."""
        return [
            self._to_model(db_company) for db_company in self._list_all(active_only)
        ]

    def _to_model(self, db_company: CompanyDB) -> CompanyModel:
        """Map one DB row object to the API company model."""
        return CompanyModel(
            rep_company_key=db_company.rep_company_key,
            company_id=db_company.company_id,
            company_name=db_company.company_name,
            country=db_company.country,
            corporate_sector=db_company.corporate_sector,
            reporting_currency=db_company.reporting_currency,
            accounting_principles=db_company.accounting_principles,
            fiscal_year_end=db_company.fiscal_year_end,
            industry_classification=db_company.industry_classification,
            industry_risk_score=db_company.industry_risk_score,
            industry_weight=db_company.industry_weight,
            segmentation_criteria=db_company.segmentation_criteria,
            rating_methodologies_applied=db_company.rating_methodologies_applied,
            document_version=db_company.document_version,
            start_at=db_company.start_at,
            end_at=db_company.end_at,
            is_active=db_company.is_active,
            source_modified_date_key=db_company.source_modified_date_key,
            source_modified_date=db_company.source_modified_date,
            source_file_path=db_company.source_file_path,
            source_modified_at_utc=db_company.source_modified_at_utc,
            ingested_at=db_company.ingested_at,
            business_risk_score=db_company.business_risk_score,
            financial_risk_score=db_company.financial_risk_score,
            blended_industry_risk_profile=db_company.blended_industry_risk_profile,
            competitive_positioning=db_company.competitive_positioning,
            market_share=db_company.market_share,
            diversification=db_company.diversification,
            operating_profitability=db_company.operating_profitability,
            sector_company_specific_factors_1=db_company.sector_company_specific_factors_1,
            sector_company_specific_factors_2=db_company.sector_company_specific_factors_2,
            leverage=db_company.leverage,
            interest_cover=db_company.interest_cover,
            cash_flow_cover=db_company.cash_flow_cover,
            liquidity_adjustment_notches=db_company.liquidity_adjustment_notches,
            credit_metrics=db_company.credit_metrics,
        )

    def _list_all(self, active_only: bool = True) -> list[CompanyDB]:
        """Query all companies from reports table with optional active filter."""
        query = """
            SELECT *
            FROM reports.rep_company
        """

        if active_only:
            query += " WHERE is_active = TRUE"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

        return [CompanyDB(**row) for row in rows]

    def get(self, company_id: str, active_only: bool = True) -> CompanyModel:
        """Get one company by id, optionally restricted to active version."""
        query = """
            SELECT *
            FROM reports.rep_company
            WHERE company_id = %s
        """

        if active_only:
            query += " AND is_active = TRUE"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (company_id,))
            row = cur.fetchone()

        if not row:
            raise NotFound(f"Company {company_id} not found")

        db_company = CompanyDB(**row)

        return self._to_model(db_company)

    def get_versions(self, company_id: str) -> list[CompanyModel]:
        """Get all company versions ordered from latest to oldest."""
        query = """
            SELECT *
            FROM reports.rep_company
            WHERE company_id = %s
            ORDER BY document_version DESC, start_at DESC
        """

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (company_id,))
            rows = cur.fetchall()

        if not rows:
            raise NotFound(f"Company {company_id} not found")

        return [self._to_model(CompanyDB(**row)) for row in rows]

    def compare(self, company_ids: list[str], as_of_date: datetime | None = None) -> list[CompanyModel]:
        """Fetch one row per company for comparison at latest or as-of timestamp."""
        select_cols = """
            rep_company_key,
            assessment_key,
            record_hash,
            company_scd_key,
            company_id,
            company_name,
            country,
            corporate_sector,
            reporting_currency,
            accounting_principles,
            fiscal_year_end,
            industry_classification,
            industry_risk_score,
            industry_weight,
            segmentation_criteria,
            rating_methodologies_applied,
            document_version,
            start_at,
            end_at,
            is_active,
            source_modified_date_key,
            source_modified_date,
            source_file_path,
            source_modified_at_utc,
            ingested_at,
            business_risk_score,
            financial_risk_score,
            blended_industry_risk_profile,
            competitive_positioning,
            market_share,
            diversification,
            operating_profitability,
            sector_company_specific_factors_1,
            sector_company_specific_factors_2,
            leverage,
            interest_cover,
            cash_flow_cover,
            liquidity_adjustment_notches,
            credit_metrics
        """
        if as_of_date is None:
            query = """
                with ranked as (
                    select
                        *,
                        row_number() over (
                            partition by company_id
                            order by start_at desc, document_version desc
                        ) as rn
                    from reports.rep_company
                    where company_id = any(%s)
                      and is_active = true
                )
                select
                    """ + select_cols + """
                from ranked
                where rn = 1
                order by company_id
            """
            params = (company_ids,)
        else:
            query = """
                with ranked as (
                    select
                        *,
                        row_number() over (
                            partition by company_id
                            order by start_at desc, document_version desc
                        ) as rn
                    from reports.rep_company
                    where company_id = any(%s)
                      and start_at <= %s
                      and (end_at is null or end_at > %s)
                )
                select
                    """ + select_cols + """
                from ranked
                where rn = 1
                order by company_id
            """
            params = (company_ids, as_of_date, as_of_date)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            rows = cur.fetchall()

        if not rows:
            raise NotFound("No companies found for comparison")

        return [self._to_model(CompanyDB(**row)) for row in rows]

    def get_history(
        self,
        company_id: str,
        column_name: str,
        metric_name: str | None = None,
        year_label: str | None = None,
    ) -> list[CompanyHistoryPointModel]:
        """Fetch normalized company time-series points with 3-level filters."""
        query = """
            SELECT
                timeseries_key,
                company_id,
                document_version,
                event_time,
                column_name,
                metric_name,
                series_value,
                year_label,
                is_estimate
            FROM facts.fct_company_timeseries
            WHERE company_id = %s
              AND column_name = %s
        """
        params: list[str] = [company_id, column_name]

        if metric_name:
            query += " AND metric_name = %s"
            params.append(metric_name)
        if year_label:
            query += " AND year_label = %s"
            params.append(year_label)

        query += " ORDER BY column_name ASC, metric_name ASC, document_version ASC, event_time ASC, year_label ASC"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, tuple(params))
            rows = cur.fetchall()

        if not rows:
            raise NotFound(f"Company {company_id} not found")

        return [CompanyHistoryPointModel(**row) for row in rows]
