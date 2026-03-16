"""Nchantrs package initialization."""

import logging
import sys
from typing import Any

# Import agent awareness
from nchantrs.agent_awareness import get_agent_workspace, get_current_agent, is_agent_available

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


def main() -> int:
    """Main entry point for the nchantrs CLI."""
    logger.info("Running nchantrs CLI")
    return 0


if __name__ == "__main__":
    sys.exit(main())
