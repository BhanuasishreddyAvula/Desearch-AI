"""Progress event model definitions, SSE formatting utilities, and terminal event listeners."""

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
import json
import threading
from typing import Any


class ProgressEventType(str, Enum):
    """Stable event vocabulary for research workflow progress streaming."""

    WORKFLOW_STARTED = "workflow.started"

    PLANNER_STARTED = "planner.started"
    PLANNER_COMPLETED = "planner.completed"

    RESEARCH_STARTED = "research.started"
    RESEARCH_SEARCHING = "research.searching"
    RESEARCH_EXTRACTING = "research.extracting"
    RESEARCH_COMPLETED = "research.completed"

    WRITER_STARTED = "writer.started"
    WRITER_COMPLETED = "writer.completed"

    REVIEWER_STARTED = "reviewer.started"
    REVIEWER_COMPLETED = "reviewer.completed"

    REPORT_PERSISTED = "report.persisted"
    WORKFLOW_COMPLETED = "workflow.completed"
    WORKFLOW_FAILED = "workflow.failed"


# Centralized progress percentage mapping for UX progress bars
EVENT_PROGRESS_MAP: dict[str, int] = {
    ProgressEventType.WORKFLOW_STARTED.value: 0,
    ProgressEventType.PLANNER_STARTED.value: 5,
    ProgressEventType.PLANNER_COMPLETED.value: 15,
    ProgressEventType.RESEARCH_STARTED.value: 20,
    ProgressEventType.RESEARCH_SEARCHING.value: 25,
    ProgressEventType.RESEARCH_EXTRACTING.value: 40,
    ProgressEventType.RESEARCH_COMPLETED.value: 60,
    ProgressEventType.WRITER_STARTED.value: 65,
    ProgressEventType.WRITER_COMPLETED.value: 80,
    ProgressEventType.REVIEWER_STARTED.value: 85,
    ProgressEventType.REVIEWER_COMPLETED.value: 95,
    ProgressEventType.REPORT_PERSISTED.value: 98,
    ProgressEventType.WORKFLOW_COMPLETED.value: 100,
    ProgressEventType.WORKFLOW_FAILED.value: 100,
}


@dataclass
class ProgressEvent:
    """Typed domain progress event emitted during research workflow execution."""

    event_type: str
    stage: str
    message: str
    session_id: str
    progress: int = 0
    timestamp: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert ProgressEvent to dictionary representation."""
        return {
            "event_type": self.event_type,
            "stage": self.stage,
            "message": self.message,
            "session_id": self.session_id,
            "progress": self.progress,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }

    def format_sse(self) -> str:
        """Serialize ProgressEvent according to standard SSE text/event-stream syntax."""
        json_payload = json.dumps(self.to_dict())
        return f"event: {self.event_type}\ndata: {json_payload}\n\n"


def create_progress_event(
    event_type: str | ProgressEventType,
    stage: str,
    message: str,
    session_id: str,
    metadata: dict[str, Any] | None = None,
) -> ProgressEvent:
    """Helper factory constructing a ProgressEvent with automatic percentage mapping."""
    ev_type_str = (
        event_type.value if isinstance(event_type, ProgressEventType) else str(event_type)
    )
    progress_val = EVENT_PROGRESS_MAP.get(ev_type_str, 0)
    return ProgressEvent(
        event_type=ev_type_str,
        stage=stage,
        message=message,
        session_id=session_id,
        progress=progress_val,
        metadata=metadata or {},
    )


class ProgressStreamListener:
    """Thread-safe progress listener enforcing exactly ONE terminal event per execution stream."""

    def __init__(self, callback: Callable[[ProgressEvent], None]) -> None:
        self.callback = callback
        self._terminal_emitted = False
        self._lock = threading.Lock()

    def __call__(self, event: ProgressEvent) -> bool:
        """Allow instance to be called directly as a listener function (e.g. progress_listener(event))."""
        return self.emit(event)

    @property
    def terminal_emitted(self) -> bool:
        """Return True if a terminal event (workflow.completed or workflow.failed) was emitted."""
        with self._lock:
            return self._terminal_emitted

    def emit(self, event: ProgressEvent) -> bool:
        """Emit progress event if terminal limit has not been reached. Returns True if emitted."""
        with self._lock:
            if self._terminal_emitted:
                return False

            is_terminal = event.event_type in (
                ProgressEventType.WORKFLOW_COMPLETED.value,
                ProgressEventType.WORKFLOW_FAILED.value,
            )

            if is_terminal:
                self._terminal_emitted = True

            self.callback(event)
            return True
