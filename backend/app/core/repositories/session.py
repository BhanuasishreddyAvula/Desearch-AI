"""Abstract session repository interface."""

from abc import ABC, abstractmethod

from app.core.repositories.base import BaseRepository
from app.sessions.models import ResearchSession


class AbstractSessionRepository(BaseRepository[ResearchSession, str], ABC):
    """Abstract repository interface for ResearchSession entity domain."""

    @abstractmethod
    def list_by_device(self, device_id: str) -> list[ResearchSession]:
        """Retrieve all sessions belonging to a specific device, ordered by updated_at DESC."""
        ...
