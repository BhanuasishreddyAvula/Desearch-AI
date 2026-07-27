"""In-memory tracing engine supporting nested spans and trace IDs."""

import time
import uuid
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from app.observability.context import (
    generate_trace_id,
    get_trace_id,
    set_trace_id,
)


class Span:
    """Represents a single execution span within a trace."""

    def __init__(
        self,
        name: str,
        trace_id: str,
        parent_span_id: str | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> None:
        self.span_id: str = uuid.uuid4().hex[:16]
        self.trace_id: str = trace_id
        self.parent_span_id: str | None = parent_span_id
        self.name: str = name
        self.start_time: float = time.perf_counter()
        self.end_time: float | None = None
        self.duration_ms: float | None = None
        self.attributes: dict[str, Any] = attributes or {}

    def finish(self) -> None:
        """Mark span execution complete and calculate duration."""
        self.end_time = time.perf_counter()
        self.duration_ms = round((self.end_time - self.start_time) * 1000, 2)

    def to_dict(self) -> dict[str, Any]:
        """Convert span record into a dictionary."""
        return {
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "trace_id": self.trace_id,
            "name": self.name,
            "duration_ms": self.duration_ms,
            "attributes": self.attributes,
        }


class Tracer:
    """Tracer manager handling nested span stacks and trace collections."""

    def __init__(self) -> None:
        self._traces: dict[str, list[Span]] = {}
        self._span_stack: dict[str, list[Span]] = {}

    @contextmanager
    def trace_span(
        self, name: str, attributes: dict[str, Any] | None = None
    ) -> Generator[Span, None, None]:
        """Context manager to start and finish a nested span."""
        current_trace_id = get_trace_id()
        if not current_trace_id:
            current_trace_id = generate_trace_id()
            set_trace_id(current_trace_id)

        if current_trace_id not in self._span_stack:
            self._span_stack[current_trace_id] = []
            self._traces[current_trace_id] = []

        parent_span = (
            self._span_stack[current_trace_id][-1] if self._span_stack[current_trace_id] else None
        )
        parent_span_id = parent_span.span_id if parent_span else None

        span = Span(
            name=name,
            trace_id=current_trace_id,
            parent_span_id=parent_span_id,
            attributes=attributes,
        )

        self._span_stack[current_trace_id].append(span)
        self._traces[current_trace_id].append(span)

        try:
            yield span
        finally:
            span.finish()
            self._span_stack[current_trace_id].pop()

    def get_trace(self, trace_id: str) -> list[dict[str, Any]]:
        """Retrieve all spans associated with a trace_id."""
        spans = self._traces.get(trace_id, [])
        return [span.to_dict() for span in spans]


tracer = Tracer()
