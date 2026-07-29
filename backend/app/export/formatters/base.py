"""Abstract base export formatter interface."""

from abc import ABC, abstractmethod
import re
from typing import Any

from app.export.models import ExportResult


class BaseExportFormatter(ABC):
    """Abstract interface defining report export formatting contracts."""

    @abstractmethod
    def format_report(
        self, report_data: dict[str, Any], session_id: str
    ) -> ExportResult:
        """Format report data dictionary into an ExportResult."""
        pass

    @staticmethod
    def sanitize_filename(name: str, fallback_id: str, extension: str) -> str:
        """Sanitize report title into safe filename preventing path traversal or OS errors."""
        cleaned = re.sub(r"[^\w\s-]", "", name).strip().replace(" ", "_")
        cleaned = re.sub(r"_+", "_", cleaned).lower()
        if not cleaned:
            cleaned = f"desearch_report_{fallback_id[:8]}"
        else:
            cleaned = f"desearch_{cleaned[:40]}"
        return f"{cleaned}.{extension.lstrip('.')}"
