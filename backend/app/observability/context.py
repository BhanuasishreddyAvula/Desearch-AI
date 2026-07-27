"""Context management using contextvars for request and trace correlation."""

import uuid
from contextvars import ContextVar

# Context Variables
_request_id_ctx: ContextVar[str | None] = ContextVar("request_id", default=None)
_trace_id_ctx: ContextVar[str | None] = ContextVar("trace_id", default=None)
_execution_time_ctx: ContextVar[float] = ContextVar("execution_time", default=0.0)


def generate_trace_id() -> str:
    """Generate a unique 32-character hex trace ID."""
    return uuid.uuid4().hex


def get_request_id() -> str | None:
    """Retrieve the current request ID from context."""
    return _request_id_ctx.get()


def set_request_id(request_id: str) -> None:
    """Set the current request ID in context."""
    _request_id_ctx.set(request_id)


def get_trace_id() -> str | None:
    """Retrieve the current trace ID from context."""
    return _trace_id_ctx.get()


def set_trace_id(trace_id: str) -> None:
    """Set the current trace ID in context."""
    _trace_id_ctx.set(trace_id)


def get_execution_time_ms() -> float:
    """Retrieve current execution time in milliseconds from context."""
    return _execution_time_ctx.get()


def set_execution_time_ms(duration_ms: float) -> None:
    """Set current execution time in milliseconds in context."""
    _execution_time_ctx.set(duration_ms)


def clear_observability_context() -> None:
    """Reset observability context variables."""
    _request_id_ctx.set(None)
    _trace_id_ctx.set(None)
    _execution_time_ctx.set(0.0)
