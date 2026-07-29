"""Web Fetch placeholder tool metadata and mock execution."""

from typing import Any

from app.tools.base import BaseTool
from app.tools.enums import AgentType, ToolCategory
from app.tools.models import ToolMetadata


class WebFetchTool(BaseTool):
    """Metadata and deterministic mock execution tool for fetching web page content."""

    @property
    def metadata(self) -> ToolMetadata:
        """Return metadata specification for Web Fetch tool."""
        return ToolMetadata(
            id="web_fetch",
            name="Web Fetch Tool",
            description="Fetches raw HTML/Markdown content from a specified URL.",
            category=ToolCategory.FETCH,
            supported_agents=[AgentType.RESEARCH, AgentType.ORCHESTRATOR],
            input_schema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "description": "Target web page URL",
                    }
                },
                "required": ["url"],
            },
            output_schema={
                "type": "object",
                "properties": {
                    "url": {"type": "string"},
                    "content": {"type": "string"},
                    "status_code": {"type": "integer"},
                },
            },
            version="1.0.0",
            enabled=True,
        )

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        """Execute mock web fetch returning deterministic content data."""
        url = str(kwargs.get("url", "https://docs.example.com/technical-spec"))
        return {
            "url": url,
            "content": (
                f"# Retrieved Content\nOfficial technical documentation extracted from {url}.\n"
                "System architecture features high-throughput REST API processing and low-latency storage."
            ),
            "status_code": 200,
        }
