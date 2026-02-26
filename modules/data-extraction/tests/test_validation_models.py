import importlib.util
import sys
from pathlib import Path

import pytest

pytest.importorskip("pydantic")

from pydantic import ValidationError


MODULE_PATH = Path(__file__).resolve().parents[1] / "validation_models.py"
SPEC = importlib.util.spec_from_file_location("validation_models", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def _valid_payload() -> dict:
    return {
        "company_information": {
            "name": "Company A",
            "corporate_sector": "CorporateSector",
            "country_of_origin": "Federal Republic of Germany",
            "reporting_currency": "EUR",
            "accounting_principles": "IFRS",
            "fiscal_year_end": "December",
            "segmentation_criteria": "EBITDA contribution",
            "methodology": {
                "rating_methodologies_applied": ["General Corporate Rating Methodology"]
            },
            "industry_risk": [
                {
                    "industry_classification": "Consumer Products: Non-Discretionary",
                    "industry_risk_score": "BBB",
                    "industry_weight": 1.0,
                }
            ],
        },
        "business_risk_profile": {
            "overall_score": "B",
            "components": {
                "blended_industry_risk_profile": "A",
                "competitive_positioning": "B+",
                "market_share": "B+",
                "diversification": "B+",
                "operating_profitability": "B",
                "sector_company_specific_factors_1": "B-",
                "sector_company_specific_factors_2": None,
            },
        },
        "financial_risk_profile": {
            "overall_score": "CC",
            "components": {
                "leverage": "CCC",
                "interest_cover": "B-",
                "cash_flow_cover": "CCC",
                "liquidity_adjustment_notches": -2,
            },
        },
        "credit_metrics": [
            {
                "metric": "scope_adjusted_ebitda_interest_cover",
                "values": [{"year": "2024", "value": 36.8}],
                "locked": True,
            }
        ],
    }


def test_validate_extracted_payload_success():
    payload = _valid_payload()
    validated = MODULE.validate_extracted_payload(payload)

    assert validated["company_information"]["name"] == "Company A"
    assert validated["credit_metrics"][0]["values"][0]["value"] == 36.8


def test_validate_extracted_payload_missing_required_field_fails():
    payload = _valid_payload()
    del payload["company_information"]["name"]

    with pytest.raises(ValidationError):
        MODULE.validate_extracted_payload(payload)


def test_validate_extracted_payload_invalid_credit_metric_value_type_fails():
    payload = _valid_payload()
    payload["credit_metrics"][0]["values"][0]["value"] = "not-a-float"

    with pytest.raises(ValidationError):
        MODULE.validate_extracted_payload(payload)


def test_validate_extracted_payload_invalid_text_type_fails():
    payload = _valid_payload()
    payload["company_information"]["name"] = 123

    with pytest.raises(ValidationError):
        MODULE.validate_extracted_payload(payload)


def test_validate_extracted_payload_invalid_numeric_type_fails():
    payload = _valid_payload()
    payload["company_information"]["industry_risk"][0]["industry_weight"] = "bad-float"

    with pytest.raises(ValidationError):
        MODULE.validate_extracted_payload(payload)
