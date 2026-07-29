"""Unit tests for ReportExportService, Markdown & PDF formatters, and export endpoint."""

import pytest
from unittest.mock import MagicMock

from app.core.exceptions import ResourceNotFoundException, ValidationException
from app.core.repositories.session import AbstractSessionRepository
from app.export.exceptions import ReportNotExportableException
from app.export.formatters.base import BaseExportFormatter
from app.export.formatters.markdown import MarkdownExportFormatter
from app.export.formatters.pdf import PdfExportFormatter
from app.export.service import ReportExportService
from app.sessions.enums import SessionStatus
from app.sessions.models import ResearchSession


@pytest.fixture
def sample_report_data():
    """Fixture returning sample canonical report dictionary."""
    return {
        "session_id": "test-session-12345",
        "title": "Comprehensive Supabase vs Firebase AI Comparison",
        "executive_summary": "This report compares Supabase and Firebase for building AI applications.",
        "full_markdown": "# Comprehensive Supabase vs Firebase AI Comparison\n\n## Executive Summary\n\nThis report compares Supabase and Firebase for building AI applications.\n\n## Architecture\n\nSupabase uses PostgreSQL with pgvector.\n\n## Sources & Citations\n\n- https://supabase.com/docs/guides/ai\n- https://firebase.google.com/docs/genkit\n",
        "sections": [
            {
                "title": "Architecture",
                "content": "Supabase uses PostgreSQL with pgvector.",
                "level": 2,
            }
        ],
        "sources_cited": [
            "https://supabase.com/docs/guides/ai",
            "https://firebase.google.com/docs/genkit",
        ],
        "metadata": {
            "word_count": 450,
            "sections_count": 2,
            "evidence_cited_count": 5,
            "sources_count": 2,
        },
    }


def test_sanitize_filename_prevents_path_traversal():
    """Verify filename sanitizer strips path traversal characters and unsafe symbols."""
    filename = BaseExportFormatter.sanitize_filename(
        "../../etc/passwd Report!!", "test-id-12345", "pdf"
    )
    assert "/" not in filename
    assert ".." not in filename
    assert filename.endswith(".pdf")
    assert filename.startswith("desearch_")


def test_markdown_export_formatter(sample_report_data):
    """Verify MarkdownExportFormatter returns UTF-8 encoded markdown bytes with correct metadata."""
    formatter = MarkdownExportFormatter()
    res = formatter.format_report(sample_report_data, "test-session-12345")

    assert res.media_type == "text/markdown; charset=utf-8"
    assert res.filename.endswith(".md")
    content_str = res.content.decode("utf-8")
    assert "Comprehensive Supabase vs Firebase AI Comparison" in content_str
    assert "https://supabase.com/docs/guides/ai" in content_str
    assert "Executive Summary" in content_str


def test_pdf_export_formatter(sample_report_data):
    """Verify PdfExportFormatter generates valid PDF binary bytes."""
    formatter = PdfExportFormatter()
    res = formatter.format_report(sample_report_data, "test-session-12345")

    assert res.media_type == "application/pdf"
    assert res.filename.endswith(".pdf")
    assert len(res.content) > 100
    # PDF magic bytes signature check (%PDF-)
    assert res.content.startswith(b"%PDF-")


def test_export_service_markdown(sample_report_data):
    """Verify ReportExportService exports Markdown for completed session."""
    mock_repo = MagicMock(spec=AbstractSessionRepository)
    session = ResearchSession(
        id="s123",
        title="Test Session",
        status=SessionStatus.COMPLETED,
        metadata={"report_result": sample_report_data},
    )
    mock_repo.get_by_id.return_value = session

    service = ReportExportService(session_repository=mock_repo)
    res = service.export_report("s123", "markdown")

    assert res.media_type == "text/markdown; charset=utf-8"
    assert b"Supabase vs Firebase" in res.content


def test_export_service_pdf(sample_report_data):
    """Verify ReportExportService exports PDF for completed session."""
    mock_repo = MagicMock(spec=AbstractSessionRepository)
    session = ResearchSession(
        id="s123",
        title="Test Session",
        status=SessionStatus.COMPLETED,
        metadata={"report_result": sample_report_data},
    )
    mock_repo.get_by_id.return_value = session

    service = ReportExportService(session_repository=mock_repo)
    res = service.export_report("s123", "pdf")

    assert res.media_type == "application/pdf"
    assert res.content.startswith(b"%PDF-")


def test_export_service_missing_session():
    """Verify ResourceNotFoundException raised when session ID does not exist."""
    mock_repo = MagicMock(spec=AbstractSessionRepository)
    mock_repo.get_by_id.return_value = None

    service = ReportExportService(session_repository=mock_repo)
    with pytest.raises(ResourceNotFoundException):
        service.export_report("nonexistent", "pdf")


def test_export_service_uncompleted_session():
    """Verify ReportNotExportableException raised when session report is not completed."""
    mock_repo = MagicMock(spec=AbstractSessionRepository)
    session = ResearchSession(
        id="s123",
        title="Test Session",
        status=SessionStatus.DRAFT,
        metadata={},
    )
    mock_repo.get_by_id.return_value = session

    service = ReportExportService(session_repository=mock_repo)
    with pytest.raises(ReportNotExportableException):
        service.export_report("s123", "markdown")


def test_export_service_unsupported_format(sample_report_data):
    """Verify ValidationException raised for invalid format parameter."""
    mock_repo = MagicMock(spec=AbstractSessionRepository)
    session = ResearchSession(
        id="s123",
        title="Test Session",
        status=SessionStatus.COMPLETED,
        metadata={"report_result": sample_report_data},
    )
    mock_repo.get_by_id.return_value = session

    service = ReportExportService(session_repository=mock_repo)
    with pytest.raises(ValidationException) as exc_info:
        service.export_report("s123", "docx")
    assert "Unsupported export format" in str(exc_info.value)
