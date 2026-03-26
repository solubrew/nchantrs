# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name:
	description: >
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt

import logging


logger = logging.getLogger(__name__)
# Add at the top of the file, before any other Qt imports
import os
import sys

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from typing import Optional, Dict, List, Any, Tuple
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


# Configure Qt environment before importing Qt modules
def _configure_qt_environment() -> None:
    """Configure Qt environment for better compatibility"""

    # WebEngine Chromium flags for stability
    chromium_flags = [
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--disable-gpu-sandbox",
        "--no-sandbox",
        "--disable-dev-shm-usage",
    ]

    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = " ".join(chromium_flags)
    os.environ["QT_QUICK_BACKEND"] = "software"
    os.environ["QT_OPENGL"] = "software"

    # Platform specific settings (only if not already set)
    if "QT_QPA_PLATFORM" not in os.environ:
        if sys.platform.startswith("linux"):
            os.environ["QT_QPA_PLATFORM"] = "xcb"


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
