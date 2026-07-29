"""API router for Multi-Agent Orchestrator endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.agents.planner.router import get_planner_service
from app.agents.planner.schemas import PlannerResultSchema, TaskSchema
from app.agents.planner.service import PlannerService
from app.agents.research.router import get_research_service
from app.agents.research.schemas import EvidenceSchema, ResearchResultSchema
from app.agents.research.service import ResearchService
from app.agents.reviewer.router import get_reviewer_service
from app.agents.reviewer.schemas import ReviewResultSchema
from app.agents.reviewer.service import ReviewerService
from app.agents.writer.router import get_writer_service
from app.agents.writer.schemas import (
    ReportMetadataSchema,
    ReportResultSchema,
    ReportSectionSchema,
)
from app.agents.writer.service import WriterService
from app.core.config import settings
from app.core.repositories.session import AbstractSessionRepository
from app.dependencies import (
    get_execution_time_dep,
    get_request_id_dep,
    get_session_repository_dep,
)
from app.orchestrator.orchestrator import MultiAgentOrchestrator
from app.orchestrator.schemas import (
    AgentExecutionSchema,
    WorkflowEnvelope,
    WorkflowResultSchema,
    WorkflowRunRequest,
)
from app.orchestrator.service import OrchestratorService
from app.schemas.metadata import ResponseMetadata

router = APIRouter(tags=["Orchestrator"])


def get_multi_agent_orchestrator(
    planner_service: Annotated[PlannerService, Depends(get_planner_service)],
    research_service: Annotated[
        ResearchService, Depends(get_research_service)
    ],
    writer_service: Annotated[WriterService, Depends(get_writer_service)],
    reviewer_service: Annotated[
        ReviewerService, Depends(get_reviewer_service)
    ],
) -> MultiAgentOrchestrator:
    """Dependency provider creating MultiAgentOrchestrator instance."""
    return MultiAgentOrchestrator(
        planner_service=planner_service,
        research_service=research_service,
        writer_service=writer_service,
        reviewer_service=reviewer_service,
    )


def get_orchestrator_service(
    session_repo: Annotated[
        AbstractSessionRepository, Depends(get_session_repository_dep)
    ],
    orchestrator: Annotated[
        MultiAgentOrchestrator, Depends(get_multi_agent_orchestrator)
    ],
) -> OrchestratorService:
    """Dependency provider creating OrchestratorService instance."""
    return OrchestratorService(
        session_repository=session_repo, orchestrator=orchestrator
    )


@router.post(
    "/run",
    response_model=WorkflowEnvelope,
    summary="Run Multi-Agent Research Workflow",
    description="Coordinate sequential multi-agent execution (Planner Agent -> Research Agent -> Writer Agent -> Reviewer Agent).",
)
async def run_workflow(
    data: WorkflowRunRequest,
    service: Annotated[OrchestratorService, Depends(get_orchestrator_service)],
    request_id: Annotated[str | None, Depends(get_request_id_dep)],
    execution_time_ms: Annotated[float, Depends(get_execution_time_dep)],
) -> WorkflowEnvelope:
    """Execute multi-agent workflow endpoint."""
    result = service.execute_session_workflow(data.session_id, data.query)

    planner_tasks = [
        TaskSchema(
            id=t.id,
            title=t.title,
            description=t.description,
            priority=t.priority,
            reason=t.reason,
        )
        for t in result.planner_result.tasks
    ]

    planner_schema = PlannerResultSchema(
        goal=result.planner_result.goal,
        summary=result.planner_result.summary,
        tasks=planner_tasks,
        dependencies=result.planner_result.dependencies,
        expected_output=result.planner_result.expected_output,
        estimated_steps=result.planner_result.estimated_steps,
        estimated_complexity=result.planner_result.estimated_complexity,
        clarification_required=result.planner_result.clarification_required,
        clarification_questions=result.planner_result.clarification_questions,
    )

    research_evidence = [
        EvidenceSchema(
            id=e.id,
            title=e.title,
            summary=e.summary,
            source=e.source,
            tool_used=e.tool_used,
            confidence=e.confidence,
            metadata=e.metadata,
        )
        for e in result.research_result.evidence_items
    ]

    research_schema = ResearchResultSchema(
        session_id=result.research_result.session_id,
        goal=result.research_result.goal,
        summary=result.research_result.summary,
        evidence_items=research_evidence,
        sources_consulted=result.research_result.sources_consulted,
        tools_executed=result.research_result.tools_executed,
    )

    report_sections = [
        ReportSectionSchema(
            title=s.title,
            content=s.content,
            level=s.level,
        )
        for s in result.report_result.sections
    ]

    report_metadata = ReportMetadataSchema(
        word_count=result.report_result.metadata.word_count,
        sections_count=result.report_result.metadata.sections_count,
        evidence_cited_count=result.report_result.metadata.evidence_cited_count,
        sources_count=result.report_result.metadata.sources_count,
    )

    report_schema = ReportResultSchema(
        session_id=result.report_result.session_id,
        title=result.report_result.title,
        executive_summary=result.report_result.executive_summary,
        full_markdown=result.report_result.full_markdown,
        sections=report_sections,
        sources_cited=result.report_result.sources_cited,
        metadata=report_metadata,
    )

    review_schema = ReviewResultSchema(
        session_id=result.review_result.session_id,
        approved=result.review_result.approved,
        overall_score=result.review_result.overall_score,
        confidence=result.review_result.confidence,
        summary=result.review_result.summary,
        strengths=result.review_result.strengths,
        issues=result.review_result.issues,
        missing_evidence=result.review_result.missing_evidence,
        unsupported_claims=result.review_result.unsupported_claims,
        recommendations=result.review_result.recommendations,
    )

    execution_schemas = [
        AgentExecutionSchema(
            agent_name=ex.agent_name,
            step=ex.step.value if hasattr(ex.step, "value") else str(ex.step),
            status=ex.status.value
            if hasattr(ex.status, "value")
            else str(ex.status),
            execution_time_ms=ex.execution_time_ms,
            details=ex.details,
        )
        for ex in result.executions
    ]

    result_schema = WorkflowResultSchema(
        session_id=result.session_id,
        status=result.status.value
        if hasattr(result.status, "value")
        else str(result.status),
        planner_result=planner_schema,
        research_result=research_schema,
        report_result=report_schema,
        review_result=review_schema,
        executions=execution_schemas,
        total_execution_time_ms=result.total_execution_time_ms,
    )

    return WorkflowEnvelope(
        success=True,
        message="Multi-agent research workflow completed successfully.",
        request_id=request_id,
        data=result_schema,
        metadata=ResponseMetadata(
            execution_time_ms=execution_time_ms,
            api_version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT.value,
        ),
    )
