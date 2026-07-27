"""Session domain enumerations."""

from enum import StrEnum


class SessionStatus(StrEnum):
    """Lifecycle state machine stages for a Research Session."""

    DRAFT = "draft"
    PLANNING = "planning"
    WAITING_APPROVAL = "waiting_approval"
    RESEARCHING = "researching"
    REVIEWING = "reviewing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"
