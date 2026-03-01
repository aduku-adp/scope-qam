"""Company Provider UT."""

# pylint: disable=invalid-name, protected-access

from unittest.mock import MagicMock
from datetime import datetime

import pytest

from api.company.models import CompanyModel
from api.providers.company_provider import CompanyProvider, NotFound


COMPANY_1_ROW = {
    "company_scd_key": "COMP1_v1",
    "company_id": "COMP1",
    "company_name": "ACME",
    "country": "DE",
    "corporate_sector": "Industrial",
    "reporting_currency": "EUR",
    "accounting_principles": "IFRS",
    "fiscal_year_end": "12-31",
    "industry_classification": "Manufacturing",
    "industry_risk_score": "Medium",
    "industry_weight": "0.75",
    "segmentation_criteria": "Enterprise",
    "rating_methodologies_applied": "Corporate Rating v1",
    "document_version": 1,
    "start_at": datetime(2024, 1, 1),
    "end_at": None,
    "is_active": True,
}

COMPANY_2_ROW = {
    **COMPANY_1_ROW,
    "company_scd_key": "COMP1_v2",
    "company_id": "COMP1",
    "document_version": 2,
    "start_at": datetime(2025, 1, 1),
    "end_at": datetime(2025, 12, 31),
    "is_active": False,
}


@pytest.fixture(name="provider")
def fix_provider():
    """Instantiate provider with mocked psycopg2 connection."""
    connection = MagicMock()
    cursor = MagicMock()

    connection.cursor.return_value.__enter__.return_value = cursor

    provider = CompanyProvider(connection=connection)

    return provider


# -- list tests


def test_list_ok(provider):
    """Test list returns all companies."""
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [COMPANY_1_ROW, COMPANY_2_ROW]

    output = provider.list()

    assert output == [
        CompanyModel(**COMPANY_1_ROW),
        CompanyModel(**COMPANY_2_ROW),
    ]


def test_list_active_only(provider):
    """Test list with active_only=True filters correctly."""
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [COMPANY_1_ROW]

    output = provider.list(active_only=True)

    assert output == [CompanyModel(**COMPANY_1_ROW)]

    executed_query = cursor.execute.call_args[0][0]
    assert "WHERE is_active = TRUE" in executed_query


# -- get tests


def test_get_ok(provider):
    """Test get returns expected company."""
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = COMPANY_1_ROW

    output = provider.get("COMP1")

    assert output == CompanyModel(**COMPANY_1_ROW)

    cursor.execute.assert_called_once()
    assert cursor.execute.call_args[0][1] == ("COMP1",)
    query = cursor.execute.call_args[0][0]
    assert "FROM reports.rep_company" in query
    assert "WHERE company_id = %s" in query


def test_get_notfound(provider):
    """Test get raises NotFound if company does not exist."""
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = None

    with pytest.raises(NotFound):
        provider.get("UNKNOWN")


def test_get_versions_ok(provider):
    """Test get_versions returns all versions for a company."""
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [COMPANY_2_ROW, COMPANY_1_ROW]

    output = provider.get_versions("COMP1")

    assert output == [
        CompanyModel(**COMPANY_2_ROW),
        CompanyModel(**COMPANY_1_ROW),
    ]
    cursor.execute.assert_called_once()
    assert cursor.execute.call_args[0][1] == ("COMP1",)
    query = cursor.execute.call_args[0][0]
    assert "FROM reports.rep_company" in query
    assert "WHERE company_id = %s" in query
    assert "ORDER BY document_version DESC" in query


def test_get_versions_notfound(provider):
    """Test get_versions raises NotFound if company does not exist."""
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = []

    with pytest.raises(NotFound):
        provider.get_versions("UNKNOWN")


def test_compare_ok_latest(provider):
    """Test compare returns latest active rows for requested companies."""
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [COMPANY_1_ROW]

    output = provider.compare(["COMP1", "COMP2"])

    assert output == [CompanyModel(**COMPANY_1_ROW)]
    cursor.execute.assert_called_once()
    assert cursor.execute.call_args[0][1] == (["COMP1", "COMP2"],)
    query = cursor.execute.call_args[0][0].lower()
    assert "from reports.rep_company" in query
    assert "company_id = any(%s)" in query
    assert "is_active = true" in query


