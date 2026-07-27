"""Core module containing settings, constants, enums, exceptions, and logging."""

from app.core.config import settings
from app.core.constants import (
    API_V1_STR,
    DEFAULT_APP_NAME,
    DEFAULT_APP_VERSION,
    DEFAULT_SERVICE_NAME,
)
from app.core.enums import Environment, LLMProvider, LogLevel
from app.core.exceptions import (
    AppException,
    AuthenticationException,
    AuthorizationException,
    ConflictException,
    ExternalServiceException,
    RateLimitException,
    ResourceNotFoundException,
    ValidationException,
)
from app.core.logging import get_logger, setup_logging

__all__ = [
    "settings",
    "setup_logging",
    "get_logger",
    "Environment",
    "LogLevel",
    "LLMProvider",
    "API_V1_STR",
    "DEFAULT_APP_NAME",
    "DEFAULT_APP_VERSION",
    "DEFAULT_SERVICE_NAME",
    "AppException",
    "ValidationException",
    "AuthenticationException",
    "AuthorizationException",
    "ResourceNotFoundException",
    "ConflictException",
    "RateLimitException",
    "ExternalServiceException",
]
