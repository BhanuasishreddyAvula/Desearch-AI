"""Pydantic v2 serialization schemas for Content Tool and Firecrawl API contracts."""

from typing import Any
from pydantic import BaseModel, Field


class FirecrawlScrapeRequestSchema(BaseModel):
    """Payload schema sent to Firecrawl API /v1/scrape endpoint."""

    url: str = Field(..., description="Target web page URL to extract")
    formats: list[str] = Field(default_factory=lambda: ["markdown"], description="Extraction format list")


class ExtractedDocumentSchema(BaseModel):
    """Pydantic schema representing ExtractedDocument tool output."""

    url: str = Field(..., description="Target page URL")
    title: str = Field(..., description="Page title")
    markdown: str = Field(..., description="Extracted Markdown document content")
    plain_text: str = Field(..., description="Extracted plain text content")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Extraction metadata")
