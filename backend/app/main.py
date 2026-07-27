"""Main FastAPI application entry point for Desearch AI Backend."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.openapi import custom_openapi
from app.middleware import register_middleware
from app.observability.events import SystemEvents
from app.observability.logger import get_app_logger

# Setup console logging
setup_logging()
logger = get_app_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager handling application startup and shutdown events."""
    logger.event(
        SystemEvents.APPLICATION_STARTED,
        f"Starting up {settings.APP_NAME} v{settings.APP_VERSION} in {settings.ENVIRONMENT} mode",
    )
    yield
    logger.event(
        SystemEvents.APPLICATION_STOPPED,
        f"Shutting down {settings.APP_NAME}",
    )


app = FastAPI(
    title=settings.APP_NAME,
    description="Production-grade AI Research Workbench Backend",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Customize OpenAPI schema
app.openapi = lambda: custom_openapi(app)  # type: ignore[method-assign]

# Register application middleware in correct execution sequence
register_middleware(app)

# Register global exception handlers
register_exception_handlers(app)

# Register centralized API router under /api/v1
app.include_router(api_router, prefix=settings.API_V1_STR)
