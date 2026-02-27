"""Common configuration for API tests."""

from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi import APIRouter, FastAPI

from helpers.constants import API_DESCRIPTION, API_TITLE, API_VERSION


@pytest.fixture(name="app")
def app_fixture() -> Generator[FastAPI, None, None]:
    """Set up testing FastAPI app with add_controller helper."""
    fastapi_app = FastAPI(
        title=API_TITLE,
        description=API_DESCRIPTION,
        version=API_VERSION,
    )

    def add_controller(prefix: str, build_fn, **kwargs) -> None:
        router = APIRouter()
        build_fn(router=router, **kwargs)
        fastapi_app.include_router(router, prefix=prefix)

    fastapi_app.add_controller = add_controller  # type: ignore[attr-defined]

    yield fastapi_app
