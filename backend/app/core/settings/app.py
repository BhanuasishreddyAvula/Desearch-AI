"""Application settings model."""

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import (
    API_V1_STR,
    DEFAULT_APP_NAME,
    DEFAULT_APP_VERSION,
    DEFAULT_HOST,
    DEFAULT_PORT,
)
from app.core.enums import Environment


class AppSettings(BaseSettings):
    """General application settings."""

    APP_NAME: str = DEFAULT_APP_NAME
    APP_VERSION: str = DEFAULT_APP_VERSION
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    DEBUG: bool = True
    HOST: str = DEFAULT_HOST
    PORT: int = DEFAULT_PORT
    API_V1_STR: str = API_V1_STR

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
