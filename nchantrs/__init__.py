"""Nchantrs package initialization."""

__version__ = "0.0.1.0.1.1"
__author__ = "Solutions Brewer"
__license__ = "MIT"

import logging
import sys

# Configure package logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)
logger.info(f"Nchantrs v{__version__} initialized")

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "logger",
]
