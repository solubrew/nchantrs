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
import os
import sys

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from typing import Optional, Dict, List, Any, Tuple

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")

"""
Qt Application setup and configuration for graphics compatibility
"""


def configure_qt_for_webengine() -> None:
    """
    Configure Qt environment variables for WebEngine compatibility
    Must be called before QApplication is created
    """
    # Graphics backend configuration
    qt_flags = [
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--disable-gpu-sandbox",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-extensions",
        "--disable-plugins",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-renderer-backgrounding",
        "--disable-features=TranslateUI",
        "--disable-ipc-flooding-protection",
        "--enable-logging",
        "--log-level=0",
    ]
    # Set Chromium flags
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = " ".join(qt_flags)
    # Force software rendering for better compatibility
    os.environ["QT_QUICK_BACKEND"] = "software"
    # Set graphics platform (only if not already set, e.g., by environment)
    if "QT_QPA_PLATFORM" not in os.environ:
        if sys.platform.startswith("linux"):
            os.environ["QT_QPA_PLATFORM"] = "xcb"
        elif sys.platform == "darwin":
            os.environ["QT_QPA_PLATFORM"] = "cocoa"
        elif sys.platform.startswith("win"):
            os.environ["QT_QPA_PLATFORM"] = "windows"
    # OpenGL configuration
    os.environ["QT_OPENGL"] = "software"  # Use software OpenGL for stability
    # Alternative: os.environ["QT_OPENGL"] = "es2"  # Use OpenGL ES 2.0
    # Disable hardware acceleration features that can cause issues
    os.environ["QTWEBENGINE_DISABLE_GPU_THREAD"] = "1"
    # Additional compatibility settings
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
    os.environ["QT_SCALE_FACTOR"] = "1"
    logma.info("Qt WebEngine environment configured for compatibility")


def setup_application_attributes() -> None:
    """
    Set Qt application attributes for better graphics compatibility
    Must be called before QApplication is created
    """
    try:
        # Enable software rendering
        pyqt.QApplication.setAttribute(pyqt.Qt.ApplicationAttribute.AA_UseSoftwareOpenGL, True)
        # Disable high DPI scaling issues
        pyqt.QApplication.setAttribute(pyqt.Qt.ApplicationAttribute.AA_DisableHighDpiScaling, True)
        # Use desktop OpenGL
        pyqt.QApplication.setAttribute(pyqt.Qt.ApplicationAttribute.AA_UseDesktopOpenGL, False)
        # Enable OpenGL ES
        pyqt.QApplication.setAttribute(pyqt.Qt.ApplicationAttribute.AA_UseOpenGLES, False)
        logma.info("Qt application attributes configured")
    except AttributeError as e:
        logma.warning(f"Some Qt attributes not available: {e}")


def initialize_qt_application() -> None:
    """
    Initialize Qt application with proper configuration
    """
    configure_qt_for_webengine()
    setup_application_attributes()


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
