"""Business logic service for Research Session management and state transitions."""

from datetime import UTC, datetime

from app.core.exceptions import ResourceNotFoundException, ValidationException
from app.core.repositories.session import AbstractSessionRepository
from app.sessions.enums import SessionStatus
from app.sessions.models import ResearchSession
from app.sessions.schemas import CreateSessionRequest, UpdateSessionRequest

# State Machine Transition Rules Matrix
ALLOWED_TRANSITIONS: dict[SessionStatus, set[SessionStatus]] = {
    SessionStatus.DRAFT: {SessionStatus.PLANNING, SessionStatus.CANCELLED},
    SessionStatus.PLANNING: {
        SessionStatus.WAITING_APPROVAL,
        SessionStatus.FAILED,
        SessionStatus.CANCELLED,
    },
    SessionStatus.WAITING_APPROVAL: {
        SessionStatus.RESEARCHING,
        SessionStatus.CANCELLED,
    },
    SessionStatus.RESEARCHING: {
        SessionStatus.REVIEWING,
        SessionStatus.FAILED,
        SessionStatus.CANCELLED,
    },
    SessionStatus.REVIEWING: {
        SessionStatus.COMPLETED,
        SessionStatus.RESEARCHING,
        SessionStatus.FAILED,
        SessionStatus.CANCELLED,
    },
    SessionStatus.COMPLETED: {SessionStatus.ARCHIVED},
    SessionStatus.FAILED: {SessionStatus.ARCHIVED},
    SessionStatus.CANCELLED: {SessionStatus.ARCHIVED},
    SessionStatus.ARCHIVED: set(),  # Terminal state
}


class SessionService:
    """Service encapsulating research session business logic and validation rules."""

    def __init__(self, repository: AbstractSessionRepository) -> None:
        self.repository = repository

    def create_session(
        self, data: CreateSessionRequest, device_id: str = ""
    ) -> ResearchSession:
        """Create and store a new research session owned by the given device."""
        title = data.title or self._derive_title(data.query)
        session = ResearchSession(
            title=title,
            query=data.query,
            status=SessionStatus.DRAFT,
            device_id=device_id,
            metadata=data.metadata or {},
        )
        return self.repository.create(session)

    def get_session(
        self, session_id: str, device_id: str = ""
    ) -> ResearchSession:
        """Retrieve a session by ID, enforcing device ownership when device_id is provided."""
        session = self.repository.get_by_id(session_id)
        if not session:
            raise ResourceNotFoundException(
                message=f"Research session '{session_id}' was not found"
            )
        # Enforce device ownership — allow access if session belongs to device or is legacy nil UUID
        nil_uuid = "00000000-0000-0000-0000-000000000000"
        if (
            device_id
            and session.device_id
            and session.device_id != nil_uuid
            and session.device_id != device_id
        ):
            raise ResourceNotFoundException(
                message=f"Research session '{session_id}' was not found"
            )
        return session


    def list_sessions(
        self, device_id: str = ""
    ) -> tuple[list[ResearchSession], int]:
        """Retrieve sessions for the given device with total count."""
        if device_id:
            sessions = self.repository.list_by_device(device_id)
        else:
            sessions = self.repository.list_all()
        return sessions, len(sessions)

    def update_session(
        self,
        session_id: str,
        data: UpdateSessionRequest,
        device_id: str = "",
    ) -> ResearchSession:
        """Update session fields, validating state machine transitions and device ownership."""
        session = self.get_session(session_id, device_id)

        if data.status is not None and data.status != session.status:
            self.validate_state_transition(session.status, data.status)
            session.status = data.status

        if data.title is not None:
            session.title = data.title

        if data.metadata is not None:
            session.metadata.update(data.metadata)

        session.updated_at = datetime.now(UTC)
        return self.repository.update(session)

    def delete_session(self, session_id: str, device_id: str = "") -> None:
        """Delete a research session by ID after verifying existence and device ownership."""
        session = self.get_session(session_id, device_id)
        self.repository.delete(session.id)

    def validate_state_transition(
        self, current_status: SessionStatus, target_status: SessionStatus
    ) -> None:
        """Validate if a transition from current_status to target_status is permitted."""
        allowed = ALLOWED_TRANSITIONS.get(current_status, set())
        if target_status not in allowed:
            raise ValidationException(
                message=(
                    f"Invalid session status transition from '{current_status.value}' "
                    f"to '{target_status.value}'"
                ),
                details={
                    "current_status": current_status.value,
                    "target_status": target_status.value,
                    "allowed_transitions": [s.value for s in allowed],
                },
            )

    @staticmethod
    def _derive_title(query: str) -> str:
        """Derive default title from first 50 characters of query."""
        cleaned = query.strip()
        if len(cleaned) <= 50:
            return cleaned
        return cleaned[:47] + "..."
