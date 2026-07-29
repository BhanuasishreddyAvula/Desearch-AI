"""Pydantic v2 serialization schemas for Search Tool and Exa API contracts."""

from typing import Any
from pydantic import BaseModel, Field


class ExaSearchRequestSchema(BaseModel):
    """Payload schema sent to Exa API /search endpoint."""

    query: str = Field(..., description="Search query string")
    numResults: int = Field(default=5, ge=1, le=20, description="Number of results requested")
    useAutoprompt: bool = Field(default=True, description="Enable Exa autoprompting")


class SearchResultItemSchema(BaseModel):
    """Pydantic schema representing a normalized search result item."""

    title: str = Field(..., description="Web page title")
    url: str = Field(..., description="Web page URL")
    snippet: str = Field(..., description="Extracted content snippet or summary")
    published_at: str | None = Field(default=None, description="Publication date string")
    score: float | None = Field(default=None, description="Exa relevance score")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class SearchResultSchema(BaseModel):
    """Pydantic schema representing SearchResult tool output."""

    query: str = Field(..., description="Executed search query")
    results: list[SearchResultItemSchema] = Field(default_factory=list, description="List of search result items")
    total_results: int = Field(default=0, description="Total number of results returned")
    latency_ms: float = Field(default=0.0, description="Provider execution latency in milliseconds")
