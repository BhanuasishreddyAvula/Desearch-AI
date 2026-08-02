"""Pydantic v2 schemas for Research Session API payloads."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field

from app.schemas.base import BaseResponse
from app.sessions.enums import SessionStatus


class CreateSessionRequest(BaseModel):
    """Payload schema for creating a new research session."""

    query: str = Field(
        ...,
        min_length=3,
        description="The primary research query or topic to investigate",
    )
    title: str | None = Field(
        default=None,
        description="Optional human-readable title for the research session",
    )
    metadata: dict[str, Any] | None = Field(
        default=None, description="Optional custom session metadata"
    )


class UpdateSessionRequest(BaseModel):
    """Payload schema for updating an existing research session."""

    title: str | None = Field(
        default=None, description="Updated session title"
    )
    status: SessionStatus | None = Field(
        default=None, description="Target session lifecycle state transition"
    )
    metadata: dict[str, Any] | None = Field(
        default=None, description="Metadata dictionary to merge/update"
    )


class SessionResponse(BaseModel):
    """API representation of a research session entity."""

    id: str = Field(..., description="Unique session UUID identifier")
    title: str = Field(..., description="Session title")
    query: str = Field(..., description="Original research query")
    status: SessionStatus = Field(..., description="Current lifecycle state")
    device_id: str = Field(default="", description="Owning device UUID")
    created_at: datetime = Field(..., description="Session creation timestamp")
    updated_at: datetime = Field(..., description="Last updated timestamp")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Session metadata"
    )


class SessionListResponse(BaseModel):
    """Paginated or listed collection of research sessions."""

    sessions: list[SessionResponse] = Field(
        default_factory=list, description="List of session objects"
    )
    total: int = Field(..., description="Total count of sessions")


# Type aliases for standardized API Envelope responses
CreateSessionEnvelope = BaseResponse[SessionResponse]
SessionEnvelope = BaseResponse[SessionResponse]
SessionListEnvelope = BaseResponse[SessionListResponse]
