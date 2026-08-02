"""Domain models for conversation messages and context."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
import uuid


@dataclass
class ConversationMessage:
    """A single message in a research session conversation."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = ""
    role: str = "user"          # "user" | "assistant"
    content: str = ""           # Plain text content / query
    metadata: dict[str, Any] = field(default_factory=dict)
    # Assistant metadata keys: full_markdown, sources_cited, title, word_count
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class ConversationContext:
    """Assembled bounded context window passed into the research workflow."""

    session_id: str = ""
    current_query: str = ""
    # Recent message pairs formatted as a readable conversation string
    recent_context_text: str = ""
    # Optional rolling summary of older messages beyond the context window
    rolling_summary: str = ""
    # Total message count (used to decide when to refresh summary)
    total_message_count: int = 0

    def build_context_string(self) -> str:
        """Return a single formatted string injected into agent prompts."""
        parts: list[str] = []

        if self.rolling_summary:
            parts.append(
                "=== CONVERSATION SUMMARY (earlier turns) ===\n"
                + self.rolling_summary
            )

        if self.recent_context_text:
            parts.append(
                "=== RECENT CONVERSATION ===\n"
                + self.recent_context_text
            )

        if not parts:
            return ""

        return "\n\n".join(parts)
