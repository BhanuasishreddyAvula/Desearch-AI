"""Request context middleware generating unique request IDs."""

import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.observability.context import (
    clear_observability_context,
    generate_trace_id,
    set_request_id,
    set_trace_id,
)


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Middleware attaching unique request_id and trace_id to context and response headers."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Clear any residual context from previous execution threads
        clear_observability_context()

        # Generate unique UUID4 request ID and trace ID
        request_id = str(uuid.uuid4())
        trace_id = generate_trace_id()

        # Attach to request.state and contextvars
        request.state.request_id = request_id
        request.state.trace_id = trace_id

        set_request_id(request_id)
        set_trace_id(trace_id)

        try:
            # Process request downstream
            response: Response = await call_next(request)

            # Attach X-Request-ID and X-Trace-ID headers to outgoing response
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Trace-ID"] = trace_id
            return response
        finally:
            clear_observability_context()
