"""Infrastructure dependency providers for FastAPI endpoints."""

from app.core.config import Settings, settings
from app.core.container import Container, container
from app.observability.logger import AppLogger, get_app_logger
from app.observability.metrics import MetricsCollector, metrics
from app.observability.tracing import Tracer, tracer


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
