"""API router for Reviewer Agent endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.agents.planner.models import PlannerResult, TaskModel
from app.agents.research.models import Evidence, ResearchResult
from app.agents.reviewer.reviewer import ReviewerAgent
from app.agents.reviewer.schemas import (
    ReviewEnvelope,
    ReviewResultSchema,
    ReviewRunRequest,
)
from app.agents.reviewer.service import ReviewerService
from app.agents.writer.models import ReportMetadata, ReportResult, ReportSection
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

router = APIRouter(tags=["Reviewer", "Agents"])


def get_reviewer_agent(
    llm_client: Annotated[LLMClient, Depends(get_llm_client_dep)],
) -> ReviewerAgent:
    """Dependency provider returning ReviewerAgent instance."""
    return ReviewerAgent(llm_client=llm_client)


def get_reviewer_service(
    session_repo: Annotated[
        AbstractSessionRepository, Depends(get_session_repository_dep)
    ],
    reviewer_agent: Annotated[ReviewerAgent, Depends(get_reviewer_agent)],
) -> ReviewerService:
    """Dependency provider injecting ReviewerService."""
    return ReviewerService(
        session_repository=session_repo, reviewer_agent=reviewer_agent
    )


@router.post(
    "/review",
    response_model=ReviewEnvelope,
    summary="Evaluate Report Quality",
    description="Compare generated ReportResult against PlannerResult and ResearchResult evidence collection.",
)
async def review_report(
    data: ReviewRunRequest,
    service: Annotated[ReviewerService, Depends(get_reviewer_service)],
    request_id: Annotated[str | None, Depends(get_request_id_dep)],
    execution_time_ms: Annotated[float, Depends(get_execution_time_dep)],
) -> ReviewEnvelope:
    """Evaluate report endpoint."""
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

    sections = [
        ReportSection(title=s.title, content=s.content, level=s.level)
        for s in data.report.sections
    ]
    metadata = ReportMetadata(
        word_count=data.report.metadata.word_count,
        sections_count=data.report.metadata.sections_count,
        evidence_cited_count=data.report.metadata.evidence_cited_count,
        sources_count=data.report.metadata.sources_count,
    )
    report_model = ReportResult(
        session_id=data.report.session_id,
        title=data.report.title,
        executive_summary=data.report.executive_summary,
        full_markdown=data.report.full_markdown,
        sections=sections,
        sources_cited=data.report.sources_cited,
        metadata=metadata,
    )

    result = service.evaluate_report(
        data.session_id, planner_model, research_model, report_model
    )

    result_schema = ReviewResultSchema(
        session_id=result.session_id,
        approved=result.approved,
        overall_score=result.overall_score,
        confidence=result.confidence,
        summary=result.summary,
        strengths=result.strengths,
        issues=result.issues,
        missing_evidence=result.missing_evidence,
        unsupported_claims=result.unsupported_claims,
        recommendations=result.recommendations,
    )

    return ReviewEnvelope(
        success=True,
        message="Report quality evaluation completed successfully.",
        request_id=request_id,
        data=result_schema,
        metadata=ResponseMetadata(
            execution_time_ms=execution_time_ms,
            api_version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT.value,
        ),
    )
