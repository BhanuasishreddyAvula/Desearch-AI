"""Shared enumeration types for Desearch AI Backend."""

from enum import StrEnum


class Environment(StrEnum):
    """Application runtime environments."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(StrEnum):
    """Standard logging level names."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LLMProvider(StrEnum):
    """Supported LLM provider options."""

    OPENROUTER = "openrouter"
    GEMINI = "gemini"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    MOCK = "mock"
