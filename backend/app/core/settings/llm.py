"""LLM provider integration configuration settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT_SECONDS
from app.core.enums import LLMProvider


class LLMSettings(BaseSettings):
    """LLM Provider inference configuration settings."""

    LLM_PROVIDER: LLMProvider = LLMProvider.GEMINI
    LLM_MODEL: str = "gemini-1.5-flash"
    API_KEY: str = "your_llm_api_key_placeholder"
    TEMPERATURE: float = 0.2
    MAX_TOKENS: int = 4096
    TIMEOUT_SECONDS: int = DEFAULT_TIMEOUT_SECONDS
    MAX_RETRIES: int = DEFAULT_MAX_RETRIES

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
