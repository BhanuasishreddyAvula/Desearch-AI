"""Pydantic schemas for Conversation Messages API."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field

from app.schemas.base import BaseResponse


class ConversationMessageResponse(BaseModel):
    """API representation of a single conversation message."""

    id: str = Field(..., description="Unique message UUID")
    session_id: str = Field(..., description="Parent session UUID")
    role: str = Field(..., description="Message role: user | assistant")
    content: str = Field(..., description="Message text content")
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata (sources, markdown, title for assistant messages)",
    )
    created_at: datetime = Field(..., description="Message creation timestamp")


class ConversationMessagesListResponse(BaseModel):
    """Paginated conversation messages list."""

    messages: list[ConversationMessageResponse] = Field(
        default_factory=list, description="Ordered list of conversation messages"
    )
    total: int = Field(..., description="Total message count for this session")


# Envelope type aliases
ConversationMessagesEnvelope = BaseResponse[ConversationMessagesListResponse]
