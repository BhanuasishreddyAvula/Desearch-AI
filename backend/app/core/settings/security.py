import json
from typing import Any
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class SecuritySettings(BaseSettings):
    """Security, tokens, and CORS configuration."""

    SECRET_KEY: str = "change_this_secret_key_in_production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*",
    ]
    API_KEY_SECRET: str = "change_this_api_key_secret_in_production"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            v_clean = v.strip()
            if not v_clean:
                return ["*"]
            if v_clean.startswith("[") and v_clean.endswith("]"):
                try:
                    return json.loads(v_clean)
                except Exception:
                    # Fallback if single quotes or malformed JSON
                    cleaned = v_clean.strip("[]").replace("'", '"')
                    try:
                        return json.loads(cleaned)
                    except Exception:
                        pass
            return [i.strip().strip("'\"") for i in v_clean.split(",") if i.strip()]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
