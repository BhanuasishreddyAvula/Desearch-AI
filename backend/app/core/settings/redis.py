"""Redis and cache configuration settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import (
    DEFAULT_CACHE_TTL_SECONDS,
    DEFAULT_RATE_LIMIT_WINDOW_SECONDS,
)


class RedisSettings(BaseSettings):
    """Redis connections, caching TTL, and rate limiting settings."""

    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = DEFAULT_CACHE_TTL_SECONDS
    RATE_LIMIT_WINDOW: int = DEFAULT_RATE_LIMIT_WINDOW_SECONDS

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
