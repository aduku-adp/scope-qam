import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "extract_ratings_history.py"
)
SPEC = importlib.util.spec_from_file_location("extract_ratings_history", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def _sample_payload() -> dict:
    return {
        "entity_information": {
            "name": "Company A",
            "country_of_origin": "Federal Republic of Germany",
            "industry": "Personal & Household Goods",
        },
        "methodology": {"rating_methodologies_applied": ["General Corporate Rating Methodology"]},
        "industry_risk": {"industry_risk_score": "BBB"},
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

    with patch.object(MODULE.psycopg2, "connect", return_value=conn):
        inserted_id = MODULE.ensure_table_and_insert("data/corporates_A_2.xlsm", payload, cfg)

    assert inserted_id == "11111111-1111-1111-1111-111111111111"
    assert cur.execute.call_count == 4

    insert_sql, insert_params = cur.execute.call_args_list[3].args
    assert "ON CONFLICT (record_hash) DO NOTHING" in insert_sql

    expected_hash = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    ).hexdigest()
    assert insert_params[0] == expected_hash


def test_ensure_table_and_insert_returns_none_on_duplicate_conflict():
    payload = _sample_payload()
    cfg = MODULE.DbConfig(host="h", port=5432, user="u", password="p", dbname="d")

    conn, _cur = _mock_conn_with_fetchone(None)

    with patch.object(MODULE.psycopg2, "connect", return_value=conn):
        inserted_id = MODULE.ensure_table_and_insert("data/corporates_A_2.xlsm", payload, cfg)

    assert inserted_id is None
