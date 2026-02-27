"""Upload controller UT."""

from pathlib import Path
from unittest.mock import create_autospec

import pytest
from fastapi.testclient import TestClient

from api.upload import controller
from api.upload.models import UploadDetailsModel, UploadModel, UploadStatsModel
from api.upload.service import UploadService


@pytest.fixture(name="mock_service")
def fix_mock_service():
    return create_autospec(UploadService)


@pytest.fixture(autouse=True)
def fix_controller(app, mock_service):
    app.add_controller("/api", controller.build, service=mock_service)


def test_list_uploads_ok(app, mock_service):
    uploads = [UploadModel(upload_id="u1", source_filename="a.xlsm")]
    mock_service.list_uploads.return_value = uploads

    with TestClient(app) as client:
        response = client.get("/api/uploads")
        assert response.status_code == 200
        assert response.json()["data"] == [u.model_dump(exclude_none=True, mode="json") for u in uploads]


def test_get_upload_details_ok(app, mock_service):
    details = UploadDetailsModel(upload=UploadModel(upload_id="u1"))
    mock_service.get_upload_details.return_value = details

    with TestClient(app) as client:
        response = client.get("/api/uploads/u1/details")
        assert response.status_code == 200
        assert response.json()["data"] == details.model_dump(exclude_none=True, mode="json")


def test_get_upload_stats_ok(app, mock_service):
    stats = UploadStatsModel(
        total_uploads=1,
        successful_uploads=1,
        failed_uploads=0,
        total_warnings=0,
        total_errors=0,
    )
    mock_service.get_upload_stats.return_value = stats

    with TestClient(app) as client:
        response = client.get("/api/uploads/stats")
        assert response.status_code == 200
        assert response.json()["data"] == stats.model_dump(exclude_none=True, mode="json")


def test_download_upload_file_ok(app, mock_service, tmp_path: Path):
    source_file = tmp_path / "a.xlsm"
    source_file.write_text("dummy")
    mock_service.get_upload_file_info.return_value = (str(source_file), source_file.name)

    with TestClient(app) as client:
        response = client.get("/api/uploads/u1/file")
        assert response.status_code == 200
        assert "attachment; filename=\"a.xlsm\"" in response.headers.get("content-disposition", "")

