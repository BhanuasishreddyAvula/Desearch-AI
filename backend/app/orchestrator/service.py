"""Service layer for Multi-Agent Orchestrator."""

from collections.abc import Callable

from app.core.exceptions import ResourceNotFoundException
from app.core.repositories.session import AbstractSessionRepository
from app.orchestrator.events import (
    ProgressEvent,
    ProgressEventType,
    create_progress_event,
)
from app.orchestrator.models import WorkflowResult
from app.orchestrator.orchestrator import MultiAgentOrchestrator
from app.sessions.enums import SessionStatus


class OrchestratorService:
    """Service validating session state, executing multi-agent workflow, and persisting report."""

    def __init__(
        self,
        session_repository: AbstractSessionRepository,
        orchestrator: MultiAgentOrchestrator,
    ) -> None:
        self.session_repository = session_repository
        self.orchestrator = orchestrator

    def execute_session_workflow(
        self,
        session_id: str,
        query: str,
        progress_listener: Callable[[ProgressEvent], None] | None = None,
    ) -> WorkflowResult:
        """Validate session in Supabase, trigger Orchestrator flow, and persist canonical report."""
        session = self.session_repository.get_by_id(session_id)
        if not session:
            raise ResourceNotFoundException(
                message=f"Research session '{session_id}' was not found."
            )

        session.status = SessionStatus.PLANNING
        self.session_repository.update(session)

        try:
            workflow_result = self.orchestrator.run_workflow(
                session_id=session_id,
                query=query,
                progress_listener=progress_listener,
            )

            # Update session status to COMPLETED and persist canonical report_result in metadata
            session.status = SessionStatus.COMPLETED
            session.metadata["report_result"] = {
                "session_id": workflow_result.report_result.session_id,
                "title": workflow_result.report_result.title,
                "executive_summary": workflow_result.report_result.executive_summary,
                "full_markdown": workflow_result.report_result.full_markdown,
                "sections": [
                    {
                        "title": s.title,
                        "content": s.content,
                        "level": s.level,
                    }
                    for s in workflow_result.report_result.sections
                ],
                "sources_cited": workflow_result.report_result.sources_cited,
                "metadata": {
                    "word_count": workflow_result.report_result.metadata.word_count,
                    "sections_count": workflow_result.report_result.metadata.sections_count,
                    "evidence_cited_count": workflow_result.report_result.metadata.evidence_cited_count,
                    "sources_count": workflow_result.report_result.metadata.sources_count,
                },
            }
            session.metadata["review_result"] = {
                "approved": workflow_result.review_result.approved,
                "overall_score": workflow_result.review_result.overall_score,
            }

            self.session_repository.update(session)

            if progress_listener:
                progress_listener(
                    create_progress_event(
                        ProgressEventType.REPORT_PERSISTED,
                        "Persistence",
                        "Report persisted to database",
                        session_id,
                    )
                )
                progress_listener(
                    create_progress_event(
                        ProgressEventType.WORKFLOW_COMPLETED,
                        "Completed",
                        "Research workflow completed successfully.",
                        session_id,
                        {"total_execution_time_ms": workflow_result.total_execution_time_ms},
                    )
                )

            return workflow_result
        except Exception:
            session.status = SessionStatus.FAILED
            self.session_repository.update(session)
            raise
