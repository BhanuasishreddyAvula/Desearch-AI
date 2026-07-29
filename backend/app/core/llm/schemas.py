"""Pydantic v2 schemas for OpenRouter API request and response envelopes."""

from typing import Any
from pydantic import BaseModel, Field


class OpenRouterMessage(BaseModel):
    """Chat completion message object."""

    role: str = Field(..., description="Message role (system, user, assistant)")
    content: str = Field(..., description="Message content string")


class OpenRouterResponseFormat(BaseModel):
    """Response format specification."""

    type: str = Field(default="json_object", description="Response type format")


class OpenRouterChatRequest(BaseModel):
    """OpenRouter /chat/completions request body payload."""

    model: str = Field(..., description="Target model identifier on OpenRouter")
    messages: list[OpenRouterMessage] = Field(..., description="Chat completion messages")
    temperature: float = Field(default=0.2, description="Sampling temperature")
    max_tokens: int = Field(default=4096, description="Max completion tokens")
    response_format: OpenRouterResponseFormat | None = Field(
        default=None, description="Optional structured JSON format specification"
    )
