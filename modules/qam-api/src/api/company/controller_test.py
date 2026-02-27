"""Company controller UT."""

# pylint: disable=invalid-name

from unittest.mock import create_autospec
import pytest
from fastapi.testclient import TestClient

from . import controller
from api.company.models import (
    CompanyCompareResultModel,
    CompanyComparisonDiffModel,
    CompanyHistoryPointModel,
    CompanyModel,
)
from api.company.service import CompanyService


@pytest.fixture(name="mock_service")
def fix_mock_service():
    """Set up service fixture."""
    return create_autospec(CompanyService)


@pytest.fixture(autouse=True)
def fix_controller(app, mock_service):
    """Build the controller filled with mocked dependencies."""
    app.add_controller("/api", controller.build, service=mock_service)


@pytest.mark.parametrize(
    "companies",
    [
        [
            CompanyModel(
                company_scd_key="COMP1_v1",
                company_id="COMP1",
                company_name="ACME Corp",
                country="DE",
                document_version=1,
                is_active=True,
            ),
            CompanyModel(
                company_scd_key="COMP2_v1",
                company_id="COMP2",
                company_name="Globex",
                country="FR",
                document_version=1,
                is_active=True,
            ),
        ]
    ],
)
def test_get_companies_ok(app, mock_service, companies):
    """Test that GET /companies returns list of companies."""
    # GIVEN
    mock_service.list_all.return_value = companies

    with TestClient(app) as client:
        # WHEN
        response = client.get("/api/companies")

        # THEN
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["data"] == [
            c.model_dump(exclude_none=True) for c in companies
        ]
        mock_service.list_all.assert_called_once()


def test_get_companies_notfound(app, mock_service):
    """Test GET /companies propagates NotFound."""
    mock_service.list_all.side_effect = Exception("Not Found")

    with TestClient(app) as client:
        response = client.get("/api/companies")

        assert response.status_code >= 400


def test_compare_companies_ok(app, mock_service):
    """Test GET /companies/compare returns compared companies."""
    companies = [
        CompanyModel(
            company_scd_key="COMP1_v1",
            company_id="COMP1",
            company_name="ACME Corp",
            country="DE",
            document_version=1,
            is_active=True,
        ),
        CompanyModel(
            company_scd_key="COMP2_v1",
            company_id="COMP2",
            company_name="Globex",
            country="FR",
            document_version=1,
            is_active=True,
        ),
    ]
    result = CompanyCompareResultModel(
        companies=companies,
        diffs=[
            CompanyComparisonDiffModel(
                column="country",
                values_by_company_id={"COMP1": "DE", "COMP2": "FR"},
            )
        ],
    )
    mock_service.compare_companies_with_diffs.return_value = result

    with TestClient(app) as client:
        response = client.get(
            "/api/companies/compare?company_ids=COMP1,COMP2&as_of_date=2025-01-01T00:00:00Z"
        )

        assert response.status_code == 200
        response_json = response.json()
        assert response_json["data"] == result.model_dump(exclude_none=True, mode="json")
        mock_service.compare_companies_with_diffs.assert_called_once()
        args, kwargs = mock_service.compare_companies_with_diffs.call_args
        assert args[0] == ["COMP1", "COMP2"]
        assert kwargs["as_of_date"] is not None


def test_compare_companies_bad_request(app, mock_service):
    """Test GET /companies/compare validates company_ids query param."""
    with TestClient(app) as client:
        response = client.get("/api/companies/compare?company_ids=,,")

        assert response.status_code == 400


def test_compare_companies_notfound(app, mock_service):
    """Test GET /companies/compare returns 404 on service failure."""
    mock_service.compare_companies_with_diffs.side_effect = Exception("Not Found")

    with TestClient(app) as client:
        response = client.get("/api/companies/compare?company_ids=UNKNOWN")

        assert response.status_code >= 400


@pytest.mark.parametrize(
    "company_id, company",
    [
        (
            "ACME Corp",
            CompanyModel(
                company_scd_key="COMP1_v1",
                company_id="COMP1",
                company_name="ACME Corp",
                country="DE",
                document_version=1,
                is_active=True,
            ),
        )
    ],
)
def test_get_company_ok(app, mock_service, company_id, company):
    """Test that GET /companies/{company_id} returns company."""
    # GIVEN
    mock_service.get_company.return_value = company

    with TestClient(app) as client:
        # WHEN
        response = client.get(f"/api/companies/{company_id}")

        # THEN
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["data"] == company.model_dump(exclude_none=True)
        mock_service.get_company.assert_called_once_with(company_id)


