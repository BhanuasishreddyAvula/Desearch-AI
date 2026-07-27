"""Application service container centralizing shared singleton infrastructure objects."""

from app.core.config import Settings, settings
from app.observability.logger import AppLogger, get_app_logger
from app.observability.metrics import MetricsCollector, metrics
from app.observability.tracing import Tracer, tracer


class Container:
    """Lightweight application container centralizing shared singleton objects."""

    def __init__(self) -> None:
        self.settings: Settings = settings
        self.logger: AppLogger = get_app_logger("container")
        self.tracer: Tracer = tracer
        self.metrics: MetricsCollector = metrics

    def get_logger(self, name: str) -> AppLogger:
        """Factory method for creating named AppLogger instances."""
        return get_app_logger(name)


container = Container()
