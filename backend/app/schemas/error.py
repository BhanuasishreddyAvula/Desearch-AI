"""Standardized API error response models."""

from typing import Any

from pydantic import BaseModel, Field

from app.schemas.base import BaseResponse


class ErrorDetails(BaseModel):
    """Structured error descriptor model."""

    error_code: str = Field(..., description="Unique machine-readable error code")
    error_type: str = Field(..., description="High-level category of error")
    details: Any | None = Field(
        default=None,
        description="Detailed diagnostic or field-level validation errors",
    )
    trace_id: str | None = Field(
        default=None,
        description="Trace or correlation identifier for debugging",
    )


class ErrorResponse(BaseResponse[ErrorDetails]):
    """Standardized API error envelope response model."""

    success: bool = Field(default=False, description="Always False for error responses")
    message: str = Field(default="An error occurred", description="Human-readable error message")
    data: ErrorDetails | None = Field(default=None, description="Error detail payload")
