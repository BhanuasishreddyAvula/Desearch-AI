"""Service layer for Multi-Agent Orchestrator."""

from app.core.exceptions import ResourceNotFoundException
from app.core.repositories.session import AbstractSessionRepository
from app.orchestrator.models import WorkflowResult
from app.orchestrator.orchestrator import MultiAgentOrchestrator


class OrchestratorService:
    """Service validating session state and executing multi-agent workflow."""

    def __init__(
        self,
        session_repository: AbstractSessionRepository,
        orchestrator: MultiAgentOrchestrator,
    ) -> None:
        self.session_repository = session_repository
        self.orchestrator = orchestrator

    def execute_session_workflow(
        self, session_id: str, query: str
    ) -> WorkflowResult:
        """Validate session in Supabase and trigger Orchestrator execution flow."""
        session = self.session_repository.get_by_id(session_id)
        if not session:
            raise ResourceNotFoundException(
                message=f"Research session '{session_id}' was not found."
            )

        return self.orchestrator.run_workflow(
            session_id=session_id, query=query
        )
