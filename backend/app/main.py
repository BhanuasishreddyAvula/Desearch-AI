"""Main FastAPI application entry point for Desearch AI Backend."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import get_logger, setup_logging

# Setup console logging
setup_logging()
logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager handling application startup and shutdown events."""
    # Startup lifespan execution
    logger.info(
        "Starting up %s v%s in %s mode",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.ENVIRONMENT,
    )
    yield
    # Shutdown lifespan execution
    logger.info("Shutting down %s", settings.APP_NAME)


app = FastAPI(
    title=settings.APP_NAME,
    description="Production-grade AI Research Workbench Backend",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Register centralized API router under /api/v1
app.include_router(api_router, prefix=settings.API_V1_STR)
