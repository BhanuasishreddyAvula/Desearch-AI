"""API router for Tool Registry endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.config import settings
from app.dependencies import (
    get_execution_time_dep,
    get_request_id_dep,
    get_tool_registry_dep,
)
from app.schemas.metadata import ResponseMetadata
from app.tools.base import BaseTool
from app.tools.registry import ToolRegistry
from app.tools.schemas import ToolEnvelope, ToolListEnvelope, ToolResponseSchema
from app.tools.service import ToolService

router = APIRouter(tags=["Tools"])


def get_tool_service(
    registry: Annotated[ToolRegistry, Depends(get_tool_registry_dep)],
) -> ToolService:
    """Dependency provider for ToolService."""
    return ToolService(registry=registry)


def _to_schema(tool: BaseTool) -> ToolResponseSchema:
    """Helper converting BaseTool instance to ToolResponseSchema."""
    return ToolResponseSchema(
        id=tool.id,
        name=tool.name,
        description=tool.description,
        category=tool.category.value
        if hasattr(tool.category, "value")
        else str(tool.category),
        version=tool.version,
        enabled=tool.enabled,
        supported_agents=[
            agent.value if hasattr(agent, "value") else str(agent)
            for agent in tool.supported_agents
        ],
        input_schema=tool.input_schema,
        output_schema=tool.output_schema,
    )


@router.get(
    "",
    response_model=ToolListEnvelope,
    summary="List All Registered Tools",
    description="Retrieve all registered tools and their metadata specifications from the catalog.",
)
async def list_tools(
    service: Annotated[ToolService, Depends(get_tool_service)],
    request_id: Annotated[str | None, Depends(get_request_id_dep)],
    execution_time_ms: Annotated[float, Depends(get_execution_time_dep)],
) -> ToolListEnvelope:
    """Get all tools endpoint."""
    tools = service.list_tools()
    data = [_to_schema(t) for t in tools]
    return ToolListEnvelope(
        success=True,
        message=f"Retrieved {len(data)} tools successfully.",
        request_id=request_id,
        data=data,
        metadata=ResponseMetadata(
            execution_time_ms=execution_time_ms,
            api_version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT.value,
        ),
    )


@router.get(
    "/categories/{category}",
    response_model=ToolListEnvelope,
    summary="List Tools by Category",
    description="Retrieve registered tools filtered by category (search, fetch, document, citation, utility).",
)
async def list_tools_by_category(
    category: str,
    service: Annotated[ToolService, Depends(get_tool_service)],
    request_id: Annotated[str | None, Depends(get_request_id_dep)],
    execution_time_ms: Annotated[float, Depends(get_execution_time_dep)],
) -> ToolListEnvelope:
    """Get tools by category endpoint."""
    tools = service.list_by_category(category)
    data = [_to_schema(t) for t in tools]
    return ToolListEnvelope(
        success=True,
        message=f"Retrieved {len(data)} tools for category '{category}'.",
        request_id=request_id,
        data=data,
        metadata=ResponseMetadata(
            execution_time_ms=execution_time_ms,
            api_version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT.value,
        ),
    )


@router.get(
    "/{tool_id}",
    response_model=ToolEnvelope,
    summary="Get Tool Details",
    description="Retrieve metadata specification for a specific tool by unique ID.",
)
async def get_tool(
    tool_id: str,
    service: Annotated[ToolService, Depends(get_tool_service)],
    request_id: Annotated[str | None, Depends(get_request_id_dep)],
    execution_time_ms: Annotated[float, Depends(get_execution_time_dep)],
) -> ToolEnvelope:
    """Get specific tool endpoint."""
    tool = service.get_tool(tool_id)
    return ToolEnvelope(
        success=True,
        message=f"Tool '{tool_id}' retrieved successfully.",
        request_id=request_id,
        data=_to_schema(tool),
        metadata=ResponseMetadata(
            execution_time_ms=execution_time_ms,
            api_version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT.value,
        ),
    )
