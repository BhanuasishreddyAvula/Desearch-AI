"""Production Web Search Tool delegating to ExaProvider."""

from typing import Any

from app.tools.base import BaseTool
from app.tools.enums import AgentType, ToolCategory
from app.tools.models import ToolMetadata
from app.tools.search.provider import ExaProvider


class SearchTool(BaseTool):
    """Production Search Tool executing queries via ExaProvider."""

    def __init__(self, provider: ExaProvider | None = None) -> None:
        self.provider = provider or ExaProvider()

    @property
    def metadata(self) -> ToolMetadata:
        """Return metadata specification for Search Tool."""
        return ToolMetadata(
            id="web_search",
            name="Web Search Tool",
            description=(
                "Executes targeted web search queries to discover relevant"
                " online documents and sources via Exa AI Search."
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
                    "query": {"type": "string"},
                    "results": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "url": {"type": "string"},
                                "snippet": {"type": "string"},
                                "published_at": {"type": "string"},
                                "score": {"type": "number"},
                            },
                        },
                    },
                    "total_results": {"type": "integer"},
                    "latency_ms": {"type": "number"},
                },
            },
            version="2.0.0",
            enabled=True,
        )

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        """Execute search query via ExaProvider and return normalized dictionary output."""
        query = str(kwargs.get("query", "general technical research"))
        max_results = int(kwargs.get("max_results", 5))
        result = self.provider.search(query=query, max_results=max_results)
        return result.to_dict()
