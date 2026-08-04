"""Middleware package re-exporting custom application middleware."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.middleware.request_context import RequestContextMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware
from app.middleware.request_timing import RequestTimingMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware


def register_middleware(app: FastAPI) -> None:
    """Register application middleware in execution sequence order:

    Request Ingress Order:
      CORSMiddleware -> RequestContextMiddleware -> RequestTimingMiddleware -> RequestLoggingMiddleware -> SecurityHeadersMiddleware
    """
    raw_origins = settings.CORS_ORIGINS or ["*"]
    origins = [o.rstrip("/") for o in raw_origins]
    allow_credentials = "*" not in origins

    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RequestTimingMiddleware)
    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )


__all__ = [
    "RequestContextMiddleware",
    "RequestTimingMiddleware",
    "RequestLoggingMiddleware",
    "SecurityHeadersMiddleware",
    "register_middleware",
]
