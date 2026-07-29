"""Unit tests for SearchTool, ContentTool, ExaProvider, and FirecrawlProvider."""

import pytest
from unittest.mock import MagicMock, patch

from app.core.exceptions import AuthenticationException
from app.tools.content.exceptions import ContentAuthenticationException
from app.tools.content.models import ExtractedDocument
from app.tools.content.provider import FirecrawlProvider
from app.tools.content.tool import ContentTool
from app.tools.registry import ToolRegistry
from app.tools.search.exceptions import SearchAuthenticationException
from app.tools.search.models import SearchResult, SearchResultItem
from app.tools.search.provider import ExaProvider
from app.tools.search.tool import SearchTool


def test_exa_provider_missing_api_key_raises_exception():
    """Verify ExaProvider raises SearchAuthenticationException when API key is unconfigured."""
    provider = ExaProvider(api_key="")
    with pytest.raises(SearchAuthenticationException) as exc_info:
        provider.search("test query")
    assert "EXA_API_KEY is missing" in str(exc_info.value)


def test_firecrawl_provider_missing_api_key_raises_exception():
    """Verify FirecrawlProvider raises ContentAuthenticationException when API key is unconfigured."""
    provider = FirecrawlProvider(api_key="")
    with pytest.raises(ContentAuthenticationException) as exc_info:
        provider.scrape("https://example.com")
    assert "FIRECRAWL_API_KEY is missing" in str(exc_info.value)


def test_exa_provider_successful_search(httpx_mock=None):
    """Verify ExaProvider correctly parses HTTP 200 JSON response from Exa REST API."""
    mock_response_data = {
        "results": [
            {
                "title": "Example Exa Page",
                "url": "https://exa.ai/test",
                "text": "Exa search result snippet text.",
                "publishedDate": "2026-01-01T00:00:00Z",
                "score": 0.98,
            }
        ]
    }
    with patch("httpx.Client.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response_data
        mock_post.return_value = mock_resp

        provider = ExaProvider(api_key="test-exa-key")
        res = provider.search("python async", max_results=1)

        assert isinstance(res, SearchResult)
        assert len(res.results) == 1
        assert res.results[0].title == "Example Exa Page"
        assert res.results[0].url == "https://exa.ai/test"
        assert res.results[0].score == 0.98


def test_firecrawl_provider_successful_scrape():
    """Verify FirecrawlProvider correctly parses HTTP 200 JSON response from Firecrawl API."""
    mock_response_data = {
        "success": True,
        "data": {
            "markdown": "# Firecrawl Page Title\n\nContent body text.",
            "metadata": {
                "title": "Firecrawl Page Title",
                "sourceURL": "https://example.com/article",
            },
        },
    }
    with patch("httpx.Client.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_response_data
        mock_post.return_value = mock_resp

        provider = FirecrawlProvider(api_key="test-firecrawl-key")
        doc = provider.scrape("https://example.com/article")

        assert isinstance(doc, ExtractedDocument)
        assert doc.title == "Firecrawl Page Title"
        assert "Firecrawl Page Title" in doc.markdown


def test_tool_registry_contains_production_tools():
    """Verify ToolRegistry catalogs production SearchTool and ContentTool."""
    registry = ToolRegistry()
    assert registry.exists("web_search")
    assert registry.exists("web_fetch")
    search_tool = registry.get("web_search")
    content_tool = registry.get("web_fetch")
    assert isinstance(search_tool, SearchTool)
    assert isinstance(content_tool, ContentTool)
