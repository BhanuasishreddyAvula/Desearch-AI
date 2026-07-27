"""Research session domain model."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
import uuid

from app.sessions.enums import SessionStatus


@dataclass
class ResearchSession:
    """Internal domain model representing a research session entity."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    query: str = ""
    status: SessionStatus = SessionStatus.DRAFT
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)