def test_get_company_notfound(app, mock_service):
    """Test GET /companies/{company_id} returns 404."""
    mock_service.get_company.side_effect = Exception("Not Found")

    with TestClient(app) as client:
        response = client.get("/api/companies/Unknown")

        assert response.status_code >= 400


@pytest.mark.parametrize(
    "company_id, versions",
    [
        (
            "COMP1",
            [
                CompanyModel(
                    company_scd_key="COMP1_v2",
                    company_id="COMP1",
                    company_name="ACME Corp",
                    country="DE",
                    document_version=2,
                    is_active=False,
                ),
                CompanyModel(
                    company_scd_key="COMP1_v1",
                    company_id="COMP1",
                    company_name="ACME Corp",
                    country="DE",
                    document_version=1,
                    is_active=True,
                ),
            ],
        )
    ],
)
def test_get_company_versions_ok(app, mock_service, company_id, versions):
    """Test that GET /companies/{company_id}/versions returns versions."""
    mock_service.get_company_versions.return_value = versions

    with TestClient(app) as client:
        response = client.get(f"/api/companies/{company_id}/versions")

        assert response.status_code == 200
        response_json = response.json()
        assert response_json["data"] == [
            v.model_dump(exclude_none=True) for v in versions
        ]
        mock_service.get_company_versions.assert_called_once_with(company_id)


def test_get_company_versions_notfound(app, mock_service):
    """Test GET /companies/{company_id}/versions returns 404."""
    mock_service.get_company_versions.side_effect = Exception("Not Found")

    with TestClient(app) as client:
        response = client.get("/api/companies/Unknown/versions")

        assert response.status_code >= 400


@pytest.mark.parametrize(
    "company_id, history",
    [
        (
            "COMP1",
            [
                CompanyHistoryPointModel(
                    timeseries_key="ts1",
                    company_id="COMP1",
                    document_version=1,
                    event_time="2024-01-01T00:00:00Z",
                    series_type="rating",
                    series_name="business_risk_score",
                    series_value="B",
                ),
                CompanyHistoryPointModel(
                    timeseries_key="ts2",
                    company_id="COMP1",
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
def test_get_company_history_ok(app, mock_service, company_id, history):
    """Test that GET /companies/{company_id}/history returns time-series data."""
    mock_service.get_company_history.return_value = history

    with TestClient(app) as client:
        response = client.get(f"/api/companies/{company_id}/history")

        assert response.status_code == 200
        response_json = response.json()
        assert response_json["data"] == [
            h.model_dump(exclude_none=True, mode="json") for h in history
        ]
        mock_service.get_company_history.assert_called_once_with(
            company_id,
            series_type=None,
            series_name=None,
            year_label=None,
        )


def test_get_company_history_notfound(app, mock_service):
    """Test GET /companies/{company_id}/history returns 404."""
    mock_service.get_company_history.side_effect = Exception("Not Found")

    with TestClient(app) as client:
        response = client.get("/api/companies/Unknown/history")

        assert response.status_code >= 400


def test_get_company_history_with_filters_ok(app, mock_service):
    """Test GET /companies/{company_id}/history forwards filter query params."""
    history = [
        CompanyHistoryPointModel(
            timeseries_key="ts1",
            company_id="COMP1",
            document_version=1,
            event_time="2024-01-01T00:00:00Z",
            series_type="rating",
            series_name="business_risk_score",
            series_value="B",
        )
    ]
    mock_service.get_company_history.return_value = history

    with TestClient(app) as client:
        response = client.get(
            "/api/companies/COMP1/history?series_type=rating&series_name=business_risk_score&year_label=2025E"
        )

        assert response.status_code == 200
        response_json = response.json()
        assert response_json["data"] == [
            h.model_dump(exclude_none=True, mode="json") for h in history
        ]
        mock_service.get_company_history.assert_called_once_with(
            "COMP1",
            series_type="rating",
            series_name="business_risk_score",
            year_label="2025E",
        )
