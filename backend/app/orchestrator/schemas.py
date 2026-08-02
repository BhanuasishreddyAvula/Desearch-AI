"""Pydantic v2 schemas for Multi-Agent Orchestrator endpoints."""

from typing import Any
from pydantic import BaseModel, Field

from app.agents.planner.schemas import PlannerResultSchema
from app.agents.research.schemas import ResearchResultSchema
from app.agents.reviewer.schemas import ReviewResultSchema
from app.agents.writer.schemas import ReportResultSchema
from app.schemas.base import BaseResponse


class WorkflowRunRequest(BaseModel):
    """Request payload for running an orchestrated multi-agent workflow."""

    session_id: str = Field(..., description="UUID identifier of ResearchSession")
    query: str = Field(..., description="Primary research objective query")


class WorkflowCancelRequest(BaseModel):
    """Request payload for cancelling a running workflow."""

    session_id: str = Field(..., description="UUID identifier of the session to cancel")




class AgentExecutionSchema(BaseModel):
    """Schema representing an individual agent execution run in the workflow."""

    agent_name: str = Field(..., description="Name identifier of executed agent")
    step: str = Field(
        ...,
        description="Workflow step string (planning, researching, writing, reviewing)",
    )
    status: str = Field(
        ..., description="Execution status (pending, running, completed, failed)"
    )
    execution_time_ms: float = Field(
        ..., description="Execution latency in milliseconds"
    )
    details: dict[str, Any] = Field(
        default_factory=dict, description="Execution metadata details"
    )


class WorkflowResultSchema(BaseModel):
    """Aggregated workflow response model wrapping Planner, Research, Report, and Review results."""

    session_id: str = Field(..., description="UUID identifier of ResearchSession")
    status: str = Field(..., description="Overall workflow status")
    planner_result: PlannerResultSchema = Field(
        ..., description="Structured plan produced by Planner Agent"
    )
    research_result: ResearchResultSchema = Field(
        ..., description="Structured evidence gathered by Research Agent"
    )
    report_result: ReportResultSchema = Field(
        ..., description="Final Markdown research report synthesized by Writer Agent"
    )
    review_result: ReviewResultSchema = Field(
        ..., description="Quality evaluation report produced by Reviewer Agent"
    )
    executions: list[AgentExecutionSchema] = Field(
        default_factory=list, description="Ordered execution metrics for each agent"
    )
    total_execution_time_ms: float = Field(
        ..., description="Total workflow execution latency in milliseconds"
    )


WorkflowEnvelope = BaseResponse[WorkflowResultSchema]
