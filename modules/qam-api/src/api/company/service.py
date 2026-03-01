"""Company service."""

from datetime import datetime
import json

from api.company.models import CompanyComparisonDiffModel, CompanyHistoryPointModel, CompanyModel
from api.providers.company_provider import CompanyProvider


class CompanyService:
    """Application service for company read/query operations."""

    def __init__(
        self,
        company_provider: CompanyProvider,
    ):
        """Instantiate the service with its persistence provider."""
        self.company_provider = company_provider

    def list_all(self, active_only: bool = True) -> list[CompanyModel]:
        """List companies, optionally restricted to active rows."""
        return self.company_provider.list(active_only=active_only)

    def get_company(self, company_id: str) -> CompanyModel:
        """Get one company record (latest active by default in provider)."""
        company = self.company_provider.get(company_id)

        return company

    def get_company_versions(self, company_id: str) -> list[CompanyModel]:
        """Get all versions for a company."""
        return self.company_provider.get_versions(company_id)

    def compare_companies(
        self, company_ids: list[str], as_of_date: datetime | None = None
    ) -> list[CompanyModel]:
        """Return comparable company rows at latest or point-in-time cutoff."""
        return self.company_provider.compare(company_ids, as_of_date=as_of_date)

    def compare_companies_with_diffs(
        self, company_ids: list[str], as_of_date: datetime | None = None
    ) -> list[CompanyComparisonDiffModel]:
        """Return only column-level differences across compared company rows."""
        companies = self.compare_companies(company_ids, as_of_date=as_of_date)

        excluded_columns = {
            "rep_company_key",
            "assessment_key",
            "record_hash",
            "company_scd_key",
        }
        comparable_columns = [
            field_name
            for field_name in CompanyModel.model_fields
            if field_name not in excluded_columns
        ]

        diffs: list[CompanyComparisonDiffModel] = []
        for column in comparable_columns:
            # Normalize complex values (e.g. datetimes/lists) for stable equality checks.
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

        return diffs

    def get_company_history(
        self,
        company_id: str,
        column_name: str,
        metric_name: str | None = None,
        year_label: str | None = None,
    ) -> list[CompanyHistoryPointModel]:
        """Return normalized company history points using 3-level filters."""
        return self.company_provider.get_history(
            company_id,
            column_name=column_name,
            metric_name=metric_name,
            year_label=year_label,
        )
