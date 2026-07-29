"""Domain models for Search Tool and Exa Provider."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SearchResultItem:
    """Individual normalized search result item."""

    title: str
    url: str
    snippet: str
    published_at: str | None = None
    score: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert result item to dictionary."""
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "published_at": self.published_at,
            "score": self.score,
            "metadata": self.metadata,
        }


@dataclass
class SearchResult:
    """Normalized search result collection returned by Search Tool."""

    query: str
    results: list[SearchResultItem] = field(default_factory=list)
    total_results: int = 0
    latency_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert SearchResult to dictionary output matching Tool schema."""
        return {
            "query": self.query,
            "results": [item.to_dict() for item in self.results],
            "total_results": self.total_results,
            "latency_ms": self.latency_ms,
        }
