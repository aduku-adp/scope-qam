"""Snapshot Provider UT."""

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from api.providers.snapshot_provider import NotFound, SnapshotProvider
from api.snapshot.models import SnapshotModel


SNAPSHOT_ROW = {
    "snapshot_id": "COMP1_v1",
    "company_id": "COMP1",
    "company_name": "ACME",
    "country": "DE",
    "corporate_sector": "Industrial",
    "reporting_currency": "EUR",
    "accounting_principles": "IFRS",
    "fiscal_year_end": "12-31",
    "industry_classification": "Manufacturing",
    "industry_risk_score": "BBB",
    "industry_weight": "1.0",
    "segmentation_criteria": "Enterprise",
    "rating_methodologies_applied": "Corporate Rating v1",
    "document_version": 1,
    "start_at": datetime(2024, 1, 1),
    "end_at": None,
    "is_active": True,
}


@pytest.fixture(name="provider")
def fix_provider():
    connection = MagicMock()
    cursor = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor
    return SnapshotProvider(connection=connection)


def test_list_ok(provider):
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [SNAPSHOT_ROW]

    output = provider.list(company_id="COMP1", country="DE")

    assert output == [SnapshotModel(**SNAPSHOT_ROW)]
    cursor.execute.assert_called_once()
    query = cursor.execute.call_args[0][0].lower()
    assert "from snapshots.snap_company" in query
    assert "dbt_scd_id is not null" in query
    assert "company_id = %s" in query
    assert "country = %s" in query


def test_get_ok(provider):
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = SNAPSHOT_ROW

    output = provider.get("COMP1_v1")

    assert output == SnapshotModel(**SNAPSHOT_ROW)


def test_get_notfound(provider):
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = None

    with pytest.raises(NotFound):
        provider.get("UNKNOWN")


def test_latest_ok(provider):
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [SNAPSHOT_ROW]

    output = provider.latest()

    assert output == [SnapshotModel(**SNAPSHOT_ROW)]
    cursor.execute.assert_called_once()
    query = cursor.execute.call_args[0][0].lower()
    assert "select distinct on (company_id)" in query
    assert "from snapshots.snap_company" in query
    assert "where dbt_valid_to is null" in query
    assert "and dbt_scd_id is not null" in query
