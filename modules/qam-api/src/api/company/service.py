"""Company service."""

from datetime import datetime
import json

from api.company.models import (
    CompanyCompareResultModel,
    CompanyComparisonDiffModel,
    CompanyHistoryPointModel,
    CompanyModel,
)
from api.providers.company_provider import CompanyProvider


class CompanyService:
    """Company service."""

    def __init__(
        self,
        company_provider: CompanyProvider,
    ):
        """Initialize the instance."""
        self.company_provider = company_provider

    def list_all(self, active_only=True) -> list[CompanyModel]:
        """List all the latest companies."""
        return self.company_provider.list(active_only=active_only)

    def get_company(self, company_id: str) -> CompanyModel:
        """Get a latest company details"""
        company = self.company_provider.get(company_id)

        return company

    def get_company_versions(self, company_id: str) -> list[CompanyModel]:
        """Get all versions for a company."""
        return self.company_provider.get_versions(company_id)

    def compare_companies(
        self, company_ids: list[str], as_of_date: datetime | None = None
    ) -> list[CompanyModel]:
        """Compare multiple companies at latest or at a specific point in time."""
        return self.company_provider.compare(company_ids, as_of_date=as_of_date)

    def compare_companies_with_diffs(
        self, company_ids: list[str], as_of_date: datetime | None = None
    ) -> CompanyCompareResultModel:
        """Compare companies and return differing columns across returned rows."""
        companies = self.compare_companies(company_ids, as_of_date=as_of_date)

        comparable_columns = [
            "company_name",
            "country",
            "corporate_sector",
            "reporting_currency",
            "accounting_principles",
            "fiscal_year_end",
            "industry_classification",
            "industry_risk_score",
            "industry_weight",
            "segmentation_criteria",
            "rating_methodologies_applied",
            "document_version",
            "end_at",
            "is_active",
        ]

        diffs: list[CompanyComparisonDiffModel] = []
        for column in comparable_columns:
            values = {c.company_id: getattr(c, column) for c in companies}
            normalized = {
                json.dumps(value, default=str, sort_keys=True) for value in values.values()
            }
            if len(normalized) > 1:
                diffs.append(
                    CompanyComparisonDiffModel(
                        column=column,
                        values_by_company_id=values,
                    )
                )

        return CompanyCompareResultModel(companies=companies, diffs=diffs)

    def get_company_history(
        self,
        company_id: str,
        series_type: str | None = None,
        series_name: str | None = None,
        year_label: str | None = None,
    ) -> list[CompanyHistoryPointModel]:
        """Get time-series data for company analysis."""
        return self.company_provider.get_history(
            company_id,
            series_type=series_type,
            series_name=series_name,
            year_label=year_label,
        )
