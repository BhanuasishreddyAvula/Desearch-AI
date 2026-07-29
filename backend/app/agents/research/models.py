"""Domain models for Research Agent and Evidence Collection."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ResearchTask:
    """Represents a single research execution task derived from PlannerResult."""

    id: str
    title: str
    description: str
    priority: str = "medium"


@dataclass
class Evidence:
    """Represents an individual item of gathered research evidence."""

    id: str
    title: str
    summary: str
    source: str
    tool_used: str
    confidence: float = 0.85
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert evidence model to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "source": self.source,
            "tool_used": self.tool_used,
            "confidence": self.confidence,
            "metadata": self.metadata,
        }


@dataclass
class EvidenceCollection:
    """Container collection wrapping gathered evidence items."""

    items: list[Evidence] = field(default_factory=list)

    def add(self, evidence: Evidence) -> None:
        """Add an evidence item to the collection."""
        self.items.append(evidence)

    def list_all(self) -> list[Evidence]:
        """Return all evidence items."""
        return self.items


@dataclass
class ResearchResult:
    """Structured output produced by the Research Agent."""

    session_id: str
    goal: str
    summary: str
    evidence_items: list[Evidence] = field(default_factory=list)
    sources_consulted: list[str] = field(default_factory=list)
    tools_executed: list[str] = field(default_factory=list)
