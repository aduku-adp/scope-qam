"""E2E tests for qam-api company endpoints."""

import requests

from helpers.connectors import Connectors
from helpers.constants import SERVICE_URL

BASE_URL = f"{SERVICE_URL}/v1/companies"
SNAPSHOT_BASE_URL = f"{SERVICE_URL}/v1/snapshots"


def _service_or_skip(connectors: Connectors):
    try:
        response = connectors.requester.get(BASE_URL, timeout=10)
        return response
    except requests.RequestException as exc:
        raise AssertionError(f"Service not reachable at {SERVICE_URL}: {exc}") from exc


def _json_payload_or_fail(response: requests.Response) -> dict:
    content_type = response.headers.get("content-type", "")
    if "application/json" not in content_type.lower():
        preview = response.text[:200].replace("\n", " ")
        raise AssertionError(
            f"Expected JSON from {response.url}, got content-type '{content_type}'. "
            f"Response starts with: {preview!r}. "
            "Check SERVICE_URL points to qam-api."
        )
    try:
        return response.json()
    except requests.JSONDecodeError as exc:
        preview = response.text[:200].replace("\n", " ")
        raise AssertionError(
            f"Invalid JSON response from {response.url}. "
            f"Response starts with: {preview!r}"
        ) from exc


def test_e2e_get_companies_ok(connectors: Connectors):
    """GET /v1/companies returns a valid response envelope."""
    response = _service_or_skip(connectors)
    assert response.status_code == 200
    payload = _json_payload_or_fail(response)
    assert payload["status"] == "OK"
    assert "request_uid" in payload
    assert isinstance(payload["data"], list)


def test_e2e_get_company_ok(connectors: Connectors):
    """GET /v1/companies/{company_id} returns one company when data exists."""
    list_response = _service_or_skip(connectors)
    companies = _json_payload_or_fail(list_response)["data"]
    if not companies:
        raise AssertionError("No companies loaded in DB; cannot validate company detail endpoint")

    company_id = companies[0]["company_id"]
    response = connectors.requester.get(f"{BASE_URL}/{company_id}", timeout=10)
    assert response.status_code == 200
    payload = _json_payload_or_fail(response)
    assert payload["status"] == "OK"
    assert payload["data"]["company_id"] == company_id


def test_e2e_get_company_versions_ok(connectors: Connectors):
    """GET /v1/companies/{company_id}/versions returns versions list."""
    list_response = _service_or_skip(connectors)
    companies = _json_payload_or_fail(list_response)["data"]
    if not companies:
        raise AssertionError("No companies loaded in DB; cannot validate versions endpoint")

    company_id = companies[0]["company_id"]
    response = connectors.requester.get(f"{BASE_URL}/{company_id}/versions", timeout=10)
    assert response.status_code == 200
    payload = _json_payload_or_fail(response)
    assert payload["status"] == "OK"
    assert isinstance(payload["data"], list)
    assert len(payload["data"]) >= 1
    assert all(item["company_id"] == company_id for item in payload["data"])


def test_e2e_get_company_history_ok(connectors: Connectors):
    """GET /v1/companies/{company_id}/history returns time-series points."""
    list_response = _service_or_skip(connectors)
    companies = _json_payload_or_fail(list_response)["data"]
    if not companies:
        raise AssertionError("No companies loaded in DB; cannot validate history endpoint")

    company_id = companies[0]["company_id"]
    response = connectors.requester.get(f"{BASE_URL}/{company_id}/history", timeout=10)
    assert response.status_code == 200
    payload = _json_payload_or_fail(response)
    assert payload["status"] == "OK"
    assert isinstance(payload["data"], list)
    assert len(payload["data"]) >= 1
    assert all(item["company_id"] == company_id for item in payload["data"])


def test_e2e_compare_companies_ok(connectors: Connectors):
    """GET /v1/companies/compare returns point-in-time company comparison."""
    list_response = _service_or_skip(connectors)
    companies = _json_payload_or_fail(list_response)["data"]
    if len(companies) < 2:
        raise AssertionError("Need at least two companies in DB to validate compare endpoint")

    id_1 = companies[0]["company_id"]
    id_2 = companies[1]["company_id"]
    response = connectors.requester.get(
        f"{BASE_URL}/compare?company_ids={id_1},{id_2}",
        timeout=10,
    )
    assert response.status_code == 200
    payload = _json_payload_or_fail(response)
    assert payload["status"] == "OK"
    assert isinstance(payload["data"], dict)
    assert isinstance(payload["data"].get("companies"), list)
    assert isinstance(payload["data"].get("diffs"), list)
    returned_ids = {item["company_id"] for item in payload["data"]["companies"]}
    assert id_1 in returned_ids
    assert id_2 in returned_ids


def test_e2e_list_snapshots_ok(connectors: Connectors):
    """GET /v1/snapshots returns snapshot list."""
    response = connectors.requester.get(SNAPSHOT_BASE_URL, timeout=10)
    assert response.status_code == 200
    payload = _json_payload_or_fail(response)
    assert payload["status"] == "OK"
    assert isinstance(payload["data"], list)


def test_e2e_latest_snapshots_ok(connectors: Connectors):
    """GET /v1/snapshots/latest returns latest snapshots."""
    response = connectors.requester.get(f"{SNAPSHOT_BASE_URL}/latest", timeout=10)
    assert response.status_code == 200
    payload = _json_payload_or_fail(response)
    assert payload["status"] == "OK"
    assert isinstance(payload["data"], list)


def test_e2e_get_snapshot_ok(connectors: Connectors):
    """GET /v1/snapshots/{snapshot_id} returns snapshot details."""
    list_resp = connectors.requester.get(SNAPSHOT_BASE_URL, timeout=10)
    assert list_resp.status_code == 200
    snapshots = _json_payload_or_fail(list_resp)["data"]
    if not snapshots:
        raise AssertionError("No snapshots available to validate /snapshots/{snapshot_id}")
    snapshot_id = snapshots[0]["snapshot_id"]

    response = connectors.requester.get(f"{SNAPSHOT_BASE_URL}/{snapshot_id}", timeout=10)
    assert response.status_code == 200
    payload = _json_payload_or_fail(response)
    assert payload["status"] == "OK"
    assert payload["data"]["snapshot_id"] == snapshot_id
