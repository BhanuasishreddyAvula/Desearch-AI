"""Normalized data models for the LLM Platform Layer."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class LLMRequest:
    """Normalized input payload for LLM chat completion requests."""

    system_prompt: str
    user_prompt: str
    model: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    response_format_json: bool = True


@dataclass
class LLMResponse:
    """Normalized response envelope returned by LLMClient."""

    content: str
    model: str
    provider: str = "openrouter"
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_ms: float = 0.0
    raw_payload: dict[str, Any] = field(default_factory=dict)
