"""Company service."""

from api.company.models import CompanyModel
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
