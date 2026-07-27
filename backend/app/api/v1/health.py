"""Health check endpoint handler for API v1."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.config import Settings
from app.dependencies import (
    get_execution_time_dep,
    get_request_id_dep,
    get_settings_dep,
)
from app.schemas.health import HealthData, HealthResponse
from app.schemas.metadata import ResponseMetadata

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Returns service health status wrapped in standardized BaseResponse envelope.",
)
async def health_check(
    settings: Annotated[Settings, Depends(get_settings_dep)],
    request_id: Annotated[str | None, Depends(get_request_id_dep)],
    execution_time_ms: Annotated[float, Depends(get_execution_time_dep)],
) -> HealthResponse:
    """Health check endpoint verifying backend service availability using Dependency Injection."""
    return HealthResponse(
        success=True,
        message="Health check successful.",
        request_id=request_id,
        data=HealthData(
            status="healthy",
            service="desearch-ai-backend",
            version=settings.APP_VERSION,
        ),
        metadata=ResponseMetadata(
            execution_time_ms=execution_time_ms,
            api_version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT.value,
        ),
    )
