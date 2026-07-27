"""Supabase database client initialization and management."""

from supabase import Client, create_client

from app.core.config import settings
from app.core.exceptions import AppException
from app.observability.logger import get_app_logger

logger = get_app_logger("database")

_supabase_client: Client | None = None


def get_supabase_client() -> Client:
    """Initialize and return singleton Supabase client instance."""
    global _supabase_client

    if _supabase_client is not None:
        return _supabase_client

    url = settings.SUPABASE_URL
    key = settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY

    if not url or not key:
        logger.error("Supabase URL or Key is missing from configuration")
        raise AppException(
            message="Supabase credentials are not configured",
            error_code="DATABASE_CONFIG_ERROR",
        )

    try:
        _supabase_client = create_client(url, key)
        logger.info("Supabase client initialized successfully (%s)", url)
        return _supabase_client
    except Exception as exc:
        logger.exception("Failed to initialize Supabase client: %s", str(exc))
        raise AppException(
            message=f"Failed to connect to Supabase: {str(exc)}",
            error_code="DATABASE_CONNECTION_ERROR",
        ) from exc