def test_compare_ok_as_of_date(provider):
    """Test compare applies as_of_date snapshot filtering."""
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [COMPANY_1_ROW]
    as_of_date = datetime(2025, 1, 1)

    output = provider.compare(["COMP1"], as_of_date=as_of_date)

    assert output == [CompanyModel(**COMPANY_1_ROW)]
    cursor.execute.assert_called_once()
    assert cursor.execute.call_args[0][1] == (["COMP1"], as_of_date, as_of_date)
    query = cursor.execute.call_args[0][0].lower()
    assert "start_at <= %s" in query
    assert "(end_at is null or end_at > %s)" in query


def test_compare_notfound(provider):
    """Test compare raises NotFound when no rows are found."""
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = []

    with pytest.raises(NotFound):
        provider.compare(["UNKNOWN"])


def test_get_history_ok(provider):
    """Test get_history returns ordered time-series points."""
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [
        {
            "timeseries_key": "ts1",
            "company_id": "COMP1",
            "document_version": 1,
            "source_modified_at_utc": datetime(2024, 1, 1),
            "event_time": datetime(2024, 1, 1),
            "source_file_path": "/data/corporates_A_1.xlsm",
            "source_modified_date_key": 20240101,
            "source_modified_date": datetime(2024, 1, 1),
            "column_name": "rating",
            "metric_name": "business_risk_score",
            "series_value": "B",
            "year_label": None,
            "is_estimate": None,
        },
        {
            "timeseries_key": "ts2",
            "company_id": "COMP1",
            "document_version": 2,
            "source_modified_at_utc": datetime(2025, 1, 1),
            "event_time": datetime(2025, 1, 1),
            "source_file_path": "/data/corporates_A_2.xlsm",
            "source_modified_date_key": 20250101,
            "source_modified_date": datetime(2025, 1, 1),
            "column_name": "credit_metric",
            "metric_name": "scope_adjusted_debt_ebitda",
            "series_value": "18.49",
            "year_label": "2025E",
            "is_estimate": True,
        },
    ]

    output = provider.get_history("COMP1", column_name="industry_risk_score")

    assert len(output) == 2
    assert output[0].document_version == 1
    assert output[1].document_version == 2
    cursor.execute.assert_called_once()
    assert cursor.execute.call_args[0][1] == ("COMP1", "industry_risk_score")
    query = cursor.execute.call_args[0][0]
    assert "FROM facts.fct_company_timeseries" in query
    assert "WHERE company_id = %s" in query
    assert "AND column_name = %s" in query


def test_get_history_notfound(provider):
    """Test get_history raises NotFound if company history does not exist."""
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = []

    with pytest.raises(NotFound):
        provider.get_history("UNKNOWN", column_name="industry_risk_score")


def test_get_history_with_filters(provider):
    """Test get_history applies optional filters in SQL."""
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [
        {
            "timeseries_key": "ts1",
            "company_id": "COMP1",
            "document_version": 1,
            "source_modified_at_utc": datetime(2024, 1, 1),
            "event_time": datetime(2024, 1, 1),
            "source_file_path": "/data/corporates_A_1.xlsm",
            "source_modified_date_key": 20240101,
            "source_modified_date": datetime(2024, 1, 1),
            "column_name": "rating",
            "metric_name": "business_risk_score",
            "series_value": "B",
            "year_label": None,
            "is_estimate": None,
        }
    ]

    output = provider.get_history(
        "COMP1",
        column_name="rating",
        metric_name="business_risk_score",
        year_label="2025E",
    )

    assert len(output) == 1
    cursor.execute.assert_called_once()
    assert cursor.execute.call_args[0][1] == (
        "COMP1",
        "rating",
        "business_risk_score",
        "2025E",
    )
    query = cursor.execute.call_args[0][0]
    assert "column_name = %s" in query
    assert "metric_name = %s" in query
    assert "year_label = %s" in query
