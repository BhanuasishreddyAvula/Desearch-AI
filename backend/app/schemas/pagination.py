"""Pagination schemas for API list endpoints."""

from pydantic import BaseModel, Field


class PaginationMetadata(BaseModel):
    """Pagination metadata model for paginated API responses."""

    page: int = Field(default=1, ge=1, description="Current page number (1-indexed)")
    page_size: int = Field(default=20, ge=1, description="Number of items per page")
    total_items: int = Field(default=0, ge=0, description="Total number of items available")
    total_pages: int = Field(default=0, ge=0, description="Total number of pages available")
    has_next: bool = Field(default=False, description="Flag indicating if a next page exists")
    has_previous: bool = Field(
        default=False, description="Flag indicating if a previous page exists"
    )
