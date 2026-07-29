"""Domain models for Multi-Agent Orchestrator."""

from dataclasses import dataclass, field
from typing import Any

from app.agents.planner.models import PlannerResult
from app.agents.research.models import ResearchResult
from app.agents.reviewer.models import ReviewResult
from app.agents.writer.models import ReportResult
from app.orchestrator.workflow import WorkflowStatus, WorkflowStep


@dataclass
class AgentExecution:
    """Tracks execution metrics for an individual agent run in the workflow."""

    agent_name: str
    step: WorkflowStep
    status: WorkflowStatus
    execution_time_ms: float
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowRequest:
    """Input parameters for initiating an orchestrated multi-agent workflow."""

    session_id: str
    query: str


@dataclass
class WorkflowResult:
    """Aggregated result output produced by the Multi-Agent Orchestrator."""

    session_id: str
    status: WorkflowStatus
    planner_result: PlannerResult
    research_result: ResearchResult
    report_result: ReportResult
    review_result: ReviewResult
    executions: list[AgentExecution] = field(default_factory=list)
    total_execution_time_ms: float = 0.0
