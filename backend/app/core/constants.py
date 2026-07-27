"""Application constants and default specifications."""

# System Identity & Versioning
DEFAULT_APP_NAME: str = "Desearch AI Backend"
DEFAULT_APP_VERSION: str = "0.1.0"
DEFAULT_SERVICE_NAME: str = "desearch-ai-backend"

# Server Network Defaults
DEFAULT_HOST: str = "0.0.0.0"
DEFAULT_PORT: int = 8000

# API Routing Specifications
API_V1_STR: str = "/api/v1"
HEALTH_CHECK_PATH: str = "/health"

# HTTP Headers
CORRELATION_ID_HEADER: str = "X-Correlation-ID"
API_KEY_HEADER: str = "X-API-Key"

# System Timeouts & Operational Limits
DEFAULT_TIMEOUT_SECONDS: int = 30
DEFAULT_MAX_RETRIES: int = 3
DEFAULT_CACHE_TTL_SECONDS: int = 3600
DEFAULT_RATE_LIMIT_WINDOW_SECONDS: int = 60

# Logging Formats
DEFAULT_LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DEFAULT_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
