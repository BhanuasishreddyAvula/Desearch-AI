"""Exception definitions for Content Tool and Firecrawl Provider."""

from app.core.exceptions import (
    AuthenticationException,
    AuthorizationException,
    ExternalServiceException,
    RateLimitException,
    ResourceNotFoundException,
)


class ContentException(ExternalServiceException):
    """Base exception for content tool extraction failures."""

    def __init__(
        self,
        message: str = "Content extraction tool execution failed",
        details: dict | None = None,
    ) -> None:
        super().__init__(
            message=message, error_code="CONTENT_EXTRACTION_ERROR", details=details
        )


class ContentAuthenticationException(AuthenticationException):
    """Raised when Firecrawl API key authentication fails."""

    def __init__(
        self,
        message: str = "Firecrawl API authentication failed",
        details: dict | None = None,
    ) -> None:
        super().__init__(message=message, details=details)


class ContentAuthorizationException(AuthorizationException):
    """Raised when Firecrawl API request is unauthorized."""

    def __init__(
        self,
        message: str = "Firecrawl API request unauthorized",
        details: dict | None = None,
    ) -> None:
        super().__init__(message=message, details=details)


class ContentNotFoundException(ResourceNotFoundException):
    """Raised when Firecrawl target web page or endpoint is not found."""

    def __init__(
        self,
        message: str = "Firecrawl target page or resource not found",
        details: dict | None = None,
    ) -> None:
        super().__init__(message=message, details=details)


class ContentTimeoutException(ExternalServiceException):
    """Raised when Firecrawl HTTP request times out."""

    def __init__(
        self,
        message: str = "Firecrawl content extraction request timed out",
        details: dict | None = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code="CONTENT_TIMEOUT",
            details=details,
        )


class ContentRateLimitException(RateLimitException):
    """Raised when Firecrawl API rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Firecrawl API rate limit exceeded",
        details: dict | None = None,
    ) -> None:
        super().__init__(message=message, details=details)
