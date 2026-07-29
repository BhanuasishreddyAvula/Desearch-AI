"""Web Search placeholder tool metadata and mock execution."""

from typing import Any

from app.tools.base import BaseTool
from app.tools.enums import AgentType, ToolCategory
from app.tools.models import ToolMetadata


class WebSearchTool(BaseTool):
    """Metadata and deterministic mock execution tool for web search queries."""

    @property
    def metadata(self) -> ToolMetadata:
        """Return metadata specification for Web Search tool."""
        return ToolMetadata(
            id="web_search",
            name="Web Search Tool",
            description=(
                "Executes targeted web search queries to discover relevant"
                " online documents and sources."
            ),
            category=ToolCategory.SEARCH,
            supported_agents=[AgentType.RESEARCH, AgentType.ORCHESTRATOR],
            input_schema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string",
                    },
                    "max_results": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
            output_schema={
                "type": "object",
                "properties": {
                    "results": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "url": {"type": "string"},
                                "snippet": {"type": "string"},
                            },
                        },
                    }
                },
            },
            version="1.0.0",
            enabled=True,
        )

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        """Execute mock web search returning deterministic result data."""
        query = str(kwargs.get("query", "general technical research"))
        return {
            "results": [
                {
                    "title": f"Authoritative documentation on {query[:40]}",
                    "url": "https://docs.example.com/technical-spec",
                    "snippet": (
                        f"Primary technical specification and architectural breakdown regarding {query}."
                    ),
                },
                {
                    "title": f"Benchmark evaluation report: {query[:40]}",
                    "url": "https://benchmarks.example.org/analysis",
                    "snippet": (
                        f"Empirical performance data and comparative findings for {query}."
                    ),
                },
            ]
        }
