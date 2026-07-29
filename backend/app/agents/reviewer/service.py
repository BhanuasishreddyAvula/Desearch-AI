"""Service layer for Reviewer Agent quality evaluation."""

from app.agents.planner.models import PlannerResult
from app.agents.research.models import ResearchResult
from app.agents.reviewer.models import ReviewResult
from app.agents.reviewer.reviewer import ReviewerAgent
from app.agents.writer.models import ReportResult
from app.core.exceptions import ResourceNotFoundException
from app.core.repositories.session import AbstractSessionRepository


class ReviewerService:
    """Service handling report quality evaluation workflows."""

    def __init__(
        self,
        session_repository: AbstractSessionRepository,
        reviewer_agent: ReviewerAgent,
    ) -> None:
        self.session_repository = session_repository
        self.reviewer_agent = reviewer_agent

    def evaluate_report(
        self,
        session_id: str,
        plan: PlannerResult,
        research: ResearchResult,
        report: ReportResult,
    ) -> ReviewResult:
        """Validate research session and execute ReviewerAgent evaluation."""
        session = self.session_repository.get_by_id(session_id)
        if not session:
            raise ResourceNotFoundException(
                message=f"Research session '{session_id}' was not found."
            )

        return self.reviewer_agent.review_report(
            session_id=session_id,
            planner_result=plan,
            research_result=research,
            report_result=report,
        )
