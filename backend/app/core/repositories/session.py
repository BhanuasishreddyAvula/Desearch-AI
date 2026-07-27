"""Abstract session repository interface."""

from abc import ABC

from app.core.repositories.base import BaseRepository
from app.sessions.models import ResearchSession


class AbstractSessionRepository(BaseRepository[ResearchSession, str], ABC):
    """Abstract repository interface for ResearchSession entity domain."""

    ...
