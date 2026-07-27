"""Metadata schemas for API responses."""

from pydantic import BaseModel, Field

from app.schemas.pagination import PaginationMetadata


class ResponseMetadata(BaseModel):
    """Standard metadata model attached to API responses."""

    execution_time_ms: float = Field(
        default=0.0, description="Request execution duration in milliseconds"
    )
    api_version: str = Field(default="0.1.0", description="API version identifier")
    environment: str = Field(default="development", description="Runtime environment")
    pagination: PaginationMetadata | None = Field(
        default=None, description="Pagination details if response is paginated"
    )
