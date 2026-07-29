"""Export domain data models."""

from dataclasses import dataclass


@dataclass
class ExportResult:
    """Normalized payload container for formatted export bytes and media headers."""

    content: bytes
    media_type: str
    filename: str
