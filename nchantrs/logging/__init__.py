"""Nchantrs logging configuration module."""

import logging
import sys
from pathlib import Path
from typing import Optional

# Default log format
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Log levels
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None,
    date_format: Optional[str] = None,
) -> logging.Logger:
    """Set up logging for nchantrs.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
        format_string: Custom format string for log messages
        date_format: Custom date format for timestamps

    Returns:
        Configured logger instance
    """
    log_level = LOG_LEVELS.get(level.upper(), logging.INFO)
    fmt = format_string or DEFAULT_FORMAT
    date_fmt = date_format or DEFAULT_DATE_FORMAT

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=fmt,
        datefmt=date_fmt,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger("nchantrs")
    logger.setLevel(log_level)

    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(fmt, date_fmt))
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger for a specific module.

    Args:
        name: Name of the module (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(f"nchantrs.{name}")


# Default logger instance
logger = setup_logging()
