"""Centralized logger wrapper decorating stdlib logging with observability context."""

from typing import Any

from app.core.logging import get_logger as get_stdlib_logger
from app.observability.context import get_request_id, get_trace_id


class AppLogger:
    """Centralized logger wrapper around standard Python Logger.

    Injects context fields (request_id, trace_id) automatically into log entries.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self._logger = get_stdlib_logger(name)

    def _format_message(self, msg: str) -> str:
        req_id = get_request_id()
        trace_id = get_trace_id()

        prefix_parts = []
        if req_id:
            prefix_parts.append(f"req_id={req_id}")
        if trace_id:
            prefix_parts.append(f"trace_id={trace_id}")

        if prefix_parts:
            prefix = " [" + " ".join(prefix_parts) + "]"
            return f"{msg}{prefix}"
        return msg

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._logger.info(self._format_message(msg), *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._logger.warning(self._format_message(msg), *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._logger.error(self._format_message(msg), *args, **kwargs)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._logger.debug(self._format_message(msg), *args, **kwargs)

    def exception(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._logger.exception(self._format_message(msg), *args, **kwargs)

    def event(
        self,
        event_name: str,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Log a structured domain event."""
        details_str = f" | details={details}" if details else ""
        formatted_event = f"EVENT:{event_name} | {message}{details_str}"
        self.info(formatted_event)


def get_app_logger(name: str) -> AppLogger:
    """Factory function returning a named AppLogger instance."""
    return AppLogger(name)
