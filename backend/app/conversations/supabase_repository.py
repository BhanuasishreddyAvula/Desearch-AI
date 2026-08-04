"""Supabase implementation of AbstractConversationRepository."""

from datetime import datetime
import time
from typing import Any, Callable, TypeVar

from app.conversations.models import ConversationMessage
from app.conversations.repository import AbstractConversationRepository
from app.core.database import get_supabase_client
from app.core.exceptions import AppException
from app.observability.logger import get_app_logger

logger = get_app_logger("conversations.supabase_repository")

TABLE = "conversation_messages"
T = TypeVar("T")


def _execute_with_retry(operation: Callable[[], T], max_retries: int = 3) -> T:
    """Execute a Supabase query with automatic retry for transient network drops."""
    for attempt in range(1, max_retries + 1):
        try:
            return operation()
        except Exception as exc:
            err_msg = str(exc)
            if ("getaddrinfo failed" in err_msg or "ConnectError" in err_msg or "ConnectionRefused" in err_msg) and attempt < max_retries:
                logger.warning(
                    "Supabase connection dropped (%s). Retrying attempt %d/%d...",
                    err_msg,
                    attempt + 1,
                    max_retries,
                )
                time.sleep(0.5 * attempt)
                continue
            raise


class SupabaseConversationRepository(AbstractConversationRepository):
    """Supabase PostgreSQL implementation of AbstractConversationRepository."""

    @property
    def client(self) -> Any:
        return get_supabase_client()

    def create(self, message: ConversationMessage) -> ConversationMessage:
        """Insert a new conversation message row into Supabase."""
        try:
            payload = self._to_row(message)
            response = _execute_with_retry(
                lambda: self.client.table(TABLE).insert(payload).execute()
            )
            if not response.data:
                raise AppException(
                    message="Failed to insert conversation message",
                    error_code="DATABASE_INSERT_ERROR",
                )
            return self._to_entity(response.data[0])
        except AppException:
            raise
        except Exception as exc:
            logger.exception("create conversation message failed: %s", str(exc))
            raise AppException(
                message=f"Database error persisting message: {str(exc)}",
                error_code="DATABASE_ERROR",
            ) from exc

    def list_by_session(
        self, session_id: str, limit: int | None = None, offset: int = 0
    ) -> list[ConversationMessage]:
        """Retrieve messages for a session ordered created_at ASC."""
        try:
            def _run():
                query = (
                    self.client.table(TABLE)
                    .select("*")
                    .eq("session_id", session_id)
                    .order("created_at", desc=False)
                    .offset(offset)
                )
                if limit is not None:
                    query = query.limit(limit)
                return query.execute()

            response = _execute_with_retry(_run)
            return [self._to_entity(row) for row in (response.data or [])]
        except Exception as exc:
            logger.exception("list_by_session failed: %s", str(exc))
            raise AppException(
                message=f"Database error listing messages: {str(exc)}",
                error_code="DATABASE_ERROR",
            ) from exc

    def count_by_session(self, session_id: str) -> int:
        """Return total message count for a session."""
        try:
            response = _execute_with_retry(
                lambda: self.client.table(TABLE)
                .select("id", count="exact")
                .eq("session_id", session_id)
                .execute()
            )
            return response.count or 0
        except Exception as exc:
            logger.exception("count_by_session failed: %s", str(exc))
            return 0

    def delete_by_session(self, session_id: str) -> None:
        """Delete all messages for a session."""
        try:
            _execute_with_retry(
                lambda: self.client.table(TABLE).delete().eq("session_id", session_id).execute()
            )
        except Exception as exc:
            logger.exception("delete_by_session failed: %s", str(exc))

    def delete_after_message(self, session_id: str, message_id: str) -> None:
        """Delete target message and all downstream messages for a session starting at message_id."""
        try:
            # Fetch target message created_at timestamp to purge target & downstream turns
            resp = _execute_with_retry(
                lambda: self.client.table(TABLE).select("created_at").eq("id", message_id).execute()
            )
            if resp.data and len(resp.data) > 0:
                target_created_at = resp.data[0]["created_at"]
                _execute_with_retry(
                    lambda: self.client.table(TABLE).delete().eq("session_id", session_id).gte("created_at", target_created_at).execute()
                )
                logger.info("Purged downstream conversation messages from session %s starting at timestamp %s", session_id, target_created_at)
            else:
                _execute_with_retry(
                    lambda: self.client.table(TABLE).delete().eq("id", message_id).execute()
                )
        except Exception as exc:
            logger.exception("delete_after_message failed: %s", str(exc))

    def delete_from_index(self, session_id: str, turn_index: int) -> None:
        """Delete downstream conversation messages starting from 0-based turn index onwards."""
        try:
            messages = self.list_by_session(session_id)
            skip_count = turn_index * 2
            if len(messages) > skip_count:
                to_delete_ids = [msg.id for msg in messages[skip_count:]]
                _execute_with_retry(
                    lambda: self.client.table(TABLE).delete().in_("id", to_delete_ids).execute()
                )
                logger.info(
                    "Purged %d downstream conversation messages from session %s starting at turn_index %d",
                    len(to_delete_ids),
                    session_id,
                    turn_index,
                )
        except Exception as exc:
            logger.exception("delete_from_index failed: %s", str(exc))

    # ─── Conversion Helpers ──────────────────────────────────────────────────

    @staticmethod
    def _to_entity(row: dict[str, Any]) -> ConversationMessage:
        created_at_str = str(row["created_at"])
        created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
        return ConversationMessage(
            id=str(row["id"]),
            session_id=str(row["session_id"]),
            role=str(row["role"]),
            content=str(row.get("content", "")),
            metadata=row.get("metadata") or {},
            created_at=created_at,
        )

    @staticmethod
    def _to_row(msg: ConversationMessage) -> dict[str, Any]:
        return {
            "id": msg.id,
            "session_id": msg.session_id,
            "role": msg.role,
            "content": msg.content,
            "metadata": msg.metadata,
        }
