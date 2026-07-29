"""Service layer for Writer Agent report generation."""

from app.agents.planner.models import PlannerResult
from app.agents.research.models import ResearchResult
from app.agents.writer.models import ReportResult
from app.agents.writer.writer import WriterAgent
from app.core.exceptions import ResourceNotFoundException
from app.core.repositories.session import AbstractSessionRepository


class WriterService:
    """Service handling report creation workflows."""

    def __init__(
        self,
        session_repository: AbstractSessionRepository,
        writer_agent: WriterAgent,
    ) -> None:
        self.session_repository = session_repository
        self.writer_agent = writer_agent

    def create_report(
        self,
        session_id: str,
        plan: PlannerResult,
        research: ResearchResult,
    ) -> ReportResult:
        """Validate research session and execute WriterAgent report synthesis."""
        session = self.session_repository.get_by_id(session_id)
        if not session:
            raise ResourceNotFoundException(
                message=f"Research session '{session_id}' was not found."
            )

        return self.writer_agent.write_report(
            session_id=session_id,
            planner_result=plan,
            research_result=research,
        )
