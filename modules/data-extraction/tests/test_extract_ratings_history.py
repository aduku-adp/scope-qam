import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

pytest.importorskip("pydantic")


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "extract_ratings_history.py"
)
MODULE_DIR = str(MODULE_PATH.parent)
if MODULE_DIR not in sys.path:
    sys.path.insert(0, MODULE_DIR)
SPEC = importlib.util.spec_from_file_location("extract_ratings_history", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

REPO_PATH = Path(__file__).resolve().parents[1] / "postgres_repository.py"
REPO_SPEC = importlib.util.spec_from_file_location("postgres_repository", REPO_PATH)
REPO_MODULE = importlib.util.module_from_spec(REPO_SPEC)
assert REPO_SPEC and REPO_SPEC.loader
sys.modules[REPO_SPEC.name] = REPO_MODULE
REPO_SPEC.loader.exec_module(REPO_MODULE)


def _sample_payload() -> dict:
    return {
        "company_information": {
            "name": "Company A",
            "country_of_origin": "Federal Republic of Germany",
            "corporate_sector": "Personal & Household Goods",
            "segmentation_criteria": "EBITDA contribution",
            "methodology": {
                "rating_methodologies_applied": ["General Corporate Rating Methodology"]
            },
            "industry_risk": [{"industry_risk_score": "BBB"}],
        },
        "business_risk_profile": {"overall_score": "B"},
        "financial_risk_profile": {"overall_score": "CC"},
        "credit_metrics": [],
    }


def _mock_conn_with_fetchone(fetchone_return):
    conn = MagicMock()
    cur = MagicMock()
    conn.__enter__.return_value = conn
    conn.__exit__.return_value = None
    cur.__enter__.return_value = cur
    cur.__exit__.return_value = None
    cur.fetchone.return_value = fetchone_return
    conn.cursor.return_value = cur
    return conn, cur


def test_ensure_table_and_insert_sets_record_hash_and_returns_id():
    payload = _sample_payload()
    cfg = MODULE.DbConfig(host="h", port=5432, user="u", password="p", dbname="d")

    conn, cur = _mock_conn_with_fetchone(("11111111-1111-1111-1111-111111111111",))

    with patch.object(REPO_MODULE.psycopg2, "connect", return_value=conn):
        inserted_id = MODULE.ensure_table_and_insert("data/corporates_A_2.xlsm", payload, cfg)

    assert inserted_id == "11111111-1111-1111-1111-111111111111"
    assert cur.execute.call_count >= 4

    insert_call = None
    for call in cur.execute.call_args_list:
        sql = call.args[0]
        if "INSERT INTO raw.rating_assessments_history" in sql:
            insert_call = call
            break
    assert insert_call is not None

    insert_sql, insert_params = insert_call.args
    assert "ON CONFLICT (record_hash) DO NOTHING" in insert_sql

    expected_hash = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    ).hexdigest()
    expected_company_key = hashlib.md5(
        "Company A|Federal Republic of Germany".encode("utf-8")
    ).hexdigest()
    assert insert_params[0] == expected_company_key
    assert insert_params[1] == expected_hash
    assert insert_params[2] == expected_company_key
    assert insert_params[3].adapted == payload["company_information"]
    assert insert_params[4].adapted == payload["company_information"]["methodology"]
    assert insert_params[5].adapted == payload["company_information"]["industry_risk"]
    assert insert_params[6].adapted == payload["business_risk_profile"]
    assert insert_params[7].adapted == payload["financial_risk_profile"]
    assert insert_params[8].adapted == payload["credit_metrics"]
    assert insert_params[9].adapted == payload
    assert insert_params[10] == "Company A"
    assert insert_params[13] == "EBITDA contribution"
    assert str(insert_params[16]).endswith("corporates_A_2.xlsm")
    assert insert_params[17] is None or "T" in str(insert_params[17])


def test_ensure_table_and_insert_returns_none_on_duplicate_conflict():
    payload = _sample_payload()
    cfg = MODULE.DbConfig(host="h", port=5432, user="u", password="p", dbname="d")

    conn, _cur = _mock_conn_with_fetchone(None)

    with patch.object(REPO_MODULE.psycopg2, "connect", return_value=conn):
        inserted_id = MODULE.ensure_table_and_insert("data/corporates_A_2.xlsm", payload, cfg)

    assert inserted_id is None
