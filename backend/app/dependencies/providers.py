"""Infrastructure dependency providers for FastAPI endpoints."""

from app.conversations.repository import AbstractConversationRepository
from app.core.config import Settings, settings
from app.core.container import Container, container
from app.core.llm.client import LLMClient
from app.core.repositories.session import AbstractSessionRepository
from app.observability.logger import AppLogger, get_app_logger
from app.observability.metrics import MetricsCollector, metrics
from app.observability.tracing import Tracer, tracer
from app.tools.registry import ToolRegistry


def get_container() -> Container:
    """Dependency provider returning the shared application container."""
    return container


def get_settings_dep() -> Settings:
    """Dependency provider returning application settings."""
    return settings


def get_logger_dep(name: str = "api") -> AppLogger:
    """Dependency provider returning a named AppLogger instance."""
    return get_app_logger(name)


def get_tracer_dep() -> Tracer:
    """Dependency provider returning the tracer engine."""
    return tracer


def get_metrics_dep() -> MetricsCollector:
    """Dependency provider returning the metrics collector."""
    return metrics


def get_session_repository_dep() -> AbstractSessionRepository:
    """Dependency provider returning the active session repository interface implementation."""
    return container.session_repository


def get_conversation_repository_dep() -> AbstractConversationRepository:
    """Dependency provider returning the active conversation message repository."""
    return container.conversation_repository


def get_llm_client_dep() -> LLMClient:
    """Dependency provider returning the shared LLMClient instance."""
    return container.llm_client


def get_tool_registry_dep() -> ToolRegistry:
    """Dependency provider returning the singleton ToolRegistry instance."""
    return container.tool_registry
