"""E2E tests for qam-api company endpoints."""

import requests

from helpers.connectors import Connectors
from helpers.constants import SERVICE_URL

BASE_URL = f"{SERVICE_URL}/v1/companies"


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
