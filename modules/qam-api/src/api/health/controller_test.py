"""Health controller UT."""

from unittest.mock import create_autospec

import pytest
from fastapi.testclient import TestClient

from api.health import controller
from api.health.models import HealthModel
from api.health.service import HealthService


@pytest.fixture(name="mock_service")
def fix_mock_service():
    return create_autospec(HealthService)


@pytest.fixture(autouse=True)
def fix_controller(app, mock_service):
    app.add_controller("/api", controller.build, service=mock_service)


def test_health_ok(app, mock_service):
    mock_service.get_health.return_value = HealthModel(
        healthy=True,
        database_ok=True,
        corporates_dir_ok=True,
        corporates_dir_path="/data/corporates",
        corporates_files_count=5,
        database_message="ok",
        corporates_dir_message="ok",
    )

    with TestClient(app) as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["data"]["healthy"] is True


def test_health_unhealthy_returns_503(app, mock_service):
    mock_service.get_health.return_value = HealthModel(
        healthy=False,
        database_ok=False,
        corporates_dir_ok=True,
        corporates_dir_path="/data/corporates",
        corporates_files_count=5,
        database_message="db down",
        corporates_dir_message="ok",
    )

    with TestClient(app) as client:
        response = client.get("/api/health")
        assert response.status_code == 503
        assert response.json()["data"]["healthy"] is False

