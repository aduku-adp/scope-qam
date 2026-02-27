"""Upload service UT."""

from unittest.mock import create_autospec

import pytest

from api.providers.upload_provider import UploadProvider
from api.upload.models import UploadDetailsModel, UploadModel, UploadStatsModel
from api.upload.service import UploadService


@pytest.fixture(name="service")
def fix_service():
    return UploadService(upload_provider=create_autospec(UploadProvider))


def test_list_uploads(service):
    uploads = [UploadModel(upload_id="u1")]
    service.upload_provider.list.return_value = uploads

    output = service.list_uploads()

    service.upload_provider.list.assert_called_once()
    assert output == uploads


def test_get_upload_details(service):
    details = UploadDetailsModel(upload=UploadModel(upload_id="u1"))
    service.upload_provider.get_details.return_value = details

    output = service.get_upload_details("u1")

    service.upload_provider.get_details.assert_called_once_with("u1")
    assert output == details


def test_get_upload_file_info(service):
    service.upload_provider.get_file_info.return_value = ("/tmp/a.xlsm", "a.xlsm")

    output = service.get_upload_file_info("u1")

    service.upload_provider.get_file_info.assert_called_once_with("u1")
    assert output == ("/tmp/a.xlsm", "a.xlsm")


def test_get_upload_stats(service):
    stats = UploadStatsModel(
        total_uploads=1,
        successful_uploads=1,
        failed_uploads=0,
        total_warnings=0,
        total_errors=0,
    )
    service.upload_provider.stats.return_value = stats

    output = service.get_upload_stats()

    service.upload_provider.stats.assert_called_once()
    assert output == stats

