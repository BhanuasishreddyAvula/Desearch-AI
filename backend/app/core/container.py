"""Application service container centralizing shared singleton infrastructure objects."""

from app.conversations.repository import AbstractConversationRepository
from app.conversations.supabase_repository import SupabaseConversationRepository
from app.core.config import Settings, settings
from app.core.llm.client import LLMClient
from app.core.repositories.session import AbstractSessionRepository
from app.observability.logger import AppLogger, get_app_logger
from app.observability.metrics import MetricsCollector, metrics
from app.observability.tracing import Tracer, tracer
from app.sessions.repository import InMemorySessionRepository
from app.sessions.supabase_repository import SupabaseSessionRepository
from app.tools.registry import ToolRegistry


class Container:
    """Lightweight application container centralizing shared singleton objects."""

    def __init__(self) -> None:
        self.settings: Settings = settings
        self.logger: AppLogger = get_app_logger("container")
        self.tracer: Tracer = tracer
        self.metrics: MetricsCollector = metrics
        self.llm_client: LLMClient = LLMClient()
        self.tool_registry: ToolRegistry = ToolRegistry()

        # Inject Supabase repository if credentials configured, else fallback to InMemory
        if settings.SUPABASE_URL and (
            settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY
        ):
            self.session_repository: AbstractSessionRepository = (
                SupabaseSessionRepository()
            )
            self.conversation_repository: AbstractConversationRepository = (
                SupabaseConversationRepository()
            )
            self.logger.info(
                "Initialized SupabaseSessionRepository + SupabaseConversationRepository"
            )
        else:
            self.session_repository = InMemorySessionRepository()
            self.conversation_repository = SupabaseConversationRepository()  # Fallback still uses Supabase for conv
            self.logger.info(
                "Initialized InMemorySessionRepository as fallback session repository"
            )

    def get_logger(self, name: str) -> AppLogger:
        """Factory method for creating named AppLogger instances."""
        return get_app_logger(name)


container = Container()
