"""Company service UT."""

# pylint: disable=invalid-name

from unittest.mock import create_autospec
import pytest

from api.company.models import CompanyModel
from api.providers.company_provider import CompanyProvider, NotFound
from api.company.service import CompanyService


@pytest.fixture(name="service")
def fix_service():
    """Instantiate company service with mocked provider."""
    return CompanyService(
        company_provider=create_autospec(CompanyProvider),
    )


@pytest.mark.parametrize(
    "companies",
    [
        [
            CompanyModel(
                company_scd_key="COMP001_v1",
                company_id="COMP001",
                company_name="ACME Corp",
                country="DE",
                document_version=1,
                is_active=True,
            ),
            CompanyModel(
                company_scd_key="COMP002_v1",
                company_id="COMP002",
                company_name="Globex",
                country="FR",
                document_version=1,
                is_active=True,
            ),
        ]
    ],
)
def test_list_all(service, companies):
    """Test that list_all returns active companies."""
    # GIVEN
    service.company_provider.list.return_value = companies

    # WHEN
    output = service.list_all()

    # THEN
    service.company_provider.list.assert_called_once_with(active_only=True)
    assert output == companies


def test_list_all_notfound(service):
    """Test list_all propagates NotFound."""
    # GIVEN
    service.company_provider.list.side_effect = NotFound

    # WHEN / THEN
    with pytest.raises(NotFound):
        service.list_all()


@pytest.mark.parametrize(
    "company_id, company",
    [
        (
            "ACME Corp",
            CompanyModel(
                company_scd_key="COMP001_v1",
                company_id="COMP001",
                company_name="ACME Corp",
                country="DE",
                document_version=1,
                is_active=True,
            ),
        )
    ],
)
def test_get_company(service, company_id, company):
    """Test that get_company returns correct company."""
    # GIVEN
    service.company_provider.get.return_value = company

    # WHEN
    output = service.get_company(company_id)

    # THEN
    service.company_provider.get.assert_called_once_with(company_id)
    assert output == company


def test_get_company_notfound(service):
    """Test that get_company propagates NotFound."""
    # GIVEN
    service.company_provider.get.side_effect = NotFound

    # WHEN / THEN
    with pytest.raises(NotFound):
        service.get_company("UnknownCompany")
