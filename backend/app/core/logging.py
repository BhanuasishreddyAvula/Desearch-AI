"""Standard Python logging setup for Desearch AI Backend."""

import logging
import sys
from typing import Optional

from app.core.config import settings


def setup_logging(log_level: Optional[str] = None) -> logging.Logger:
    """Configure and return the root logger for the application.

    Args:
        log_level: Optional log level override (DEBUG, INFO, WARNING, ERROR).

    Returns:
        logging.Logger: Configured logger instance.
    """
    level_str = log_level or ("DEBUG" if settings.DEBUG else "INFO")
    numeric_level = getattr(logging, level_str.upper(), logging.INFO)

    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(numeric_level)

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Avoid adding duplicate handlers if setup_logging is called multiple times
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)

    app_logger = logging.getLogger("desearch_ai")
    app_logger.setLevel(numeric_level)

    return app_logger


def get_logger(name: str) -> logging.Logger:
    """Get a named logger instance inheriting standard configuration.

    Args:
        name: Name of the module or component requesting logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    return logging.getLogger(f"desearch_ai.{name}")
