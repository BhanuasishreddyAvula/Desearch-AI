"""Request logging middleware outputting single-line HTTP access logs."""

from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.observability.logger import get_app_logger
from app.observability.metrics import metrics

logger = get_app_logger("middleware.request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware logging HTTP requests with method, path, status, timing, request_id, and IP."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        response: Response = await call_next(request)

        # Extract context fields from request.state
        request_id = getattr(request.state, "request_id", "N/A")
        execution_time_ms = getattr(request.state, "execution_time_ms", 0.0)

        # Determine client IP address
        client_ip = request.headers.get("x-forwarded-for") or (
            request.client.host if request.client else "unknown"
        )

        # Record metric
        metrics.increment_counter(
            "http_requests_total",
            labels={
                "method": request.method,
                "status": str(response.status_code),
            },
        )
        metrics.record_duration(
            "http_request_duration_ms",
            execution_time_ms,
            labels={"path": request.url.path},
        )

        # Emit log
        logger.info(
            "%s %s | %d | %.2fms | req_id: %s | ip: %s",
            request.method,
            request.url.path,
            response.status_code,
            execution_time_ms,
            request_id,
            client_ip,
        )

        return response
