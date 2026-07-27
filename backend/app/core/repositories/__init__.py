"""Core repository interfaces package re-exporting base and domain contracts."""

from app.core.repositories.base import BaseRepository
from app.core.repositories.session import AbstractSessionRepository

__all__ = ["BaseRepository", "AbstractSessionRepository"]
