"""Service layer for Multi-Agent Orchestrator — with conversation context & message persistence."""

import uuid
from collections.abc import Callable

from app.conversations.context_builder import ContextBuilder
from app.conversations.models import ConversationMessage
from app.conversations.repository import AbstractConversationRepository
from app.core.exceptions import ResourceNotFoundException
from app.core.repositories.session import AbstractSessionRepository
from app.orchestrator import cancel_registry
from app.orchestrator.events import (
    ProgressEvent,
    ProgressEventType,
    create_progress_event,
)
from app.orchestrator.models import WorkflowResult
from app.orchestrator.orchestrator import MultiAgentOrchestrator, WorkflowCancelledError
from app.sessions.enums import SessionStatus


class OrchestratorService:
    """Service validating session state, building conversation context, executing the
    multi-agent workflow, and persisting the resulting conversation messages."""

    def __init__(
        self,
        session_repository: AbstractSessionRepository,
        orchestrator: MultiAgentOrchestrator,
        conversation_repository: AbstractConversationRepository | None = None,
    ) -> None:
        self.session_repository = session_repository
        self.orchestrator = orchestrator
        self.conversation_repository = conversation_repository
        self._context_builder = (
            ContextBuilder(conversation_repository) if conversation_repository else None
        )

    def execute_session_workflow(
        self,
        session_id: str,
        query: str,
        progress_listener: Callable[[ProgressEvent], None] | None = None,
        device_id: str = "",
    ) -> WorkflowResult:
        """Validate session, build conversation context, run workflow, persist messages."""
        session = self.session_repository.get_by_id(session_id)
        if not session:
            raise ResourceNotFoundException(
                message=f"Research session '{session_id}' was not found."
            )
        # Enforce device ownership — allow access if session belongs to device or is legacy nil UUID
        nil_uuid = "00000000-0000-0000-0000-000000000000"
        if (
            device_id
            and session.device_id
            and session.device_id != nil_uuid
            and session.device_id != device_id
        ):
            raise ResourceNotFoundException(
                message=f"Research session '{session_id}' was not found."
            )


        # ─── Build conversation context window ───────────────────────────────
        conversation_context = ""
        rolling_summary = session.metadata.get("conversation_summary", "")
        if self._context_builder:
            ctx = self._context_builder.build_context(
                session_id=session_id,
                current_query=query,
                rolling_summary=rolling_summary,
            )
            conversation_context = ctx.build_context_string()

        session.status = SessionStatus.PLANNING
        self.session_repository.update(session)

        # Create a fresh cancel token for this workflow run (previous token is discarded)
        cancel_token = cancel_registry.create_cancel_token(session_id)

        try:
            workflow_result = self.orchestrator.run_workflow(
                session_id=session_id,
                query=query,
                progress_listener=progress_listener,
                conversation_context=conversation_context,
                cancel_token=cancel_token,
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

            # ─── Persist conversation messages ────────────────────────────────
            if self.conversation_repository:
                pair_id = str(uuid.uuid4())

                # 1. User message
                user_msg = ConversationMessage(
                    session_id=session_id,
                    role="user",
                    content=query,
                    metadata={"pair_id": pair_id},
                )
                self.conversation_repository.create(user_msg)

                # 2. Assistant message (report)
                report = workflow_result.report_result
                assistant_msg = ConversationMessage(
                    session_id=session_id,
                    role="assistant",
                    content=report.executive_summary or report.title,
                    metadata={
                        "pair_id": pair_id,
                        "title": report.title,
                        "full_markdown": report.full_markdown,
                        "sources_cited": report.sources_cited,
                        "word_count": report.metadata.word_count,
                        "sections_count": report.metadata.sections_count,
                        "total_execution_time_ms": workflow_result.total_execution_time_ms,
                    },
                )
                self.conversation_repository.create(assistant_msg)

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
                        {
                            "total_execution_time_ms": workflow_result.total_execution_time_ms,
                            "report_result": session.metadata["report_result"],
                            "full_markdown": workflow_result.report_result.full_markdown,
                            "sources_cited": workflow_result.report_result.sources_cited,
                        },
                    )
                )

            return workflow_result
        except WorkflowCancelledError:
            # User stopped the agents — mark session as FAILED so the next run starts fresh
            cancel_registry.remove_cancel_token(session_id)
            session.status = SessionStatus.FAILED
            self.session_repository.update(session)
            raise
        except Exception:
            cancel_registry.remove_cancel_token(session_id)
            session.status = SessionStatus.FAILED
            self.session_repository.update(session)
            raise
