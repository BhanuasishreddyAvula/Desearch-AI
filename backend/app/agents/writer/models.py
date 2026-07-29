"""Domain models for Writer Agent and Report Synthesis."""

from dataclasses import dataclass, field


@dataclass
class ReportSection:
    """Represents an individual section in a research report."""

    title: str
    content: str
    level: int = 2


@dataclass
class ReportMetadata:
    """Metadata attributes and metrics for a generated research report."""

    word_count: int = 0
    sections_count: int = 0
    evidence_cited_count: int = 0
    sources_count: int = 0


@dataclass
class ReportResult:
    """Structured report output produced by the Writer Agent."""

    session_id: str
    title: str
    executive_summary: str
    full_markdown: str
    sections: list[ReportSection] = field(default_factory=list)
    sources_cited: list[str] = field(default_factory=list)
    metadata: ReportMetadata = field(default_factory=ReportMetadata)
