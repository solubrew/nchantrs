"""Nchantrs package initialization."""

import logging
from typing import Any

__version__: str = "1.0.0"
__author__: str = "Nchantrs Team"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger: logging.Logger = logging.getLogger(__name__)


def get_version() -> str:
    """Get the package version."""
    return __version__


def initialize() -> None:
    """Initialize the nchantrs package."""
    logger.info("Initializing nchantrs package")
