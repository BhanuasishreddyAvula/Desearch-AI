"""Export format enumeration definitions."""

from enum import Enum


class ExportFormat(str, Enum):
    """Supported export formats for research reports."""

    MARKDOWN = "markdown"
    MD = "md"
    PDF = "pdf"

    @classmethod
    def from_str(cls, val: str) -> "ExportFormat":
        """Parse format string into ExportFormat enum."""
        cleaned = val.strip().lower()
        if cleaned in ("markdown", "md"):
            return cls.MARKDOWN
        elif cleaned == "pdf":
            return cls.PDF
        raise ValueError(f"Unsupported format '{val}'")
