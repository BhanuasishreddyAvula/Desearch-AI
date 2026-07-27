"""Observability, logging, metrics, and tracing settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.enums import LogLevel


class ObservabilitySettings(BaseSettings):
    """Logging level, metrics, and tracing configuration settings."""

    LOG_LEVEL: LogLevel = LogLevel.INFO
    LOG_FORMAT: str = "json"
    ENABLE_METRICS: bool = False
    ENABLE_TRACING: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
