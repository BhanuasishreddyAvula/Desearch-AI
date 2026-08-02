"""Citation Intelligence Engine schemas separating Source, Evidence, and Citation data models."""

from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

ConfidenceLevel = Literal["High", "Medium", "Low"]
SourceCategory = Literal[
    "Official Documentation",
    "Research Paper",
    "Government",
    "GitHub",
    "Engineering Blog",
    "Community Forum",
    "General Web",
]


class SourceSchema(BaseModel):
    """Authoritative source domain entity."""

    id: str = Field(..., description="Unique source UUID")
    title: str = Field(..., description="Page or document title")
    url: str = Field(..., description="Canonical source URL")
    domain: str = Field(..., description="Clean domain name e.g. milesweb.com")
    favicon: str | None = Field(default=None, description="Favicon icon URL")
    category: SourceCategory = Field(
        default="General Web", description="Source classification category"
    )
    retrieved_at: datetime = Field(
        default_factory=datetime.utcnow, description="Retrieval timestamp"
    )
    quality_score: int = Field(
        default=85, ge=0, le=100, description="Internal ranking score (0-100)"
    )
    trust_score: ConfidenceLevel = Field(
        default="High", description="Source trust rating"
    )


class EvidenceSchema(BaseModel):
    """Evidence snippet retrieved from a source."""

    id: str = Field(..., description="Unique evidence UUID")
    source_id: str = Field(..., description="ID of supporting Source")
    snippet: str = Field(..., description="Extracted text content snippet")
    start_offset: int | None = Field(default=None, description="Character start offset")
    end_offset: int | None = Field(default=None, description="Character end offset")
    retrieval_phase: str | None = Field(
        default="reading", description="Orchestration phase where evidence was discovered"
    )
    confidence: ConfidenceLevel = Field(
        default="High", description="Evidence extraction confidence level"
    )


class CitationSchema(BaseModel):
    """Inline citation mapping connecting report claims to supporting evidence."""

    id: str = Field(..., description="Unique citation UUID")
    report_section_id: str | None = Field(
        default=None, description="ID of section containing claim"
    )
    evidence_ids: list[str] = Field(
        default_factory=list, description="IDs of supporting Evidence snippets"
    )
    citation_number: int = Field(..., ge=1, description="Numeric inline citation badge number")
    claim_text: str | None = Field(
        default=None, description="Exact factual statement supported"
    )
    confidence: ConfidenceLevel = Field(
        default="High", description="Fact-check verification rating"
    )
