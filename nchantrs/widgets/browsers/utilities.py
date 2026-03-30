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
import platform
import subprocess

try:
    import winreg
except ImportError:
    winreg = None

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidgetMixin
from typing import Optional, Dict, List, Any, Tuple

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "utilities.yaml")


def nchantd_message_handler(mode, context, message) -> None:
    """Custom logging function for PySide6."""
    mode_name = {
        pyqt.Qt.InfoMsg: "Info",
        pyqt.Qt.WarningMsg: "Warning",
        pyqt.Qt.CriticalMsg: "Critical",
        pyqt.Qt.DebugMsg: "Debug",
    }
    logger.info(f"{mode_name[mode]}: {message} (File: {context.file}, Line: {context.line})")


def set_default_browser(
    browser_name="google-chrome", browser_path="", browser_exe_path="", browser_bundle_id="com.google.Chrome"
) -> None:
    """"""
    current_platform = platform.system().lower()
    if current_platform == "darwin":  # macos
        try:
            subprocess.run(["open", "-a", browser_name], check=True)
            logger.info(f"Default browser set to application: {browser_bundle_id}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error setting default browser: {e}")
    elif current_platform == "linux":
        try:
            # Set default browser using xdg-settings
            subprocess.run(["xdg-settings", "set", "default-web-browser", browser_name], check=True)
            logger.info(f"Default browser set to {browser_name}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error setting default browser: {e}")
    elif current_platform == "windows":
        if winreg is None:
            logger.error("winreg not available, cannot set default browser on Windows")
            return
        try:
            key = r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, "Progid", 0, winreg.REG_SZ, browser_path)
            logger.info(f"Default browser set to {browser_path}")
        except Exception as e:
            logger.error(f"Failed to set default browser: {e}")

        try:
            # Set file association to the desired browser
            subprocess.run(["assoc", ".html=HtmlFile"], check=True)

            # Set the ftype command to associate HTTP/HTTPS links with the browser executable
            subprocess.run(["ftype", f"HtmlFile={browser_exe_path}", "--", "%1"], check=True)

            logger.info(f"Default Browser set to: {browser_exe_path}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error setting default browser: {e}")


# Backend class to expose methods to JavaScript
class NchantdBackend(pyqt.QObject):
    @pyqt.Slot(result=str)
    def safeFunction(self) -> None:
        return "Safe JavaScript Call Allowed!"


class NchantdJSSafeFunction(pyqt.QWebEngineScript):
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = condor.Instruct(pxcfg).select("").override(cfg)

    def add_script(self, cmd) -> None:
        """"""
        self.sourceCode = cmd
        self.setInjectionPoint(pyqt.QWebEngineScript.DocumentReady)
        self.setWorldId(pyqt.QWebEngineScript.MainWorld)


class NchantdURL(NchantdWidgetMixin, pyqt.QUrl):
    """"""

    def __init__(self, url=None, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        super().__init__(url)
        self.config = condor.Instruct(pxcfg).select("NchantdURL")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.init_variables()
        self.lock = False
        self.url = None
        self.set_url(url)

    # def initModel(self) -> None:
    #     """"""
    #     super().initModel()
    #
    #     return self
    #
    def is_equal(self, url) -> None:
        """"""
        if self.url == url:
            return True
        return False

    def is_locked(self) -> None:
        """"""
        return self.lock

    #
    # def is_valid(self) -> None:
    #     """"""
    #     if self.document.is_valid():
    #         return True
    #     return False
    #
    # def set_lock(self) -> None:
    #     """"""
    #     self.lock = True
    #     return self
    #
    # def set_unlock(self) -> None:
    #     """"""
    #     self.lock = False
    #     return self

    def set_url(self, url) -> bool:
        """"""
        if isinstance(url, pyqt.QUrl):
            url = url.toString()
        if not self.is_locked():
            self.url = url
            return True
        return False


class NchantdWebChannel(pyqt.QWebChannel):
    """Nchantd Web Channel controls scripting"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        self.config = condor.Instruct(pxcfg).select("NchantdWebChannel").override(cfg)
        self.parent = parent
        super().__init__()


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
