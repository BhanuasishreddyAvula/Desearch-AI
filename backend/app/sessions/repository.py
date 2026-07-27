"""In-memory repository for ResearchSession entities."""

from app.sessions.models import ResearchSession


class SessionRepository:
    """In-memory dictionary storage for research session entities."""

    def __init__(self) -> None:
        self._storage: dict[str, ResearchSession] = {}

    def create(self, session: ResearchSession) -> ResearchSession:
        """Store a new research session in memory."""
        self._storage[session.id] = session
        return session

    def get_by_id(self, session_id: str) -> ResearchSession | None:
        """Retrieve a session entity by ID."""
        return self._storage.get(session_id)

    def list_all(self) -> list[ResearchSession]:
        """List all stored research sessions ordered by creation time descending."""
        sessions = list(self._storage.values())
        return sorted(sessions, key=lambda s: s.created_at, reverse=True)

    def update(self, session: ResearchSession) -> ResearchSession:
        """Update an existing session entity in memory."""
        self._storage[session.id] = session
        return session

    def delete(self, session_id: str) -> bool:
        """Delete a session entity by ID."""
        if session_id in self._storage:
            del self._storage[session_id]
            return True
        return False


# Shared singleton in-memory repository instance for MVP
session_repository = SessionRepository()
