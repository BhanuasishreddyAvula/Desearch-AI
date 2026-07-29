"""Pydantic v2 schemas for Writer Agent API endpoints."""

from pydantic import BaseModel, Field

from app.agents.planner.schemas import PlannerResultSchema
from app.agents.research.schemas import ResearchResultSchema
from app.schemas.base import BaseResponse


class ReportSectionSchema(BaseModel):
    """Schema representing an individual report section."""

    title: str = Field(..., description="Section title heading")
    content: str = Field(..., description="Section markdown body content")
    level: int = Field(
        default=2, ge=1, le=6, description="Heading level (1=H1, 2=H2)"
    )


class ReportMetadataSchema(BaseModel):
    """Schema representing report metadata metrics."""

    word_count: int = Field(
        default=0, description="Total word count of generated report"
    )
    sections_count: int = Field(
        default=0, description="Total number of sections"
    )
    evidence_cited_count: int = Field(
        default=0, description="Number of evidence items cited"
    )
    sources_count: int = Field(
        default=0, description="Number of unique sources cited"
    )


class ReportResultSchema(BaseModel):
    """Pydantic representation of ReportResult output for API serialization."""

    session_id: str = Field(..., description="UUID identifier of ResearchSession")
    title: str = Field(..., description="Main title of the research report")
    executive_summary: str = Field(
        ..., description="High-level executive summary"
    )
    full_markdown: str = Field(
        ..., description="Complete compiled Markdown document string"
    )
    sections: list[ReportSectionSchema] = Field(
        default_factory=list, description="Structured list of report sections"
    )
    sources_cited: list[str] = Field(
        default_factory=list, description="List of source URLs cited in report"
    )
    metadata: ReportMetadataSchema = Field(
        default_factory=ReportMetadataSchema,
        description="Report metrics and metadata",
    )


class WriterRunRequest(BaseModel):
    """Request payload for executing Writer Agent report generation."""

    session_id: str = Field(..., description="UUID identifier of ResearchSession")
    plan: PlannerResultSchema = Field(
        ..., description="Structured PlannerResult plan"
    )
    research: ResearchResultSchema = Field(
        ..., description="Structured ResearchResult evidence collection"
    )


ReportEnvelope = BaseResponse[ReportResultSchema]
