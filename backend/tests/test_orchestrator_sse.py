"""Unit tests for Server-Sent Events (SSE) research progress streaming and terminal event deduplication."""

import json
from unittest.mock import MagicMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.router import api_router
from app.core.exceptions import AppException
from app.orchestrator.events import (
    EVENT_PROGRESS_MAP,
    ProgressEvent,
    ProgressEventType,
    ProgressStreamListener,
    create_progress_event,
)
from app.orchestrator.orchestrator import MultiAgentOrchestrator

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
client = TestClient(app)


def test_progress_event_model():
    """Verify ProgressEvent formatting into valid SSE payload."""
    event = create_progress_event(
        ProgressEventType.PLANNER_STARTED,
        "Planning",
        "Formulating plan...",
        "session-123",
        {"tasks": 3},
    )
    assert event.progress == 5
    assert event.session_id == "session-123"

    sse_text = event.format_sse()
    assert "event: planner.started\n" in sse_text
    assert "data: {" in sse_text

    data_line = [line for line in sse_text.splitlines() if line.startswith("data: ")][0]
    json_str = data_line.removeprefix("data: ").strip()
    data_dict = json.loads(json_str)

    assert data_dict["event_type"] == "planner.started"
    assert data_dict["stage"] == "Planning"
    assert data_dict["progress"] == 5
    assert data_dict["session_id"] == "session-123"


def test_event_progress_map_complete():
    """Verify all ProgressEventType enum values exist in EVENT_PROGRESS_MAP."""
    for ev_type in ProgressEventType:
        assert ev_type.value in EVENT_PROGRESS_MAP


def test_progress_stream_listener_deduplication():
    """Verify ProgressStreamListener enforces exactly ONE terminal event."""
    emitted: list[ProgressEvent] = []
    listener = ProgressStreamListener(lambda ev: emitted.append(ev))

    ev1 = create_progress_event(ProgressEventType.PLANNER_STARTED, "Planning", "Plan start", "s1")
    ev2 = create_progress_event(ProgressEventType.WORKFLOW_FAILED, "Failed", "Error 1", "s1")
    ev3 = create_progress_event(ProgressEventType.WORKFLOW_FAILED, "Failed", "Error 2", "s1")
    ev4 = create_progress_event(ProgressEventType.WORKFLOW_COMPLETED, "Completed", "Done", "s1")

    assert listener.emit(ev1) is True
    assert listener.emit(ev2) is True
    assert listener.terminal_emitted is True
    assert listener.emit(ev3) is False  # Duplicate terminal event rejected
    assert listener.emit(ev4) is False  # Second terminal event rejected

    assert len(emitted) == 2
    assert emitted[0].event_type == "planner.started"
    assert emitted[1].event_type == "workflow.failed"


def test_orchestrator_emits_ordered_events():
    """Verify MultiAgentOrchestrator emits progress events in correct logical sequence."""
    emitted_events: list[ProgressEvent] = []

    mock_planner = MagicMock()
    mock_planner.create_plan.return_value = MagicMock(
        tasks=[MagicMock(id="t1", title="Task 1", description="Desc 1", priority="high")]
    )

    mock_research = MagicMock()
    mock_research.execute_research.return_value = MagicMock(
        evidence_items=[], tools_executed=["web_search"], sources_consulted=["https://example.com"]
    )

    mock_writer = MagicMock()
    mock_writer.create_report.return_value = MagicMock(
        metadata=MagicMock(word_count=500, sections_count=2, evidence_cited_count=1, sources_count=1),
        sections=[],
        title="Report Title",
        executive_summary="Summary",
        full_markdown="# Report Title",
        sources_cited=["https://example.com"],
        session_id="s1",
    )

    mock_reviewer = MagicMock()
    mock_reviewer.evaluate_report.return_value = MagicMock(approved=True, overall_score=0.9)

    orchestrator = MultiAgentOrchestrator(
        planner_service=mock_planner,
        research_service=mock_research,
        writer_service=mock_writer,
        reviewer_service=mock_reviewer,
    )

    orchestrator.run_workflow(
        session_id="session-test-1",
        query="Query text",
        progress_listener=lambda ev: emitted_events.append(ev),
    )

    event_types = [e.event_type for e in emitted_events]

    assert ProgressEventType.WORKFLOW_STARTED.value in event_types
    assert ProgressEventType.PLANNER_STARTED.value in event_types
    assert ProgressEventType.PLANNER_COMPLETED.value in event_types
    assert ProgressEventType.RESEARCH_STARTED.value in event_types
    assert ProgressEventType.RESEARCH_COMPLETED.value in event_types
    assert ProgressEventType.WRITER_STARTED.value in event_types
    assert ProgressEventType.WRITER_COMPLETED.value in event_types
    assert ProgressEventType.REVIEWER_STARTED.value in event_types
    assert ProgressEventType.REVIEWER_COMPLETED.value in event_types

    # Ordering assertions
    assert event_types.index("planner.started") < event_types.index("planner.completed")
    assert event_types.index("research.started") < event_types.index("research.completed")
    assert event_types.index("writer.started") < event_types.index("writer.completed")
    assert event_types.index("reviewer.started") < event_types.index("reviewer.completed")


def test_sse_streaming_successful_workflow():
    """Verify POST /api/v1/orchestrator/stream contains exactly ONE workflow.completed and ZERO workflow.failed."""
    with patch("app.orchestrator.service.OrchestratorService.execute_session_workflow") as mock_exec:
        def fake_exec(session_id, query, progress_listener=None):
            if progress_listener:
                progress_listener(create_progress_event(ProgressEventType.WORKFLOW_STARTED, "Init", "Started", session_id))
                progress_listener(create_progress_event(ProgressEventType.WORKFLOW_COMPLETED, "Done", "Completed", session_id))
            return MagicMock()

        mock_exec.side_effect = fake_exec

        response = client.post(
            "/api/v1/orchestrator/stream",
            json={"session_id": "test-session-sse", "query": "Test SSE Query"},
        )

        assert response.status_code == 200
        assert "text/event-stream" in response.headers.get("content-type", "")
        content = response.text

        assert content.count("event: workflow.completed") == 1
        assert content.count("event: workflow.failed") == 0


def test_sse_streaming_failed_workflow_deduplication():
    """Verify POST /api/v1/orchestrator/stream produces exactly ONE workflow.failed event during exception."""
    with patch("app.orchestrator.service.OrchestratorService.execute_session_workflow") as mock_exec:
        def fake_failing_exec(session_id, query, progress_listener=None):
            if progress_listener:
                progress_listener(create_progress_event(ProgressEventType.WORKFLOW_STARTED, "Init", "Started", session_id))
                # Orchestrator emits workflow.failed before re-raising exception
                progress_listener(create_progress_event(ProgressEventType.WORKFLOW_FAILED, "Failed", "LLM Error", session_id))
            raise AppException(message="OpenRouter empty response error")

        mock_exec.side_effect = fake_failing_exec

        response = client.post(
            "/api/v1/orchestrator/stream",
            json={"session_id": "test-session-failed", "query": "Test Failed Query"},
        )

        assert response.status_code == 200
        content = response.text

        # Verify EXACTLY ONE workflow.failed event was emitted
        assert content.count("event: workflow.failed") == 1
        assert content.count("event: workflow.completed") == 0
