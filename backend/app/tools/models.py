"""Data models for Tool Registry."""

from dataclasses import dataclass, field
from typing import Any

from app.tools.enums import AgentType, ToolCategory


@dataclass
class ToolMetadata:
    """Metadata describing a tool's specifications and capabilities."""

    id: str
    name: str
    description: str
    category: ToolCategory
    supported_agents: list[AgentType] = field(default_factory=list)
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)
    version: str = "1.0.0"
    enabled: bool = True
