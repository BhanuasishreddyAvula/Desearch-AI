"""Document Reader placeholder tool metadata and mock execution."""

from typing import Any

from app.tools.base import BaseTool
from app.tools.enums import AgentType, ToolCategory
from app.tools.models import ToolMetadata


class DocumentReaderTool(BaseTool):
    """Metadata and deterministic mock execution tool for reading documents."""

    @property
    def metadata(self) -> ToolMetadata:
        """Return metadata specification for Document Reader tool."""
        return ToolMetadata(
            id="document_reader",
            name="Document Reader Tool",
            description=(
                "Parses PDF, Markdown, or plain text documents and extracts"
                " structured text content."
            ),
            category=ToolCategory.DOCUMENT,
            supported_agents=[
                AgentType.RESEARCH,
                AgentType.WRITER,
                AgentType.ORCHESTRATOR,
            ],
            input_schema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path or URL to document file",
                    }
                },
                "required": ["file_path"],
            },
            output_schema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "page_count": {"type": "integer"},
                },
            },
            version="1.0.0",
            enabled=True,
        )

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        """Execute mock document reading returning deterministic text content."""
        file_path = str(kwargs.get("file_path", "doc.pdf"))
        return {
            "text": f"Parsed text findings and structural specifications from document {file_path}.",
            "page_count": 3,
        }
