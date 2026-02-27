import importlib.util
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "business_rules.py"
SPEC = importlib.util.spec_from_file_location("business_rules", MODULE_PATH)
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
            "methodology": {"rating_methodologies_applied": ["General Corporate Rating Methodology"]},
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


def test_business_rules_payload_passes_with_valid_payload():
    engine = MODULE.BusinessRuleEngine(
        Path(__file__).resolve().parents[1] / "business_rules.yml"
    )
    outcomes = engine.evaluate_payload(_valid_payload())
    assert all(outcome.status in {"pass", "warn"} for outcome in outcomes)


def test_business_rules_score_scale_fails_on_invalid_score():
    engine = MODULE.BusinessRuleEngine(
        Path(__file__).resolve().parents[1] / "business_rules.yml"
    )
    payload = _valid_payload()
    payload["business_risk_profile"]["overall_score"] = "INVALID"
    outcomes = engine.evaluate_payload(payload)
    by_rule = {outcome.rule_id: outcome for outcome in outcomes}
    assert by_rule["score_scale_allowed"].status == "fail"


def test_business_rules_allow_null_credit_metric_values():
    engine = MODULE.BusinessRuleEngine(
        Path(__file__).resolve().parents[1] / "business_rules.yml"
    )
    payload = _valid_payload()
    payload["credit_metrics"][0]["values"][0]["value"] = None
    outcomes = engine.evaluate_payload(payload)
    by_rule = {outcome.rule_id: outcome for outcome in outcomes}
    assert by_rule["credit_metrics_year_value_logic"].status == "pass"
