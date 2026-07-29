"""Unit tests for ResearchContextBuilder, URL deduplication, and context budgeting."""

import pytest
from unittest.mock import MagicMock

from app.agents.research.context_builder import (
    ResearchContextBuilder,
    normalize_url,
    safe_truncate_text,
)
from app.agents.research.research import ResearchAgent
from app.core.llm.client import LLMClient
from app.tools.registry import ToolRegistry


def test_normalize_url():
    """Verify URL normalization strips fragments and trailing slashes."""
    url1 = "https://Example.com/docs/api/#section1"
    url2 = "https://example.com/docs/api/"
    assert normalize_url(url1) == "https://example.com/docs/api"
    assert normalize_url(url2) == "https://example.com/docs/api"


def test_safe_truncate_text_unicode_safety():
    """Verify safe_truncate_text preserves Unicode characters and truncates cleanly."""
    unicode_text = "Desearch AI Platform 🚀 — Bounded Context Engineering. " * 100
    truncated, is_truncated = safe_truncate_text(unicode_text, max_chars=150)
    assert is_truncated is True
    assert len(truncated) <= 180  # Max chars plus truncation notice
    assert "🚀" in truncated or "Desearch" in truncated


def test_per_source_content_budget():
    """Verify per-source character limit is enforced by ResearchContextBuilder."""
    builder = ResearchContextBuilder(max_source_chars=200, max_total_chars=1000)
    large_doc = {
        "url": "https://example.com/large",
        "title": "Large Document",
        "markdown": "A" * 5000,
    }
    context_text, metrics = builder.build_bounded_context([], [large_doc])
    assert metrics["truncated_sources"] == 1
    assert len(context_text) < 1000
    assert "https://example.com/large" in context_text


def test_global_context_budget():
    """Verify total global context budget stops appending additional content once limit is reached."""
    builder = ResearchContextBuilder(max_source_chars=500, max_total_chars=800)
    docs = [
        {"url": f"https://example.com/doc{i}", "title": f"Doc {i}", "markdown": "B" * 400}
        for i in range(10)
    ]
    context_text, metrics = builder.build_bounded_context([], docs)
    assert len(context_text) <= 1200
    assert metrics["sources_extracted"] == 10
    assert metrics["included_characters"] <= 900


def test_execution_scoped_url_deduplication():
    """Verify duplicate URLs are fetched only once and reused from execution cache."""
    builder = ResearchContextBuilder()
    url = "https://example.com/shared-spec"

    doc_data = {"url": url, "title": "Shared Spec", "markdown": "Specification content"}

    # First fetch miss
    cached1 = builder.get_cached_extraction(url)
    assert cached1 is None

    builder.cache_extraction(url, doc_data)

    # Second fetch hit (deduplication)
    cached2 = builder.get_cached_extraction(url)
    assert cached2 is not None
    assert cached2["title"] == "Shared Spec"
    assert builder.duplicate_fetches_avoided == 1


def test_research_agent_deduplication_and_budgeting():
    """Verify ResearchAgent uses ResearchContextBuilder to bound context and deduplicate URLs."""
    mock_llm = MagicMock(spec=LLMClient)
    mock_llm.generate_chat_completion.return_value = MagicMock(
        content='{"summary": "Evidence gathered", "evidence_items": [], "sources_consulted": ["https://example.com/spec"], "tools_executed": ["web_search", "web_fetch"]}'
    )

    mock_registry = MagicMock(spec=ToolRegistry)
    mock_search_tool = MagicMock()
    mock_search_tool.enabled = True
    mock_search_tool.execute.return_value = {
        "results": [{"title": "Spec Page", "url": "https://example.com/spec", "snippet": "Snippet text"}]
    }

    mock_fetch_tool = MagicMock()
    mock_fetch_tool.enabled = True
    mock_fetch_tool.execute.return_value = {
        "title": "Spec Page",
        "markdown": "Extracted Markdown " * 200,
    }

    def get_tool(tool_id):
        if tool_id == "web_search":
            return mock_search_tool
        if tool_id == "web_fetch":
            return mock_fetch_tool
        return None

    mock_registry.exists.return_value = True
    mock_registry.get.side_effect = get_tool

    agent = ResearchAgent(llm_client=mock_llm, tool_registry=mock_registry)
    tasks = [
        {"id": "t1", "title": "Task 1", "description": "Search 1"},
        {"id": "t2", "title": "Task 2", "description": "Search 2 (Same URL)"},
    ]

    res = agent.run_research(session_id="s1", goal="Test Goal", tasks=tasks)

    # ContentTool should only be called ONCE despite 2 tasks pointing to same URL
    assert mock_fetch_tool.execute.call_count == 1
    assert "web_search" in res.tools_executed
    assert "web_fetch" in res.tools_executed
