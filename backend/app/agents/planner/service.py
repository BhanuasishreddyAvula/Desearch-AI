"""Service orchestrating Planner Agent calls and ResearchSession state retrieval."""

from app.agents.planner.models import PlannerResult
from app.agents.planner.planner import PlannerAgent
from app.core.exceptions import ResourceNotFoundException
from app.core.repositories.session import AbstractSessionRepository


class PlannerService:
    """Service handling research planning requests."""

    def __init__(
        self,
        session_repository: AbstractSessionRepository,
        planner_agent: PlannerAgent,
    ) -> None:
        self.session_repository = session_repository
        self.planner_agent = planner_agent

    def create_plan(
        self, session_id: str, query: str | None = None, conversation_context: str = ""
    ) -> PlannerResult:
        """Retrieve session from repository and generate structured execution plan for current query."""
        session = self.session_repository.get_by_id(session_id)
        if not session:
            raise ResourceNotFoundException(
                message=f"Research session '{session_id}' was not found"
            )

        target_query = query.strip() if (query and query.strip()) else session.query
        return self.planner_agent.generate_plan(target_query, conversation_context=conversation_context)

