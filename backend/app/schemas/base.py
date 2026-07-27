"""Base generic API response models using Pydantic v2."""

from datetime import UTC, datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from app.schemas.metadata import ResponseMetadata

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    """Standardized API envelope model for all endpoint responses."""

    success: bool = Field(default=True, description="Indicates if request succeeded")
    message: str = Field(default="Success", description="Human-readable response message")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="ISO 8601 UTC timestamp of response generation",
    )
    request_id: str | None = Field(
        default=None, description="Unique correlation or request identifier"
    )
    data: T | None = Field(default=None, description="Payload data returned by endpoint")
    metadata: ResponseMetadata | None = Field(
        default=None, description="Additional execution metadata"
    )
