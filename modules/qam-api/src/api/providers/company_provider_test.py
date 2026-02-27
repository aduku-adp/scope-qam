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
    "company_scd_key": "COMP2_v1",
    "company_id": "COMP2",
    "company_name": "Globex",
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
    assert "FROM dims.dim_company" in query
    assert "WHERE company_id = %s" in query


def test_get_notfound(provider):
    """Test get raises NotFound if company does not exist."""
    cursor = provider.conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = None

    with pytest.raises(NotFound):
        provider.get("UNKNOWN")
