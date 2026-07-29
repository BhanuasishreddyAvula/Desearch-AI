"""Service layer orchestrating Research Agent execution."""

from app.agents.planner.models import PlannerResult
from app.agents.research.models import ResearchResult
from app.agents.research.research import ResearchAgent
from app.core.exceptions import ResourceNotFoundException
from app.core.repositories.session import AbstractSessionRepository


class ResearchService:
    """Service handling research execution against PlannerResult plans."""

    def __init__(
        self,
        session_repository: AbstractSessionRepository,
        research_agent: ResearchAgent,
    ) -> None:
        self.session_repository = session_repository
        self.research_agent = research_agent

    def execute_research(
        self, session_id: str, plan: PlannerResult
    ) -> ResearchResult:
        """Verify research session existence and execute ResearchAgent workflow."""
        session = self.session_repository.get_by_id(session_id)
        if not session:
            raise ResourceNotFoundException(
                message=f"Research session '{session_id}' was not found."
            )

        tasks_dict = [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "priority": t.priority,
            }
            for t in plan.tasks
        ]

        return self.research_agent.run_research(
            session_id=session_id,
            goal=plan.goal or session.query,
            tasks=tasks_dict,
        )
