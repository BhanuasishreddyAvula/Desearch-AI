"""ContextBuilder — assembles a bounded conversation context window for agent injection."""

from app.conversations.models import ConversationContext, ConversationMessage
from app.conversations.repository import AbstractConversationRepository
from app.observability.logger import get_app_logger

logger = get_app_logger("conversations.context_builder")

# Configurable bounds
CONTEXT_WINDOW_MESSAGES = 8     # Max recent messages to include verbatim (= 4 pairs)
SUMMARY_TRIGGER_COUNT = 16      # Start using rolling summary above this count


def _format_messages(messages: list[ConversationMessage]) -> str:
    """Render a list of messages into a compact, readable conversation string."""
    lines: list[str] = []
    for msg in messages:
        prefix = "User" if msg.role == "user" else "Assistant"
        # For assistant messages, use the content field (executive summary or query)
        text = msg.content.strip()
        if len(text) > 800:
            text = text[:800] + "…"
        lines.append(f"[{prefix}]: {text}")
    return "\n\n".join(lines)


class ContextBuilder:
    """
    Builds a bounded conversation context window from persisted messages.

    Strategy:
    - Fetch total message count for the session.
    - If count <= SUMMARY_TRIGGER_COUNT: include all messages as recent context.
    - If count > SUMMARY_TRIGGER_COUNT: use rolling_summary from session metadata
      for older turns, and verbatim recent CONTEXT_WINDOW_MESSAGES messages.
    """

    def __init__(self, repository: AbstractConversationRepository) -> None:
        self.repository = repository

    def build_context(
        self,
        session_id: str,
        current_query: str,
        rolling_summary: str = "",
    ) -> ConversationContext:
        """
        Build a ConversationContext ready for injection into agent prompts.

        Args:
            session_id:      The research session UUID.
            current_query:   The new user question being asked now.
            rolling_summary: Pre-existing conversation summary (from session.metadata).
        """
        total_count = self.repository.count_by_session(session_id)

        if total_count == 0:
            # First question in this session — no history
            return ConversationContext(
                session_id=session_id,
                current_query=current_query,
                recent_context_text="",
                rolling_summary="",
                total_message_count=0,
            )

        # Always fetch last CONTEXT_WINDOW_MESSAGES messages verbatim
        recent_messages = self.repository.list_by_session(
            session_id, limit=CONTEXT_WINDOW_MESSAGES
        )

        # Use rolling summary only when conversation exceeds threshold
        effective_summary = rolling_summary if total_count > SUMMARY_TRIGGER_COUNT else ""

        recent_text = _format_messages(recent_messages)

        logger.info(
            "Context built | session=%s | total=%d | recent=%d | has_summary=%s",
            session_id,
            total_count,
            len(recent_messages),
            bool(effective_summary),
        )

        return ConversationContext(
            session_id=session_id,
            current_query=current_query,
            recent_context_text=recent_text,
            rolling_summary=effective_summary,
            total_message_count=total_count,
        )

    def should_refresh_summary(self, session_id: str) -> bool:
        """Return True if the message count is above SUMMARY_TRIGGER_COUNT."""
        return self.repository.count_by_session(session_id) > SUMMARY_TRIGGER_COUNT
