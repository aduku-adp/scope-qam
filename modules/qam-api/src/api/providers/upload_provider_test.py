"""Upload Provider UT."""

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from api.providers.upload_provider import NotFound, UploadProvider
from api.upload.models import UploadDetailsModel, UploadModel


UPLOAD_ROW = {
    "upload_id": "11111111-1111-1111-1111-111111111111",
    "run_id": "22222222-2222-2222-2222-222222222222",
    "pipeline_name": "extract_ratings_history",
    "source_file_path": "/tmp/corporates_A_1.xlsm",
    "source_filename": "corporates_A_1.xlsm",
    "source_modified_at_utc": datetime(2026, 2, 25),
    "file_size_bytes": 1234,
    "file_hash": "abc",
    "record_hash": "def",
    "document_version": 1,
    "status": "inserted",
    "warning_count": 0,
    "error_count": 0,
    "warning_message": None,
    "error_message": None,
    "ingested_at": datetime(2026, 2, 26),
}


@pytest.fixture(name="provider")
def fix_provider():
    connection = MagicMock()
    cursor = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor
    return UploadProvider(connection=connection)


def test_list_ok(provider):
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [UPLOAD_ROW]

    output = provider.list()

    assert output == [UploadModel(**UPLOAD_ROW)]
    query = cursor.execute.call_args[0][0].lower()
    assert "from obs.file_ingestion_events" in query


def test_get_ok(provider):
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = UPLOAD_ROW

    output = provider.get(UPLOAD_ROW["upload_id"])

    assert output == UploadModel(**UPLOAD_ROW)


def test_get_notfound(provider):
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = None

    with pytest.raises(NotFound):
        provider.get("missing")


def test_get_details_ok(provider):
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = UPLOAD_ROW
    cursor.fetchall.side_effect = [
        [{"rule_id": "r1", "severity": "error", "status": "failed", "violations": 1}],
        [{"lineage_id": "l1", "target_table": "raw.rating_assessments_history"}],
    ]

    output = provider.get_details(UPLOAD_ROW["upload_id"])

    assert isinstance(output, UploadDetailsModel)
    assert output.upload.upload_id == UPLOAD_ROW["upload_id"]
    assert len(output.data_quality_results) == 1
    assert len(output.lineage_events) == 1


def test_stats_ok(provider):
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = {
        "total_uploads": 3,
        "successful_uploads": 2,
        "failed_uploads": 1,
        "total_warnings": 1,
        "total_errors": 1,
        "avg_file_size_bytes": 100.0,
        "latest_upload_at": datetime(2026, 2, 26),
    }
    cursor.fetchall.return_value = [
        {"status": "inserted", "cnt": 2},
        {"status": "validation_failed", "cnt": 1},
    ]

    output = provider.stats()

    assert output.total_uploads == 3
    assert output.uploads_by_status == {"inserted": 2, "validation_failed": 1}

