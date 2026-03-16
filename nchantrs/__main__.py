"""Nchantrs package entry point."""

import logging
import sys
from nchantrs import main
from typing import Optional, Dict, List, Any, Tuple

logger: logging.Logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting nchantrs from __main__")
    sys.exit(main())
