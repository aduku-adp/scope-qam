"""Company controller UT."""

# pylint: disable=invalid-name

from unittest.mock import create_autospec
import pytest
from fastapi.testclient import TestClient

from . import controller
from api.company.models import CompanyModel
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
