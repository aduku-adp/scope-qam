"""Upload service."""

from __future__ import annotations

from api.providers.upload_provider import UploadProvider
from api.upload.models import UploadDetailsModel, UploadModel, UploadStatsModel


class UploadService:
    """Upload service."""

    def __init__(self, upload_provider: UploadProvider):
        self.upload_provider = upload_provider

    def list_uploads(self) -> list[UploadModel]:
        return self.upload_provider.list()

    def get_upload_details(self, upload_id: str) -> UploadDetailsModel:
        return self.upload_provider.get_details(upload_id)

    def get_upload_file_info(self, upload_id: str) -> tuple[str, str]:
        return self.upload_provider.get_file_info(upload_id)

    def get_upload_stats(self) -> UploadStatsModel:
        return self.upload_provider.stats()

