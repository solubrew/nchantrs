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


def _webengine_mode() -> str:
    """Rendering mode: 'hardware' (default) or 'software'.

    Override per-run with NCHANTD_WEBENGINE_MODE=software|hardware. Hardware is
    the default because this is a real desktop GL stack; the all-software path
    (--disable-gpu + AA_UseSoftwareOpenGL + QT_OPENGL=software) was observed to
    produce a blank web surface here ("GPUInfo not initialized on GpuInfoUpdate"
    with correct geometry).
    """
    return os.environ.get("NCHANTD_WEBENGINE_MODE", "hardware").strip().lower()


def configure_qt_for_webengine() -> None:
    """
    Configure Qt environment variables for WebEngine compatibility
    Must be called before QApplication is created
    """
    mode = _webengine_mode()
    logma.info(f"[graphics] webengine render mode = {mode}")

    # Optional: enable Chromium remote debugging so the embedded pages can be
    # inspected from a real browser's DevTools (Network tab shows response codes,
    # WebSocket frames, full console). Run with:
    #   NCHANTD_WEBENGINE_DEBUG_PORT=9222 python cmds/runNchantdOffice.py
    # then open http://localhost:9222 in Chrome/Chromium.
    _dbg_port = os.environ.get("NCHANTD_WEBENGINE_DEBUG_PORT")
    if _dbg_port:
        # Set BOTH mechanisms: the env var and the explicit Chromium flag
        # (the flag is the reliable one across Qt builds). Bind to all
        # interfaces so it's reachable even if localhost resolution is odd.
        os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = _dbg_port
        logma.info(f"[graphics] remote debugging ENABLED on port {_dbg_port} (open http://localhost:{_dbg_port})")

    # Flags that are safe/beneficial in both modes.
    common_flags = [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-extensions",
        "--disable-plugins",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-renderer-backgrounding",
        # UserAgentClientHint(*): stop Chromium from emitting Sec-CH-UA request
        # headers and navigator.userAgentData. Our profile UA is Firefox (F2), and
        # real Firefox sends NO client hints — leaving Chromium's Chrome-branded
        # hints in place is the Firefox-UA/Chrome-hints mismatch that makes Google
        # hard-block a fresh embedded sign-in. Disabling them makes the identity
        # consistently Firefox. Combined into one --disable-features (Chromium
        # honours a single comma-separated list, not repeated flags).
        "--disable-features=TranslateUI,UserAgentClientHint,UserAgentClientHintFullVersionList",
        "--disable-ipc-flooding-protection",
        "--enable-logging",
        "--log-level=0",
    ]
    if _dbg_port:
        common_flags.append(f"--remote-debugging-port={_dbg_port}")
        common_flags.append("--remote-allow-origins=*")
    if mode == "software":
        # Deliberate all-software path. CRITICAL: when the GPU is disabled the
        # software rasterizer MUST stay enabled (do NOT add
        # --disable-software-rasterizer) or Chromium cannot rasterize at all and
        # every web view is blank.
        render_flags = ["--disable-gpu", "--enable-unsafe-swiftshader", "--disable-gpu-sandbox"]
    else:
        # Hardware path: let Chromium use the GPU. Ignore the driver blocklist so
        # it doesn't silently fall back to the (broken-here) software compositor.
        render_flags = ["--ignore-gpu-blocklist", "--enable-gpu-rasterization"]

    qt_flags = render_flags + common_flags
    # An explicit override wins over the computed flags, so a run can be tuned
    # without editing code (e.g. QTWEBENGINE_CHROMIUM_FLAGS_OVERRIDE=... ).
    override = os.environ.get("QTWEBENGINE_CHROMIUM_FLAGS_OVERRIDE")
    chromium_flags = override if override else " ".join(qt_flags)
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = chromium_flags
    logma.info(f"[graphics] QTWEBENGINE_CHROMIUM_FLAGS = {chromium_flags}")
    if override:
        logma.info("[graphics] (using QTWEBENGINE_CHROMIUM_FLAGS_OVERRIDE)")

    # Set graphics platform (only if not already set, e.g., by environment)
    if "QT_QPA_PLATFORM" not in os.environ:
        if sys.platform.startswith("linux"):
            os.environ["QT_QPA_PLATFORM"] = "xcb"
        elif sys.platform == "darwin":
            os.environ["QT_QPA_PLATFORM"] = "cocoa"
        elif sys.platform.startswith("win"):
            os.environ["QT_QPA_PLATFORM"] = "windows"

    if mode == "software":
        os.environ["QT_QUICK_BACKEND"] = "software"
        os.environ["QT_OPENGL"] = "software"
        os.environ["QTWEBENGINE_DISABLE_GPU_THREAD"] = "1"
    else:
        # Hardware: make sure no stale software forcing leaks in from a prior run.
        for _k in ("QT_QUICK_BACKEND", "QT_OPENGL", "QTWEBENGINE_DISABLE_GPU_THREAD",
                   "LIBGL_ALWAYS_SOFTWARE"):
            os.environ.pop(_k, None)

    # DPI settings (harmless in both modes)
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
    os.environ["QT_SCALE_FACTOR"] = "1"

    # Dump the full resulting environment so a blank/rendered outcome can be
    # correlated with the exact flags that produced it.
    for _k in (
        "QTWEBENGINE_CHROMIUM_FLAGS", "QT_QUICK_BACKEND", "QT_QPA_PLATFORM",
        "QT_OPENGL", "QTWEBENGINE_DISABLE_GPU_THREAD", "QT_AUTO_SCREEN_SCALE_FACTOR",
        "QT_SCALE_FACTOR", "LIBGL_ALWAYS_SOFTWARE",
    ):
        logma.info(f"[graphics] env {_k}={os.environ.get(_k)!r}")
    logma.info("Qt WebEngine environment configured for compatibility")


def setup_application_attributes() -> None:
    """
    Set Qt application attributes for better graphics compatibility
    Must be called before QApplication is created
    """
    mode = _webengine_mode()
    try:
        # REQUIRED for QtWebEngine to composite its content into Qt widgets.
        # Its absence is a classic cause of a blank/black web view; it must be
        # set before the QApplication (and any web view) is created.
        pyqt.QApplication.setAttribute(pyqt.Qt.ApplicationAttribute.AA_ShareOpenGLContexts, True)
        logma.info("[graphics] AA_ShareOpenGLContexts = True")

        # Avoid HiDPI surprises.
        pyqt.QApplication.setAttribute(pyqt.Qt.ApplicationAttribute.AA_DisableHighDpiScaling, True)

        if mode == "software":
            pyqt.QApplication.setAttribute(pyqt.Qt.ApplicationAttribute.AA_UseSoftwareOpenGL, True)
            pyqt.QApplication.setAttribute(pyqt.Qt.ApplicationAttribute.AA_UseDesktopOpenGL, False)
        else:
            # Hardware desktop OpenGL.
            pyqt.QApplication.setAttribute(pyqt.Qt.ApplicationAttribute.AA_UseSoftwareOpenGL, False)
            pyqt.QApplication.setAttribute(pyqt.Qt.ApplicationAttribute.AA_UseDesktopOpenGL, True)
        pyqt.QApplication.setAttribute(pyqt.Qt.ApplicationAttribute.AA_UseOpenGLES, False)
        logma.info(f"[graphics] application attributes configured for {mode} mode")
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
