"""Supabase PostgreSQL implementation of AbstractSessionRepository."""

from datetime import datetime, timezone
from typing import Any

from app.core.database import get_supabase_client
from app.core.exceptions import AppException
from app.core.repositories.session import AbstractSessionRepository
from app.observability.logger import get_app_logger
from app.sessions.enums import SessionStatus
from app.sessions.models import ResearchSession

logger = get_app_logger("sessions.supabase_repository")


class SupabaseSessionRepository(AbstractSessionRepository):
    """Supabase table-based implementation of AbstractSessionRepository."""

    def __init__(self) -> None:
        self.table_name = "research_sessions"

    @property
    def client(self) -> Any:
        """Retrieve shared Supabase client instance."""
        return get_supabase_client()

    def create(self, entity: ResearchSession) -> ResearchSession:
        """Insert a new research session row into Supabase."""
        try:
            payload = self._entity_to_row(entity)
            response = (
                self.client.table(self.table_name).insert(payload).execute()
            )
            if not response.data:
                raise AppException(
                    message="Failed to insert session row into Supabase",
                    error_code="DATABASE_INSERT_ERROR",
                )
            return self._row_to_entity(response.data[0])
        except AppException:
            raise
        except Exception as exc:
            logger.exception("Supabase create failed: %s", str(exc))
            raise AppException(
                message=f"Database error during session creation: {str(exc)}",
                error_code="DATABASE_ERROR",
            ) from exc

    def get_by_id(self, id_val: str) -> ResearchSession | None:
        """Fetch a research session by UUID primary key from Supabase."""
        try:
            response = (
                self.client.table(self.table_name)
                .select("*")
                .eq("id", id_val)
                .execute()
            )
            if not response.data:
                return None
            return self._row_to_entity(response.data[0])
        except Exception as exc:
            logger.exception("Supabase get_by_id failed: %s", str(exc))
            raise AppException(
                message=f"Database error fetching session: {str(exc)}",
                error_code="DATABASE_ERROR",
            ) from exc

    def list_all(self) -> list[ResearchSession]:
        """Fetch all research sessions ordered by created_at DESC."""
        try:
            response = (
                self.client.table(self.table_name)
                .select("*")
                .order("created_at", desc=True)
                .execute()
            )
            return [self._row_to_entity(row) for row in (response.data or [])]
        except Exception as exc:
            logger.exception("Supabase list_all failed: %s", str(exc))
            raise AppException(
                message=f"Database error listing sessions: {str(exc)}",
                error_code="DATABASE_ERROR",
            ) from exc

    def update(self, entity: ResearchSession) -> ResearchSession:
        """Update an existing research session row in Supabase."""
        try:
            payload = self._entity_to_row(entity)
            response = (
                self.client.table(self.table_name)
                .update(payload)
                .eq("id", entity.id)
                .execute()
            )
            if not response.data:
                raise AppException(
                    message=f"Session row '{entity.id}' not found for update",
                    error_code="RESOURCE_NOT_FOUND",
                )
            return self._row_to_entity(response.data[0])
        except AppException:
            raise
        except Exception as exc:
            logger.exception("Supabase update failed: %s", str(exc))
            raise AppException(
                message=f"Database error updating session: {str(exc)}",
                error_code="DATABASE_ERROR",
            ) from exc

    def delete(self, id_val: str) -> bool:
        """Delete a research session row by UUID from Supabase."""
        try:
            response = (
                self.client.table(self.table_name)
                .delete()
                .eq("id", id_val)
                .execute()
            )
            return bool(response.data)
        except Exception as exc:
            logger.exception("Supabase delete failed: %s", str(exc))
            raise AppException(
                message=f"Database error deleting session: {str(exc)}",
                error_code="DATABASE_ERROR",
            ) from exc

    @staticmethod
    def _row_to_entity(row: dict[str, Any]) -> ResearchSession:
        """Convert Supabase DB row dict to ResearchSession entity."""
        created_at_str = str(row["created_at"])
        updated_at_str = str(row["updated_at"])

        created_at = datetime.fromisoformat(
            created_at_str.replace("Z", "+00:00")
        )
        updated_at = datetime.fromisoformat(
            updated_at_str.replace("Z", "+00:00")
        )

        return ResearchSession(
            id=str(row["id"]),
            title=str(row["title"]),
            query=str(row["query"]),
            status=SessionStatus(row["status"]),
            created_at=created_at,
            updated_at=updated_at,
            metadata=row.get("metadata") or {},
        )

    @staticmethod
    def _entity_to_row(entity: ResearchSession) -> dict[str, Any]:
        """Convert ResearchSession entity to Supabase DB row dict."""
        return {
            "id": entity.id,
            "title": entity.title,
            "query": entity.query,
            "status": entity.status.value,
            "metadata": entity.metadata,
            "created_at": entity.created_at.astimezone(timezone.utc).isoformat(),
            "updated_at": entity.updated_at.astimezone(timezone.utc).isoformat(),
        }
