"""Request timing middleware measuring execution duration."""

import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.observability.context import set_execution_time_ms


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """Middleware measuring request execution time using time.perf_counter()."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.perf_counter()

        response: Response = await call_next(request)

        # Calculate duration in milliseconds
        execution_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        request.state.execution_time_ms = execution_time_ms
        set_execution_time_ms(execution_time_ms)

        return response
