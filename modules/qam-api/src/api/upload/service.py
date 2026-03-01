"""Upload service."""

from __future__ import annotations

from api.providers.upload_provider import UploadProvider
from api.upload.models import UploadDetailsModel, UploadModel, UploadStatsModel


class UploadService:
    """Application service for upload-audit read operations."""

    def __init__(self, upload_provider: UploadProvider):
        """Instantiate upload service with its persistence provider."""
        self.upload_provider = upload_provider

    def list_uploads(self) -> list[UploadModel]:
        """List upload metadata events."""
        return self.upload_provider.list()

    def get_upload_details(self, upload_id: str) -> UploadDetailsModel:
        """Get detailed upload event information for one upload id."""
        return self.upload_provider.get_details(upload_id)

    def get_upload_file_info(self, upload_id: str) -> tuple[str, str]:
        """Get source file path and filename for file download endpoint."""
        return self.upload_provider.get_file_info(upload_id)

    def get_upload_stats(self) -> UploadStatsModel:
        """Get aggregate upload statistics used by `/uploads/stats`."""
        return self.upload_provider.stats()
