"""Universal Tool Registry cataloging tool capabilities."""

from app.observability.events import SystemEvents
from app.observability.logger import get_app_logger
from app.tools.base import BaseTool
from app.tools.builtin.citation_extractor import CitationExtractorTool
from app.tools.builtin.document_reader import DocumentReaderTool
from app.tools.builtin.web_fetch import WebFetchTool
from app.tools.builtin.web_search import WebSearchTool
from app.tools.enums import ToolCategory

logger = get_app_logger("tools.registry")


class ToolRegistry:
    """Central registry cataloging all tools available to AI agents."""

    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}
        self._register_builtin_tools()
        logger.event(
            SystemEvents.APPLICATION_STARTED,
            f"Tool Registry Initialized with {len(self._tools)} registered tools.",
        )

    def _register_builtin_tools(self) -> None:
        """Automatically register core built-in metadata tools."""
        builtins: list[BaseTool] = [
            WebSearchTool(),
            WebFetchTool(),
            DocumentReaderTool(),
            CitationExtractorTool(),
        ]
        for tool in builtins:
            self.register(tool)

    def register(self, tool: BaseTool) -> None:
        """Register a new tool instance in the catalog."""
        self._tools[tool.id] = tool
        logger.info(
            "Tool Registered | ID: %s | Category: %s | Version: %s",
            tool.id,
            tool.category.value
            if hasattr(tool.category, "value")
            else str(tool.category),
            tool.version,
        )

    def unregister(self, tool_id: str) -> bool:
        """Remove a tool from the catalog by ID."""
        if tool_id in self._tools:
            del self._tools[tool_id]
            logger.info("Tool Unregistered | ID: %s", tool_id)
            return True
        return False

    def get(self, tool_id: str) -> BaseTool | None:
        """Retrieve a registered tool instance by ID."""
        return self._tools.get(tool_id)

    def list_all(self) -> list[BaseTool]:
        """Return all registered tools in the catalog."""
        return list(self._tools.values())

    def list_by_category(self, category: ToolCategory | str) -> list[BaseTool]:
        """Return tools filtered by Category."""
        cat_str = (
            category.value if hasattr(category, "value") else str(category)
        )
        return [
            tool
            for tool in self._tools.values()
            if (
                tool.category.value
                if hasattr(tool.category, "value")
                else str(tool.category)
            )
            == cat_str
        ]

    def exists(self, tool_id: str) -> bool:
        """Check if a tool ID is registered."""
        return tool_id in self._tools

    def enable(self, tool_id: str) -> bool:
        """Enable a tool by ID."""
        tool = self.get(tool_id)
        if tool:
            tool.enabled = True
            logger.info("Tool Enabled | ID: %s", tool_id)
            return True
        return False

    def disable(self, tool_id: str) -> bool:
        """Disable a tool by ID."""
        tool = self.get(tool_id)
        if tool:
            tool.enabled = False
            logger.info("Tool Disabled | ID: %s", tool_id)
            return True
        return False
