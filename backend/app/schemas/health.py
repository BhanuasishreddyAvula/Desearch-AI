"""Health check response models."""

from pydantic import BaseModel, Field

from app.schemas.base import BaseResponse


class HealthData(BaseModel):
    """Health check status data payload."""

    status: str = Field(default="healthy", description="Current health status")
    service: str = Field(default="desearch-ai-backend", description="Service identifier")
    version: str = Field(default="0.1.0", description="Application version")


class HealthResponse(BaseResponse[HealthData]):
    """Standardized health check API response model."""

    message: str = Field(
        default="Health check successful.",
        description="Response message",
    )
    data: HealthData = Field(default_factory=HealthData, description="Health data payload")
