"""Supabase and database configuration settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class SupabaseSettings(BaseSettings):
    """Supabase credentials and database connection string settings."""

    SUPABASE_URL: str = "https://your-supabase-project-id.supabase.co"
    SUPABASE_ANON_KEY: str = "your_supabase_anon_key_placeholder"
    SUPABASE_SERVICE_ROLE_KEY: str = "your_supabase_service_role_key_placeholder"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/desearch_ai"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
