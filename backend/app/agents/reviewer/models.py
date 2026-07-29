"""Domain models for Reviewer Agent and Quality Evaluation."""

from dataclasses import dataclass, field


@dataclass
class ReviewResult:
    """Structured quality evaluation output produced by the Reviewer Agent."""

    session_id: str
    approved: bool
    overall_score: float
    confidence: float
    summary: str
    strengths: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)
    missing_evidence: list[str] = field(default_factory=list)
    unsupported_claims: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
