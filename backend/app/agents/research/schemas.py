"""Pydantic v2 schemas for Research Agent API endpoints."""

from typing import Any
from pydantic import BaseModel, Field

from app.agents.planner.schemas import PlannerResultSchema
from app.schemas.base import BaseResponse


class EvidenceSchema(BaseModel):
    """Schema representing an individual research evidence item."""

    id: str = Field(..., description="Unique evidence item identifier, e.g., ev_1")
    title: str = Field(..., description="Short descriptive title of the evidence finding")
    summary: str = Field(..., description="Summary of evidence content")
    source: str = Field(..., description="Source URL or document location")
    tool_used: str = Field(..., description="ID of tool used to gather evidence")
    confidence: float = Field(
        default=0.85, ge=0.0, le=1.0, description="Evidence confidence score (0.0 - 1.0)"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Arbitrary metadata attributes"
    )


class ResearchResultSchema(BaseModel):
    """Pydantic representation of ResearchResult output for API serialization."""

    session_id: str = Field(..., description="UUID identifier of ResearchSession")
    goal: str = Field(..., description="Primary research goal statement")
    summary: str = Field(..., description="Executive summary of gathered research evidence")
    evidence_items: list[EvidenceSchema] = Field(
        default_factory=list, description="Collection of structured evidence items"
    )
    sources_consulted: list[str] = Field(
        default_factory=list, description="Unique list of verified source URLs consulted"
    )
    tools_executed: list[str] = Field(
        default_factory=list, description="List of tool IDs executed during research"
    )


class ResearchRunRequest(BaseModel):
    """Request payload for executing research against a PlannerResult plan."""

    session_id: str = Field(..., description="UUID identifier of ResearchSession")
    plan: PlannerResultSchema = Field(..., description="Structured PlannerResult execution plan")


ResearchEnvelope = BaseResponse[ResearchResultSchema]
