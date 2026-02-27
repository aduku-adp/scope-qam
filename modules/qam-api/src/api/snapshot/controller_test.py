"""Snapshot controller UT."""

from unittest.mock import create_autospec

import pytest
from fastapi.testclient import TestClient

from api.snapshot import controller
from api.snapshot.models import SnapshotModel
from api.snapshot.service import SnapshotService


@pytest.fixture(name="mock_service")
def fix_mock_service():
    return create_autospec(SnapshotService)


@pytest.fixture(autouse=True)
def fix_controller(app, mock_service):
    app.add_controller("/api", controller.build, service=mock_service)


def test_list_snapshots_ok(app, mock_service):
    snapshots = [
        SnapshotModel(
            snapshot_id="COMP1_v1",
            company_id="COMP1",
            company_name="ACME",
            document_version=1,
            is_active=True,
        )
    ]
    mock_service.list_snapshots.return_value = snapshots

    with TestClient(app) as client:
        response = client.get("/api/snapshots?company_id=COMP1")

        assert response.status_code == 200
        assert response.json()["data"] == [
            s.model_dump(exclude_none=True, mode="json") for s in snapshots
        ]


def test_get_snapshot_ok(app, mock_service):
    snapshot = SnapshotModel(
        snapshot_id="COMP1_v1",
        company_id="COMP1",
        company_name="ACME",
        document_version=1,
        is_active=True,
    )
    mock_service.get_snapshot.return_value = snapshot

    with TestClient(app) as client:
        response = client.get("/api/snapshots/COMP1_v1")

        assert response.status_code == 200
        assert response.json()["data"] == snapshot.model_dump(exclude_none=True, mode="json")


def test_get_snapshot_notfound(app, mock_service):
    mock_service.get_snapshot.side_effect = Exception("Not Found")

    with TestClient(app) as client:
        response = client.get("/api/snapshots/UNKNOWN")

        assert response.status_code >= 400


def test_latest_snapshots_ok(app, mock_service):
    snapshots = [
        SnapshotModel(
            snapshot_id="COMP1_v1",
            company_id="COMP1",
            company_name="ACME",
            document_version=1,
            is_active=True,
        )
    ]
    mock_service.get_latest_snapshots.return_value = snapshots

    with TestClient(app) as client:
        response = client.get("/api/snapshots/latest")

        assert response.status_code == 200
        assert response.json()["data"] == [
            s.model_dump(exclude_none=True, mode="json") for s in snapshots
        ]

