"""Company provider - Postgres implementation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Generator, Optional

import psycopg2
from psycopg2.extensions import connection as PgConnection
from psycopg2.extras import RealDictCursor
from api.company.models import CompanyModel


# Replace with your real API exceptions
class NotFound(Exception):
    pass


class Conflict(Exception):
    pass


@dataclass
class CompanyDB:
    """DB Company model (dims.dim_company)."""

    company_scd_key: str
    company_id: str
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


class CompanyProvider:
    """Company provider for dims.dim_company table."""

    def __init__(self, connection: PgConnection):
        self.conn = connection

    def list(self, active_only: bool = False) -> list[CompanyModel]:
        """List companies.

        Returns:
            A list of company model.
        """
        return [
            self._to_model(db_company) for db_company in self._list_all(active_only)
        ]

    def _to_model(self, db_company: CompanyDB) -> CompanyModel:
        """Return the company model."""
        return CompanyModel(
            company_scd_key=db_company.company_scd_key,
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
        )

    def _list_all(self, active_only: bool = True) -> list[CompanyDB]:
        """List companies."""
        query = """
            SELECT *
            FROM dims.dim_company
        """

        if active_only:
            query += " WHERE is_active = TRUE"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

        return [CompanyDB(**row) for row in rows]

    def get(self, company_id: str, active_only: bool = True) -> CompanyModel:
        """Get a company by company_id.

        Returns:
            A company model.
        """
        query = """
            SELECT *
            FROM dims.dim_company
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
