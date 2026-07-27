"""In-memory implementation of AbstractSessionRepository."""

from app.core.repositories.session import AbstractSessionRepository
from app.sessions.models import ResearchSession


class InMemorySessionRepository(AbstractSessionRepository):
    """In-memory dictionary storage implementation of AbstractSessionRepository."""

    def __init__(self) -> None:
        self._storage: dict[str, ResearchSession] = {}

    def create(self, entity: ResearchSession) -> ResearchSession:
        """Store a new research session in memory."""
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, id_val: str) -> ResearchSession | None:
        """Retrieve a session entity by ID."""
        return self._storage.get(id_val)

    def list_all(self) -> list[ResearchSession]:
        """List all stored research sessions ordered by creation time descending."""
        sessions = list(self._storage.values())
        return sorted(sessions, key=lambda s: s.created_at, reverse=True)

    def update(self, entity: ResearchSession) -> ResearchSession:
        """Update an existing session entity in memory."""
        self._storage[entity.id] = entity
        return entity

    def delete(self, id_val: str) -> bool:
        """Delete a session entity by ID."""
        if id_val in self._storage:
            del self._storage[id_val]
            return True
        return False
