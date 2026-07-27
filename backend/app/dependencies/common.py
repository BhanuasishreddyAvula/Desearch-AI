"""Common request-scoped dependency providers."""

from typing import Any
from fastapi import Request

from app.observability.context import (
    get_execution_time_ms,
    get_request_id,
    get_trace_id,
)


def get_request_id_dep(request: Request) -> str | None:
    """Dependency provider returning the correlated request ID."""
    req_id: str | None = getattr(request.state, "request_id", None)
    return req_id or get_request_id()


def get_trace_id_dep(request: Request) -> str | None:
    """Dependency provider returning the correlated trace ID."""
    trace_id: str | None = getattr(request.state, "trace_id", None)
    return trace_id or get_trace_id()


def get_execution_time_dep(request: Request) -> float:
    """Dependency provider returning request execution time in milliseconds."""
    exec_time: float = getattr(request.state, "execution_time_ms", 0.0)
    return exec_time or get_execution_time_ms()


def get_request_context_dep(
    request: Request,
) -> dict[str, Any]:
    """Dependency provider returning unified request context metadata."""
    return {
        "request_id": get_request_id_dep(request),
        "trace_id": get_trace_id_dep(request),
        "execution_time_ms": get_execution_time_dep(request),
        "path": request.url.path,
        "method": request.method,
    }
