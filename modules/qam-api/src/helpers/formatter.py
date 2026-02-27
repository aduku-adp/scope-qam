"""Formatter helper."""

from __future__ import annotations

from enum import Enum
from typing import Generic, Optional, TypeVar
from uuid import uuid4

from pydantic import BaseModel

T = TypeVar("T")


class Status(str, Enum):
    """Response status enum."""

    OK = "OK"


class OutputModel(BaseModel, Generic[T]):
    """Standard API output envelope."""

    data: Optional[T] = None
    request_uid: str
    status: Status = Status.OK


class EmptyOutputModel(BaseModel):
    """Standard empty API output envelope."""

    request_uid: str
    status: Status = Status.OK


class ErrorModel(BaseModel):
    """Basic error model."""

    detail: str


def _request_uid() -> str:
    return str(uuid4())


def format_response(data: T | list[T] | None = None) -> OutputModel[T]:
    """Format response for the API."""
    return OutputModel(
        data=data,
        request_uid=_request_uid(),
        status=Status.OK,
    )


def empty_response() -> EmptyOutputModel:
    """Empty response for the API."""
    return EmptyOutputModel(
        status=Status.OK,
        request_uid=_request_uid(),
    )
