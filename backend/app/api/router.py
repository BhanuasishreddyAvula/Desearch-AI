"""Centralized API v1 Router aggregator for Desearch AI."""

from fastapi import APIRouter

from app.agents.planner.router import router as planner_router
from app.agents.research.router import router as research_router
from app.agents.reviewer.router import router as reviewer_router
from app.agents.writer.router import router as writer_router
from app.api.v1.health import router as health_router
from app.orchestrator.router import router as orchestrator_router
from app.sessions.router import router as sessions_router
from app.tools.router import router as tools_router

api_router = APIRouter()

# Include feature domain routers
api_router.include_router(health_router)
api_router.include_router(sessions_router, prefix="/sessions")
api_router.include_router(planner_router, prefix="/planner")
api_router.include_router(research_router, prefix="/research")
api_router.include_router(writer_router, prefix="/writer")
api_router.include_router(reviewer_router, prefix="/reviewer")
api_router.include_router(orchestrator_router, prefix="/orchestrator")
api_router.include_router(tools_router, prefix="/tools")
