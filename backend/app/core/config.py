"""Master configuration settings exposing a flat public API."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.enums import Environment, LLMProvider, LogLevel
from app.core.settings import (
    AppSettings,
    LLMSettings,
    ObservabilitySettings,
    RedisSettings,
    SecuritySettings,
    SupabaseSettings,
)


class Settings(BaseSettings):
    """Master application settings class exposing a flat public API."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Modular Domain Sub-Settings
    app: AppSettings = Field(default_factory=AppSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    supabase: SupabaseSettings = Field(default_factory=SupabaseSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    observability: ObservabilitySettings = Field(
        default_factory=ObservabilitySettings
    )

    # --------------------------------------------------------------------------
    # Flat Public Accessors — Application Settings
    # --------------------------------------------------------------------------
    @property
    def APP_NAME(self) -> str:
        return self.app.APP_NAME

    @property
    def APP_VERSION(self) -> str:
        return self.app.APP_VERSION

    @property
    def ENVIRONMENT(self) -> Environment:
        return self.app.ENVIRONMENT

    @property
    def DEBUG(self) -> bool:
        return self.app.DEBUG

    @property
    def HOST(self) -> str:
        return self.app.HOST

    @property
    def PORT(self) -> int:
        return self.app.PORT

    @property
    def API_V1_STR(self) -> str:
        return self.app.API_V1_STR

    # --------------------------------------------------------------------------
    # Flat Public Accessors — Security Settings
    # --------------------------------------------------------------------------
    @property
    def SECRET_KEY(self) -> str:
        return self.security.SECRET_KEY

    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self) -> int:
        return self.security.ACCESS_TOKEN_EXPIRE_MINUTES

    @property
    def CORS_ORIGINS(self) -> list[str]:
        return self.security.CORS_ORIGINS

    @property
    def API_KEY_SECRET(self) -> str:
        return self.security.API_KEY_SECRET

    # --------------------------------------------------------------------------
    # Flat Public Accessors — Supabase Settings
    # --------------------------------------------------------------------------
    @property
    def SUPABASE_URL(self) -> str:
        return self.supabase.SUPABASE_URL

    @property
    def SUPABASE_ANON_KEY(self) -> str:
        return self.supabase.SUPABASE_ANON_KEY

    @property
    def SUPABASE_SERVICE_ROLE_KEY(self) -> str:
        return self.supabase.SUPABASE_SERVICE_ROLE_KEY

    @property
    def DATABASE_URL(self) -> str:
        return self.supabase.DATABASE_URL

    # --------------------------------------------------------------------------
    # Flat Public Accessors — LLM Settings
    # --------------------------------------------------------------------------
    @property
    def LLM_PROVIDER(self) -> LLMProvider:
        return self.llm.LLM_PROVIDER

    @property
    def LLM_MODEL(self) -> str:
        return self.llm.LLM_MODEL

    @property
    def OPENROUTER_API_KEY(self) -> str | None:
        return self.llm.OPENROUTER_API_KEY

    @property
    def OPENROUTER_BASE_URL(self) -> str:
        return self.llm.OPENROUTER_BASE_URL

    @property
    def TEMPERATURE(self) -> float:
        return self.llm.TEMPERATURE

    @property
    def MAX_TOKENS(self) -> int:
        return self.llm.MAX_TOKENS

    @property
    def TIMEOUT_SECONDS(self) -> int:
        return self.llm.TIMEOUT_SECONDS

    @property
    def MAX_RETRIES(self) -> int:
        return self.llm.MAX_RETRIES

    # --------------------------------------------------------------------------
    # Flat Public Accessors — Redis Settings
    # --------------------------------------------------------------------------
    @property
    def REDIS_URL(self) -> str:
        return self.redis.REDIS_URL

    @property
    def CACHE_TTL(self) -> int:
        return self.redis.CACHE_TTL

    @property
    def RATE_LIMIT_WINDOW(self) -> int:
        return self.redis.RATE_LIMIT_WINDOW

    # --------------------------------------------------------------------------
    # Flat Public Accessors — Observability Settings
    # --------------------------------------------------------------------------
    @property
    def LOG_LEVEL(self) -> LogLevel:
        return self.observability.LOG_LEVEL

    @property
    def LOG_FORMAT(self) -> str:
        return self.observability.LOG_FORMAT

    @property
    def ENABLE_METRICS(self) -> bool:
        return self.observability.ENABLE_METRICS

    @property
    def ENABLE_TRACING(self) -> bool:
        return self.observability.ENABLE_TRACING


settings = Settings()
