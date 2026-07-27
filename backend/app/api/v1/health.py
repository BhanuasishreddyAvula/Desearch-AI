"""Health check endpoint handler for API v1."""

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(tags=["Health"])


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str = Field(default="healthy", description="Current health status")
    service: str = Field(
        default="desearch-ai-backend", description="Service identifier"
    )
    version: str = Field(default="0.1.0", description="Application version")


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Health Check",
    description="Returns service health status, service identifier, and version.",
)
async def health_check() -> HealthCheckResponse:
    """Health check endpoint to verify backend service availability."""
    return HealthCheckResponse(
        status="healthy",
        service="desearch-ai-backend",
        version="0.1.0",
    )
