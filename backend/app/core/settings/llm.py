"""LLM Provider Configuration Model for OpenRouter integration."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.enums import LLMProvider


class LLMSettings(BaseSettings):
    """LLM provider configuration parameters."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    LLM_PROVIDER: LLMProvider = Field(
        default=LLMProvider.OPENROUTER,
        description="Active LLM provider name",
    )
    LLM_MODEL: str = Field(
        default="google/gemini-2.5-flash-lite",
        description="Active LLM model identifier on OpenRouter",
    )
    OPENROUTER_API_KEY: str | None = Field(
        default=None,
        description="OpenRouter API Key for authenticating LLM requests",
    )
    GROQ_API_KEY: str | None = Field(
        default=None,
        description="Groq Cloud API Key for authenticating primary ultra-fast LLM requests",
    )
    GROQ_BASE_URL: str = Field(
        default="https://api.groq.com/openai/v1",
        description="Base URL for Groq Cloud REST API",
    )
    GROQ_DEFAULT_MODEL: str = Field(
        default="llama-3.3-70b-versatile",
        description="Default high-speed LLM model identifier on Groq Cloud platform",
    )
    OPENROUTER_BASE_URL: str = Field(
        default="https://openrouter.ai/api/v1",
        description="Base URL for OpenRouter REST API",
    )
    NVIDIA_API_KEY: str | None = Field(
        default=None,
        description="NVIDIA NIM API Key for authenticating secondary LLM requests",
    )
    NVIDIA_BASE_URL: str = Field(
        default="https://integrate.api.nvidia.com/v1",
        description="Base URL for NVIDIA NIM REST API",
    )
    NVIDIA_DEFAULT_MODEL: str = Field(
        default="meta/llama-3.3-70b-instruct",
        description="Default high-performance LLM model identifier on NVIDIA NIM platform",
    )
    TEMPERATURE: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0,
        description="Sampling temperature for LLM generation",
    )
    MAX_TOKENS: int = Field(
        default=4096,
        gt=0,
        description="Maximum tokens allowed in generation response",
    )
    TIMEOUT_SECONDS: int = Field(
        default=60,
        gt=0,
        description="Request timeout in seconds for LLM API calls",
    )
    MAX_RETRIES: int = Field(
        default=3,
        ge=0,
        description="Maximum retry attempts on transient LLM errors",
    )
