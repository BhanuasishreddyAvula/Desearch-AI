"""Pydantic v2 schemas for Reviewer Agent API endpoints."""

from pydantic import BaseModel, Field

from app.agents.planner.schemas import PlannerResultSchema
from app.agents.research.schemas import ResearchResultSchema
from app.agents.writer.schemas import ReportResultSchema
from app.schemas.base import BaseResponse


class ReviewResultSchema(BaseModel):
    """Pydantic representation of ReviewResult output for API serialization."""

    session_id: str = Field(..., description="UUID identifier of ResearchSession")
    approved: bool = Field(
        ..., description="Flag indicating if the report is approved for release"
    )
    overall_score: float = Field(
        ..., ge=0.0, le=1.0, description="Overall quality score (0.0 - 1.0)"
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Evaluation confidence score (0.0 - 1.0)"
    )
    summary: str = Field(
        ..., description="Executive summary of the quality evaluation"
    )
    strengths: list[str] = Field(
        default_factory=list, description="Key strengths of the report"
    )
    issues: list[str] = Field(
        default_factory=list,
        description="Identified quality issues or formatting errors",
    )
    missing_evidence: list[str] = Field(
        default_factory=list,
        description="Planned requirements lacking evidence support",
    )
    unsupported_claims: list[str] = Field(
        default_factory=list,
        description="Claims made in report not supported by research evidence",
    )
    recommendations: list[str] = Field(
        default_factory=list,
        description="Actionable recommendations for report improvement",
    )


class ReviewRunRequest(BaseModel):
    """Request payload for executing Reviewer Agent quality evaluation."""

    session_id: str = Field(..., description="UUID identifier of ResearchSession")
    plan: PlannerResultSchema = Field(
        ..., description="Structured PlannerResult plan"
    )
    research: ResearchResultSchema = Field(
        ..., description="Structured ResearchResult evidence collection"
    )
    report: ReportResultSchema = Field(
        ..., description="Structured ReportResult generated report"
    )


ReviewEnvelope = BaseResponse[ReviewResultSchema]
