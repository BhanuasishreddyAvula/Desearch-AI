"""Tools configuration settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ToolsSettings(BaseSettings):
    """Configuration parameters for external Tool providers (Exa Search, Firecrawl) and Research Context Budgeting."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    EXA_API_KEY: str = Field(
        default="",
        description="Exa AI Search API key",
    )
    FIRECRAWL_API_KEY: str = Field(
        default="",
        description="Firecrawl Web Extraction API key",
    )
    EXA_BASE_URL: str = Field(
        default="https://api.exa.ai",
        description="Exa API base URL",
    )
    FIRECRAWL_BASE_URL: str = Field(
        default="https://api.firecrawl.dev",
        description="Firecrawl API base URL",
    )
    SEARCH_TIMEOUT: float = Field(
        default=30.0,
        description="Timeout for search API calls in seconds",
    )
    CONTENT_TIMEOUT: float = Field(
        default=30.0,
        description="Timeout for content extraction API calls in seconds",
    )
    RESEARCH_MAX_SOURCE_CHARS: int = Field(
        default=10000,
        description="Maximum character budget per extracted research source",
    )
    RESEARCH_MAX_TOTAL_CHARS: int = Field(
        default=40000,
        description="Maximum global character budget for total research context synthesis",
    )
