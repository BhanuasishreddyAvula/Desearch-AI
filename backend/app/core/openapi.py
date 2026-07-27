"""OpenAPI metadata and tag specifications for Desearch AI."""

from typing import Any
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.core.config import settings

# API Tag Definitions
OPENAPI_TAGS: list[dict[str, str]] = [
    {
        "name": "Health",
        "description": "Health check and diagnostic endpoints for operational monitoring.",
    },
    {
        "name": "System",
        "description": "System status, environment parameters, and platform health.",
    },
    {
        "name": "Research",
        "description": (
            "Research query submission, execution plan, and report generation"
            " endpoints."
        ),
    },
    {
        "name": "Sessions",
        "description": (
            "Research session lifecycle, context inspection, and trace logging."
        ),
    },
    {
        "name": "Agents",
        "description": (
            "Multi-agent pipeline inspection, status, and role configurations."
        ),
    },
    {
        "name": "Tools",
        "description": (
            "Tool registry, tool execution, and source gathering integrations."
        ),
    },
    {
        "name": "Administration",
        "description": (
            "Platform management, quota monitoring, and system metrics."
        ),
    },
]


def custom_openapi(app: FastAPI) -> dict[str, Any]:
    """Generate customized OpenAPI schema for Desearch AI."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "Production-grade AI Research & Workbench API built using a "
            "modular multi-agent orchestration architecture."
        ),
        routes=app.routes,
        tags=OPENAPI_TAGS,
    )

    openapi_schema["info"]["contact"] = {
        "name": "Desearch AI Engineering Team",
        "email": "engineering@desearch.ai",
        "url": "https://github.com/your-org/desearch-ai",
    }
    openapi_schema["info"]["license"] = {
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema
