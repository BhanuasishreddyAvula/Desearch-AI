"""Standard Python logging setup for Desearch AI Backend."""

import logging
import sys

from app.core.config import settings
from app.core.constants import DEFAULT_DATE_FORMAT, DEFAULT_LOG_FORMAT


def setup_logging(log_level: str | None = None) -> logging.Logger:
    """Configure and return the root logger for the application."""
    level_str = log_level or settings.LOG_LEVEL.value or ("DEBUG" if settings.DEBUG else "INFO")
    numeric_level = getattr(logging, level_str.upper(), logging.INFO)

    formatter = logging.Formatter(fmt=DEFAULT_LOG_FORMAT, datefmt=DEFAULT_DATE_FORMAT)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(numeric_level)

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    if not root_logger.handlers:
        root_logger.addHandler(console_handler)

    app_logger = logging.getLogger("desearch_ai")
    app_logger.setLevel(numeric_level)

    return app_logger


def get_logger(name: str) -> logging.Logger:
    """Get a named logger instance inheriting standard configuration."""
    return logging.getLogger(f"desearch_ai.{name}")
