"""Domain models for Content Tool and Firecrawl Provider."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExtractedDocument:
    """Normalized web document extracted by Content Tool."""

    url: str
    title: str
    markdown: str
    plain_text: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert ExtractedDocument to dictionary matching tool output schema."""
        return {
            "url": self.url,
            "title": self.title,
            "markdown": self.markdown,
            "plain_text": self.plain_text,
            "metadata": self.metadata,
            "content": self.markdown or self.plain_text,
            "status_code": 200,
        }
