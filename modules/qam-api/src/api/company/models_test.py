"""Company models UT."""

# pylint: disable=invalid-name

import pytest
from datetime import datetime, timezone

from .models import CompanyModel


@pytest.mark.parametrize(
    "payload",
    [
        {},  # Missing required fields
        {"company_scd_key": "COMP1_v1"},  # Missing company_id
        {"company_id": "COMP1"},  # Missing company_scd_key
    ],
)
def test_required_fields_invalid(payload):
    """Test required fields validation."""
    with pytest.raises(ValueError):
        CompanyModel(**payload)


def test_invalid_scd_dates():
    """Test end_at must be greater than start_at."""
    with pytest.raises(ValueError):
        CompanyModel(
            company_scd_key="COMP1_v1",
            company_id="COMP1",
            start_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
            end_at=datetime(2023, 1, 1, tzinfo=timezone.utc),
        )


def test_active_with_end_date_invalid():
    """Active records cannot have end_at."""
    with pytest.raises(ValueError):
        CompanyModel(
            company_scd_key="COMP1_v1",
            company_id="COMP1",
            start_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
            end_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
            is_active=True,
        )


def test_invalid_document_version():
    """document_version must be >= 1."""
    with pytest.raises(ValueError):
        CompanyModel(
            company_scd_key="COMP1_v1",
            company_id="COMP1",
            document_version=0,
        )


def test_valid_company_model():
    """Test valid CompanyModel creation."""
    model = CompanyModel(
        company_scd_key="COMP1_v1",
        company_id="COMP1",
        company_name="ACME Corp",
        country="DE",
        industry_weight="0.25 | 0.75",
        document_version=1,
        start_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        is_active=True,
    )

    assert model.company_id == "COMP1"
    assert model.is_active is True
    assert model.industry_weight == "0.25 | 0.75"
