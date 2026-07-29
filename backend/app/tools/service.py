"""Service layer for querying Tool Registry."""

from app.core.exceptions import ResourceNotFoundException
from app.tools.base import BaseTool
from app.tools.registry import ToolRegistry


class ToolService:
    """Service handling tool catalog retrieval operations."""

    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    def list_tools(self) -> list[BaseTool]:
        """Retrieve all tools registered in the catalog."""
        return self.registry.list_all()

    def get_tool(self, tool_id: str) -> BaseTool:
        """Retrieve a specific tool by ID or raise ResourceNotFoundException."""
        tool = self.registry.get(tool_id)
        if not tool:
            raise ResourceNotFoundException(
                message=f"Tool with ID '{tool_id}' was not found in registry."
            )
        return tool

    def list_by_category(self, category: str) -> list[BaseTool]:
        """Retrieve tools filtered by category name."""
        return self.registry.list_by_category(category)
