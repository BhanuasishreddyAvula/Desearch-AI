"""API router for Research Agent endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.agents.planner.models import PlannerResult, TaskModel
from app.agents.research.research import ResearchAgent
from app.agents.research.schemas import (
    EvidenceSchema,
    ResearchEnvelope,
    ResearchResultSchema,
    ResearchRunRequest,
)
from app.agents.research.service import ResearchService
from app.core.config import settings
from app.core.llm.client import LLMClient
from app.core.repositories.session import AbstractSessionRepository
from app.dependencies import (
    get_execution_time_dep,
    get_llm_client_dep,
    get_request_id_dep,
    get_session_repository_dep,
    get_tool_registry_dep,
)
from app.schemas.metadata import ResponseMetadata
from app.tools.registry import ToolRegistry

router = APIRouter(tags=["Research", "Agents"])


def get_research_agent(
    llm_client: Annotated[LLMClient, Depends(get_llm_client_dep)],
    tool_registry: Annotated[ToolRegistry, Depends(get_tool_registry_dep)],
) -> ResearchAgent:
    """Dependency provider returning ResearchAgent instance."""
    return ResearchAgent(llm_client=llm_client, tool_registry=tool_registry)


def get_research_service(
    session_repo: Annotated[
        AbstractSessionRepository, Depends(get_session_repository_dep)
    ],
    research_agent: Annotated[ResearchAgent, Depends(get_research_agent)],
) -> ResearchService:
    """Dependency provider injecting ResearchService."""
    return ResearchService(
        session_repository=session_repo, research_agent=research_agent
    )


@router.post(
    "/run",
    response_model=ResearchEnvelope,
    summary="Execute Research Workflow",
    description="Receive a PlannerResult execution plan and gather structured research evidence via ToolRegistry tools.",
)
async def run_research(
    data: ResearchRunRequest,
    service: Annotated[ResearchService, Depends(get_research_service)],
    request_id: Annotated[str | None, Depends(get_request_id_dep)],
    execution_time_ms: Annotated[float, Depends(get_execution_time_dep)],
) -> ResearchEnvelope:
    """Execute research workflow endpoint."""
    tasks_model = [
        TaskModel(
            id=t.id,
            title=t.title,
            description=t.description,
            priority=t.priority,
            reason=t.reason,
        )
        for t in data.plan.tasks
    ]

    plan_model = PlannerResult(
        goal=data.plan.goal,
        summary=data.plan.summary,
        tasks=tasks_model,
        dependencies=data.plan.dependencies,
        expected_output=data.plan.expected_output,
        estimated_steps=data.plan.estimated_steps,
        estimated_complexity=data.plan.estimated_complexity,
        clarification_required=data.plan.clarification_required,
        clarification_questions=data.plan.clarification_questions,
    )

    result = service.execute_research(data.session_id, plan_model)

    evidence_schemas = [
        EvidenceSchema(
            id=e.id,
            title=e.title,
            summary=e.summary,
            source=e.source,
            tool_used=e.tool_used,
            confidence=e.confidence,
            metadata=e.metadata,
        )
        for e in result.evidence_items
    ]

    result_schema = ResearchResultSchema(
        session_id=result.session_id,
        goal=result.goal,
        summary=result.summary,
        evidence_items=evidence_schemas,
        sources_consulted=result.sources_consulted,
        tools_executed=result.tools_executed,
    )

    return ResearchEnvelope(
        success=True,
        message="Research workflow executed and evidence gathered successfully.",
        request_id=request_id,
        data=result_schema,
        metadata=ResponseMetadata(
            execution_time_ms=execution_time_ms,
            api_version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT.value,
        ),
    )
