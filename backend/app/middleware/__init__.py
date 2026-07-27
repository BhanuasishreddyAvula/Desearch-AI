"""Middleware package re-exporting custom application middleware."""

from fastapi import FastAPI

from app.middleware.request_context import RequestContextMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware
from app.middleware.request_timing import RequestTimingMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware


def register_middleware(app: FastAPI) -> None:
    """Register application middleware in execution sequence order:

    Request Ingress Order:
      RequestContextMiddleware -> RequestTimingMiddleware -> RequestLoggingMiddleware -> SecurityHeadersMiddleware
    """
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RequestTimingMiddleware)
    app.add_middleware(RequestContextMiddleware)


__all__ = [
    "RequestContextMiddleware",
    "RequestTimingMiddleware",
    "RequestLoggingMiddleware",
    "SecurityHeadersMiddleware",
    "register_middleware",
]
