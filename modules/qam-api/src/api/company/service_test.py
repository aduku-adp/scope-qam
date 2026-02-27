"""Company service UT."""

# pylint: disable=invalid-name

from datetime import datetime
from unittest.mock import create_autospec
import pytest

from api.company.models import CompanyHistoryPointModel, CompanyModel
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


@pytest.mark.parametrize(
    "company_id, versions",
    [
        (
            "COMP001",
            [
                CompanyModel(
                    company_scd_key="COMP001_v2",
                    company_id="COMP001",
                    company_name="ACME Corp",
                    country="DE",
                    document_version=2,
                    is_active=False,
                ),
                CompanyModel(
                    company_scd_key="COMP001_v1",
                    company_id="COMP001",
                    company_name="ACME Corp",
                    country="DE",
                    document_version=1,
                    is_active=True,
                ),
            ],
        )
    ],
)
def test_get_company_versions(service, company_id, versions):
    """Test that get_company_versions returns all versions."""
    service.company_provider.get_versions.return_value = versions

    output = service.get_company_versions(company_id)

    service.company_provider.get_versions.assert_called_once_with(company_id)
    assert output == versions


def test_get_company_versions_notfound(service):
    """Test that get_company_versions propagates NotFound."""
    service.company_provider.get_versions.side_effect = NotFound

    with pytest.raises(NotFound):
        service.get_company_versions("UnknownCompany")


def test_compare_companies(service):
    """Test compare_companies forwards query args to provider."""
    companies = [
        CompanyModel(
            company_scd_key="COMP001_v1",
            company_id="COMP001",
            company_name="ACME Corp",
            country="DE",
            document_version=1,
            is_active=True,
        )
    ]
    as_of_date = datetime(2025, 1, 1)
    service.company_provider.compare.return_value = companies

    output = service.compare_companies(["COMP001"], as_of_date=as_of_date)

    service.company_provider.compare.assert_called_once_with(
        ["COMP001"], as_of_date=as_of_date
    )
    assert output == companies


def test_compare_companies_notfound(service):
    """Test compare_companies propagates NotFound."""
    service.company_provider.compare.side_effect = NotFound

    with pytest.raises(NotFound):
        service.compare_companies(["UnknownCompany"])


def test_compare_companies_with_diffs(service):
    """Test compare_companies_with_diffs returns compared companies and changed columns."""
    companies = [
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
    service.company_provider.compare.return_value = companies

    output = service.compare_companies_with_diffs(["COMP001", "COMP002"])

    assert len(output.companies) == 2
    assert any(diff.column == "country" for diff in output.diffs)


@pytest.mark.parametrize(
    "company_id, history",
    [
        (
            "COMP001",
            [
                CompanyHistoryPointModel(
                    timeseries_key="ts1",
                    company_id="COMP001",
                    document_version=1,
                    event_time="2024-01-01T00:00:00Z",
                    series_type="rating",
                    series_name="business_risk_score",
                    series_value="B",
                ),
                CompanyHistoryPointModel(
                    timeseries_key="ts2",
                    company_id="COMP001",
                    document_version=2,
                    event_time="2025-01-01T00:00:00Z",
                    series_type="credit_metric",
                    series_name="scope_adjusted_debt_ebitda",
                    series_value="18.49",
                    year_label="2025E",
                    is_estimate=True,
                ),
            ],
        )
    ],
)
def test_get_company_history(service, company_id, history):
    """Test that get_company_history returns time-series data."""
    service.company_provider.get_history.return_value = history

    output = service.get_company_history(company_id)

    service.company_provider.get_history.assert_called_once_with(
        company_id,
        series_type=None,
        series_name=None,
        year_label=None,
    )
    assert output == history


def test_get_company_history_notfound(service):
    """Test that get_company_history propagates NotFound."""
    service.company_provider.get_history.side_effect = NotFound

    with pytest.raises(NotFound):
        service.get_company_history("UnknownCompany")


def test_get_company_history_with_filters(service):
    """Test get_company_history forwards optional filters to provider."""
    expected = [
        CompanyHistoryPointModel(
            timeseries_key="ts1",
            company_id="COMP001",
            document_version=1,
            event_time="2024-01-01T00:00:00Z",
            series_type="rating",
            series_name="business_risk_score",
            series_value="B",
        )
    ]
    service.company_provider.get_history.return_value = expected

    output = service.get_company_history(
        "COMP001",
        series_type="rating",
        series_name="business_risk_score",
        year_label="2025E",
    )

    service.company_provider.get_history.assert_called_once_with(
        "COMP001",
        series_type="rating",
        series_name="business_risk_score",
        year_label="2025E",
    )
    assert output == expected
