"""Single configuration entry point aggregating all modular settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.enums import Environment, LLMProvider, LogLevel
from app.core.settings.app import AppSettings
from app.core.settings.llm import LLMSettings
from app.core.settings.observability import ObservabilitySettings
from app.core.settings.redis import RedisSettings
from app.core.settings.security import SecuritySettings
from app.core.settings.supabase import SupabaseSettings


class Settings(BaseSettings):
    """Master configuration class composed of domain settings modules,

    exposing a unified flat public API for application consumption.
    """

    app: AppSettings = Field(default_factory=AppSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    supabase: SupabaseSettings = Field(default_factory=SupabaseSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    observability: ObservabilitySettings = Field(default_factory=ObservabilitySettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --------------------------------------------------------------------------
    # Flat Public Configuration API (AppSettings)
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
    # Flat Public Configuration API (SecuritySettings)
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
    # Flat Public Configuration API (SupabaseSettings)
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
    # Flat Public Configuration API (LLMSettings)
    # --------------------------------------------------------------------------
    @property
    def LLM_PROVIDER(self) -> LLMProvider:
        return self.llm.LLM_PROVIDER

    @property
    def LLM_MODEL(self) -> str:
        return self.llm.LLM_MODEL

    @property
    def API_KEY(self) -> str:
        return self.llm.API_KEY

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
    # Flat Public Configuration API (RedisSettings)
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
    # Flat Public Configuration API (ObservabilitySettings)
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
