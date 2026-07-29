"""Exception definitions for Search Tool and Exa Provider."""

from app.core.exceptions import (
    AuthenticationException,
    AuthorizationException,
    ExternalServiceException,
    RateLimitException,
    ResourceNotFoundException,
)


class SearchException(ExternalServiceException):
    """Base exception for search tool execution failures."""

    def __init__(
        self,
        message: str = "Search tool execution failed",
        details: dict | None = None,
    ) -> None:
        super().__init__(
            message=message, error_code="SEARCH_ERROR", details=details
        )


class SearchAuthenticationException(AuthenticationException):
    """Raised when Exa API key authentication fails."""

    def __init__(
        self,
        message: str = "Exa API authentication failed",
        details: dict | None = None,
    ) -> None:
        super().__init__(message=message, details=details)


class SearchAuthorizationException(AuthorizationException):
    """Raised when Exa API request is unauthorized."""

    def __init__(
        self,
        message: str = "Exa API request unauthorized",
        details: dict | None = None,
    ) -> None:
        super().__init__(message=message, details=details)


class SearchNotFoundException(ResourceNotFoundException):
    """Raised when Exa search endpoint or resource is not found."""

    def __init__(
        self,
        message: str = "Exa Search resource not found",
        details: dict | None = None,
    ) -> None:
        super().__init__(message=message, details=details)


class SearchTimeoutException(ExternalServiceException):
    """Raised when Exa Search HTTP request times out."""

    def __init__(
        self,
        message: str = "Exa Search request timed out",
        details: dict | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code="SEARCH_TIMEOUT",
            details=details,
        )


class SearchRateLimitException(RateLimitException):
    """Raised when Exa Search API rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Exa Search API rate limit exceeded",
        details: dict | None = None,
    ) -> None:
        super().__init__(message=message, details=details)
