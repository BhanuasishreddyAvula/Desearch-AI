"""Custom application exception hierarchy for Desearch AI."""

from typing import Any
from fastapi import status


class AppException(Exception):
    """Base exception class for all custom Desearch AI application errors."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code: str = "INTERNAL_SERVER_ERROR"
    error_type: str = "SYSTEM_ERROR"

    def __init__(
        self,
        message: str = "An internal server error occurred",
        details: Any | None = None,
        status_code: int | None = None,
        error_code: str | None = None,
        error_type: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.details = details
        if status_code is not None:
            self.status_code = status_code
        if error_code is not None:
            self.error_code = error_code
        if error_type is not None:
            self.error_type = error_type


class ConfigurationException(AppException):
    """Raised when required environment or system configuration is missing."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code: str = "CONFIGURATION_ERROR"
    error_type: str = "SYSTEM_ERROR"

    def __init__(
        self,
        message: str = (
            "System configuration is invalid or missing required credentials"
        ),
        details: Any | None = None,
        error_code: str | None = None,
    ) -> None:
        super().__init__(
            message=message, details=details, error_code=error_code
        )


class ValidationException(AppException):
    """Raised when request payload or parameters fail validation."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    error_code: str = "INVALID_INPUT"
    error_type: str = "VALIDATION_ERROR"

    def __init__(
        self,
        message: str = "Request parameters or payload failed validation",
        details: Any | None = None,
        error_code: str | None = None,
    ) -> None:
        super().__init__(
            message=message, details=details, error_code=error_code
        )


class AuthenticationException(AppException):
    """Raised when authentication credentials are invalid or missing."""

    status_code: int = status.HTTP_401_UNAUTHORIZED
    error_code: str = "UNAUTHENTICATED"
    error_type: str = "AUTHENTICATION_ERROR"

    def __init__(
        self,
        message: str = (
            "Authentication credentials were not provided or are invalid"
        ),
        details: Any | None = None,
        error_code: str | None = None,
    ) -> None:
        super().__init__(
            message=message, details=details, error_code=error_code
        )


class AuthorizationException(AppException):
    """Raised when user lacks permission to access the requested resource."""

    status_code: int = status.HTTP_403_FORBIDDEN
    error_code: str = "PERMISSION_DENIED"
    error_type: str = "AUTHORIZATION_ERROR"

    def __init__(
        self,
        message: str = "You do not have permission to perform this action",
        details: Any | None = None,
        error_code: str | None = None,
    ) -> None:
        super().__init__(
            message=message, details=details, error_code=error_code
        )


class ResourceNotFoundException(AppException):
    """Raised when a requested resource or entity cannot be found."""

    status_code: int = status.HTTP_404_NOT_FOUND
    error_code: str = "RESOURCE_NOT_FOUND"
    error_type: str = "NOT_FOUND_ERROR"

    def __init__(
        self,
        message: str = "The requested resource was not found",
        details: Any | None = None,
        error_code: str | None = None,
    ) -> None:
        super().__init__(
            message=message, details=details, error_code=error_code
        )


class ConflictException(AppException):
    """Raised when an operation conflicts with the resource state."""

    status_code: int = status.HTTP_409_CONFLICT
    error_code: str = "RESOURCE_CONFLICT"
    error_type: str = "CONFLICT_ERROR"

    def __init__(
        self,
        message: str = "Operation conflicts with existing resource state",
        details: Any | None = None,
        error_code: str | None = None,
    ) -> None:
        super().__init__(
            message=message, details=details, error_code=error_code
        )


class RateLimitException(AppException):
    """Raised when request quota or rate limits are exceeded."""

    status_code: int = status.HTTP_429_TOO_MANY_REQUESTS
    error_code: str = "RATE_LIMIT_EXCEEDED"
    error_type: str = "RATE_LIMIT_ERROR"

    def __init__(
        self,
        message: str = "Rate limit exceeded. Please try again later",
        details: Any | None = None,
        error_code: str | None = None,
    ) -> None:
        super().__init__(
            message=message, details=details, error_code=error_code
        )


class ExternalServiceException(AppException):
    """Raised when an external API or service integration fails."""

    status_code: int = status.HTTP_502_BAD_GATEWAY
    error_code: str = "EXTERNAL_SERVICE_ERROR"
    error_type: str = "INTEGRATION_ERROR"

    def __init__(
        self,
        message: str = "An external service or integration request failed",
        details: Any | None = None,
        error_code: str | None = None,
    ) -> None:
        super().__init__(
            message=message, details=details, error_code=error_code
        )
