"""Abstract BaseTool class for the Tool Registry."""

from abc import ABC, abstractmethod
from typing import Any

from app.tools.enums import AgentType, ToolCategory
from app.tools.models import ToolMetadata


class BaseTool(ABC):
    """Abstract base class for all tools registered in Desearch AI."""

    @property
    @abstractmethod
    def metadata(self) -> ToolMetadata:
        """Return tool metadata specification."""
        ...

    @property
    def id(self) -> str:
        """Return unique tool ID."""
        return self.metadata.id

    @property
    def name(self) -> str:
        """Return human-readable tool display name."""
        return self.metadata.name

    @property
    def description(self) -> str:
        """Return detailed description of tool capability."""
        return self.metadata.description

    @property
    def category(self) -> ToolCategory:
        """Return tool category."""
        return self.metadata.category

    @property
    def version(self) -> str:
        """Return tool semantic version."""
        return self.metadata.version

    @property
    def enabled(self) -> bool:
        """Return enabled status flag."""
        return self.metadata.enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Set enabled status flag."""
        self.metadata.enabled = value

    @property
    def supported_agents(self) -> list[AgentType]:
        """Return list of supported AI agent roles."""
        return self.metadata.supported_agents

    @property
    def input_schema(self) -> dict[str, Any]:
        """Return JSON schema for input arguments."""
        return self.metadata.input_schema

    @property
    def output_schema(self) -> dict[str, Any]:
        """Return JSON schema for output return value."""
        return self.metadata.output_schema

    def execute(self, **kwargs: Any) -> Any:
        """Execute tool logic (Stub method - execution out-of-scope for registry ticket)."""
        raise NotImplementedError(
            f"Execution for tool '{self.id}' is not implemented."
        )
