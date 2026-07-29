"""Pydantic v2 serialization schemas for Tool Registry API endpoints."""

from typing import Any
from pydantic import BaseModel, Field

from app.schemas.base import BaseResponse


class ToolResponseSchema(BaseModel):
    """Pydantic representation of tool metadata for API responses."""

    id: str = Field(..., description="Unique tool identifier")
    name: str = Field(..., description="Human-readable tool display name")
    description: str = Field(
        ..., description="Detailed description of tool capability"
    )
    category: str = Field(..., description="Tool category string")
    version: str = Field(..., description="Semantic version string")
    enabled: bool = Field(..., description="Flag indicating if tool is enabled")
    supported_agents: list[str] = Field(
        default_factory=list, description="List of supported AI agent roles"
    )
    input_schema: dict[str, Any] = Field(
        default_factory=dict, description="JSON Schema for tool input arguments"
    )
    output_schema: dict[str, Any] = Field(
        default_factory=dict, description="JSON Schema for tool output return value"
    )


ToolEnvelope = BaseResponse[ToolResponseSchema]
ToolListEnvelope = BaseResponse[list[ToolResponseSchema]]
