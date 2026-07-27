"""Centralized API v1 Router aggregator for Desearch AI."""

from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.sessions.router import router as sessions_router

api_router = APIRouter()

# Include feature domain routers
api_router.include_router(health_router)
api_router.include_router(sessions_router, prefix="/sessions")
