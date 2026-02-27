"""Upload API controller."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path as ApiPath
from fastapi.responses import FileResponse

from api.upload.models import UploadDetailsModel, UploadModel, UploadStatsModel
from api.upload.service import UploadService
from helpers.formatter import ErrorModel, OutputModel, format_response

UPLOAD_TAG = "Upload Audit Endpoints"


def _resolve_upload_file_path(source_file_path: str, source_filename: str) -> Path | None:
    """Resolve a readable upload file path across container path layouts."""
    direct = Path(source_file_path)
    if direct.exists() and direct.is_file():
        return direct

    # Try replacing the extractor container root with an optional local mount root.
    repo_mount_root = os.environ.get("UPLOAD_REPO_MOUNT_ROOT")
    if repo_mount_root and source_file_path.startswith("/opt/airflow/repo/"):
        translated = Path(repo_mount_root) / source_file_path.removeprefix("/opt/airflow/repo/")
        if translated.exists() and translated.is_file():
            return translated

    search_dirs = os.environ.get("UPLOAD_FILE_SEARCH_DIRS", "/data/corporates,./data/corporates")
    for raw_dir in search_dirs.split(","):
        directory = raw_dir.strip()
        if not directory:
            continue
        candidate = Path(directory) / source_filename
        if candidate.exists() and candidate.is_file():
            return candidate

    return None


def build(router: APIRouter, service: UploadService) -> None:
    """Build upload audit routes."""

    @router.get(
        "/uploads",
        tags=[UPLOAD_TAG],
        responses={500: {"description": "Server error", "model": ErrorModel}},
        response_model_exclude_none=True,
    )
    async def list_uploads() -> OutputModel[list[UploadModel]]:
        uploads = service.list_uploads()
        return format_response(uploads)

    @router.get(
        "/uploads/stats",
        tags=[UPLOAD_TAG],
        responses={500: {"description": "Server error", "model": ErrorModel}},
        response_model_exclude_none=True,
    )
    async def get_upload_stats() -> OutputModel[UploadStatsModel]:
        stats = service.get_upload_stats()
        return format_response(stats)

    @router.get(
        "/uploads/{upload_id}/details",
        tags=[UPLOAD_TAG],
        responses={
            404: {"description": "Not Found", "model": ErrorModel},
            500: {"description": "Server error", "model": ErrorModel},
        },
        response_model_exclude_none=True,
    )
    async def get_upload_details(
        upload_id: Annotated[str, ApiPath(description="Upload id")],
    ) -> OutputModel[UploadDetailsModel]:
        try:
            details = service.get_upload_details(upload_id)
        except Exception as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        return format_response(details)

    @router.get(
        "/uploads/{upload_id}/file",
        tags=[UPLOAD_TAG],
        responses={
            404: {"description": "Not Found", "model": ErrorModel},
            500: {"description": "Server error", "model": ErrorModel},
        },
    )
    async def download_upload_file(
        upload_id: Annotated[str, ApiPath(description="Upload id")],
    ) -> FileResponse:
        try:
            source_file_path, source_filename = service.get_upload_file_info(upload_id)
        except Exception as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        path = _resolve_upload_file_path(source_file_path, source_filename)
        if path is None:
            raise HTTPException(status_code=404, detail=f"File not found at {source_file_path}")

        return FileResponse(path=str(path), filename=source_filename)
