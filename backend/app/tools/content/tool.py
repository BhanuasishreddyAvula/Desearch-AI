"""Production Web Fetch Content Tool delegating to FirecrawlProvider."""

from typing import Any

from app.tools.base import BaseTool
from app.tools.content.provider import FirecrawlProvider
from app.tools.enums import AgentType, ToolCategory
from app.tools.models import ToolMetadata


class ContentTool(BaseTool):
    """Production Content Tool extracting webpage markdown via FirecrawlProvider."""

    def __init__(self, provider: FirecrawlProvider | None = None) -> None:
        self.provider = provider or FirecrawlProvider()

    @property
    def metadata(self) -> ToolMetadata:
        """Return metadata specification for Content Tool."""
        return ToolMetadata(
            id="web_fetch",
            name="Web Fetch Tool",
            description=(
                "Fetches raw HTML/Markdown content from a specified URL via"
                " Firecrawl web extraction."
            ),
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
                    "title": {"type": "string"},
                    "markdown": {"type": "string"},
                    "plain_text": {"type": "string"},
                    "metadata": {"type": "object"},
                    "content": {"type": "string"},
                    "status_code": {"type": "integer"},
                },
            },
            version="2.0.0",
            enabled=True,
        )

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        """Execute content extraction via FirecrawlProvider and return normalized output dictionary."""
        url = str(kwargs.get("url", "https://docs.example.com/spec"))
        doc = self.provider.scrape(url=url)
        return doc.to_dict()
