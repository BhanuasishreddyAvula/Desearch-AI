"""API router for Planner Agent endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.agents.planner.planner import PlannerAgent
from app.agents.planner.schemas import (
    PlanEnvelope,
    PlanRequest,
    PlannerResultSchema,
    TaskSchema,
)
from app.agents.planner.service import PlannerService
from app.core.config import settings
from app.core.llm.client import LLMClient
from app.core.repositories.session import AbstractSessionRepository
from app.dependencies import (
    get_execution_time_dep,
    get_llm_client_dep,
    get_request_id_dep,
    get_session_repository_dep,
)
from app.schemas.metadata import ResponseMetadata

router = APIRouter(tags=["Planner", "Agents"])


def get_planner_agent(
    llm_client: Annotated[LLMClient, Depends(get_llm_client_dep)],
) -> PlannerAgent:
    """Dependency provider returning PlannerAgent instance with injected LLMClient."""
    return PlannerAgent(llm_client=llm_client)


def get_planner_service(
    session_repo: Annotated[
        AbstractSessionRepository, Depends(get_session_repository_dep)
    ],
    planner_agent: Annotated[PlannerAgent, Depends(get_planner_agent)],
) -> PlannerService:
    """Dependency provider injecting PlannerService."""
    return PlannerService(
        session_repository=session_repo, planner_agent=planner_agent
    )


@router.post(
    "/plan",
    response_model=PlanEnvelope,
    summary="Generate Research Plan",
    description="Analyze a ResearchSession query and generate a structured multi-step Research Execution Plan.",
)
async def generate_plan(
    data: PlanRequest,
    service: Annotated[PlannerService, Depends(get_planner_service)],
    request_id: Annotated[str | None, Depends(get_request_id_dep)],
    execution_time_ms: Annotated[float, Depends(get_execution_time_dep)],
) -> PlanEnvelope:
    """Generate research plan endpoint."""
    result = service.create_plan(data.session_id)

    tasks_schema = [
        TaskSchema(
            id=t.id,
            title=t.title,
            description=t.description,
            priority=t.priority,
            reason=t.reason,
        )
        for t in result.tasks
    ]

    result_schema = PlannerResultSchema(
        goal=result.goal,
        summary=result.summary,
        tasks=tasks_schema,
        dependencies=result.dependencies,
        expected_output=result.expected_output,
        estimated_steps=result.estimated_steps,
        estimated_complexity=result.estimated_complexity,
        clarification_required=result.clarification_required,
        clarification_questions=result.clarification_questions,
    )

    return PlanEnvelope(
        success=True,
        message="Research execution plan generated successfully.",
        request_id=request_id,
        data=result_schema,
        metadata=ResponseMetadata(
            execution_time_ms=execution_time_ms,
            api_version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT.value,
        ),
    )
