"""API router for Writer Agent endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.agents.planner.models import PlannerResult, TaskModel
from app.agents.research.models import Evidence, ResearchResult
from app.agents.writer.schemas import (
    ReportEnvelope,
    ReportMetadataSchema,
    ReportResultSchema,
    ReportSectionSchema,
    WriterRunRequest,
)
from app.agents.writer.service import WriterService
from app.agents.writer.writer import WriterAgent
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

router = APIRouter(tags=["Writer", "Agents"])


def get_writer_agent(
    llm_client: Annotated[LLMClient, Depends(get_llm_client_dep)],
) -> WriterAgent:
    """Dependency provider returning WriterAgent instance."""
    return WriterAgent(llm_client=llm_client)


def get_writer_service(
    session_repo: Annotated[
        AbstractSessionRepository, Depends(get_session_repository_dep)
    ],
    writer_agent: Annotated[WriterAgent, Depends(get_writer_agent)],
) -> WriterService:
    """Dependency provider injecting WriterService."""
    return WriterService(
        session_repository=session_repo, writer_agent=writer_agent
    )


@router.post(
    "/write",
    response_model=ReportEnvelope,
    summary="Generate Research Report",
    description="Transform structured PlannerResult and ResearchResult into a professional Markdown research report.",
)
async def generate_report(
    data: WriterRunRequest,
    service: Annotated[WriterService, Depends(get_writer_service)],
    request_id: Annotated[str | None, Depends(get_request_id_dep)],
    execution_time_ms: Annotated[float, Depends(get_execution_time_dep)],
) -> ReportEnvelope:
    """Generate report endpoint."""
    planner_tasks = [
        TaskModel(
            id=t.id,
            title=t.title,
            description=t.description,
            priority=t.priority,
            reason=t.reason,
        )
        for t in data.plan.tasks
    ]
    planner_model = PlannerResult(
        goal=data.plan.goal,
        summary=data.plan.summary,
        tasks=planner_tasks,
        dependencies=data.plan.dependencies,
        expected_output=data.plan.expected_output,
        estimated_steps=data.plan.estimated_steps,
        estimated_complexity=data.plan.estimated_complexity,
        clarification_required=data.plan.clarification_required,
        clarification_questions=data.plan.clarification_questions,
    )

    evidence_items = [
        Evidence(
            id=e.id,
            title=e.title,
            summary=e.summary,
            source=e.source,
            tool_used=e.tool_used,
            confidence=e.confidence,
            metadata=e.metadata,
        )
        for e in data.research.evidence_items
    ]
    research_model = ResearchResult(
        session_id=data.research.session_id,
        goal=data.research.goal,
        summary=data.research.summary,
        evidence_items=evidence_items,
        sources_consulted=data.research.sources_consulted,
        tools_executed=data.research.tools_executed,
    )

    result = service.create_report(
        data.session_id, planner_model, research_model
    )

    section_schemas = [
        ReportSectionSchema(
            title=s.title,
            content=s.content,
            level=s.level,
        )
        for s in result.sections
    ]

    metadata_schema = ReportMetadataSchema(
        word_count=result.metadata.word_count,
        sections_count=result.metadata.sections_count,
        evidence_cited_count=result.metadata.evidence_cited_count,
        sources_count=result.metadata.sources_count,
    )

    result_schema = ReportResultSchema(
        session_id=result.session_id,
        title=result.title,
        executive_summary=result.executive_summary,
        full_markdown=result.full_markdown,
        sections=section_schemas,
        sources_cited=result.sources_cited,
        metadata=metadata_schema,
    )

    return ReportEnvelope(
        success=True,
        message="Research report generated successfully.",
        request_id=request_id,
        data=result_schema,
        metadata=ResponseMetadata(
            execution_time_ms=execution_time_ms,
            api_version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT.value,
        ),
    )
