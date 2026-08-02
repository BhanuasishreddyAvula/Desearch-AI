"""Abstract repository interface for ConversationMessage persistence."""

from abc import ABC, abstractmethod

from app.conversations.models import ConversationMessage


class AbstractConversationRepository(ABC):
    """Abstract interface for persisting and retrieving conversation messages."""

    @abstractmethod
    def create(self, message: ConversationMessage) -> ConversationMessage:
        """Persist a new conversation message."""
        ...

    @abstractmethod
    def list_by_session(
        self, session_id: str, limit: int | None = None, offset: int = 0
    ) -> list[ConversationMessage]:
        """Retrieve messages for a session ordered by created_at ASC."""
        ...

    @abstractmethod
    def count_by_session(self, session_id: str) -> int:
        """Return the total number of messages for a session."""
        ...

    @abstractmethod
    def delete_by_session(self, session_id: str) -> None:
        """Delete all messages belonging to a session (cascade on session delete)."""
        ...
