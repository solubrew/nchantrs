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
pxcfg = {}

# def diagnose_media_support(self) -> None:
#     """Diagnose and log media codec support status."""
#     logma.info("=== Media Support Diagnostic ===")
#     # Check environment variables
#     chromium_flags = environ.get("QTWEBENGINE_CHROMIUM_FLAGS", "Not set")
#     logma.info(f"Chromium flags: {chromium_flags}")
#     ld_library_path = environ.get("LD_LIBRARY_PATH", "Not set")
#     logma.info(f"LD_LIBRARY_PATH: {ld_library_path}")
#     # Check if codec file exists
#     codec_manager = OpenH264Manager(self)
#     status = codec_manager.get_codec_status()
#     for key, value in status.items():
#         logma.info(f"Codec {key}: {value}")
#     # Platform information
#     logma.info(f"Platform: {platform.system()} {platform.release()}")
#     logma.info(f"Architecture: {platform.machine()}")
#     return status
#
# def get_codec_status(self) -> dict:
#     """Get current codec status information."""
#     from nchantrs.utilities.codec_manager import OpenH264Manager
#
#     codec_manager = OpenH264Manager(self)
#     return {
#         "available": codec_manager.is_codec_available(),
#         "library_path": codec_manager.get_library_path(),
#         "platform": platform.system(),
#         "architecture": platform.machine(),
#         "version": codec_manager.VERSION,
#         "download_url": codec_manager._get_binary_info()[0],
#         "environment_ready": self.codec_ready,
#     }
def nchantd_message_handler(mode, context, message) -> None:
    """Custom logging function for PySide6."""
    mode_name = {
        pyqt.Qt.InfoMsg: "Info",
        pyqt.Qt.WarningMsg: "Warning",
        pyqt.Qt.CriticalMsg: "Critical",
        pyqt.Qt.DebugMsg: "Debug",
    }
    print(f"{mode_name[mode]}: {message} (File: {context.file}, Line: {context.line})")


def set_default_browser() -> None:
    """"""
    if platform == "macos":
        try:
            subprocess.run(["open", "-a", "Safari"], check=True)  # Replace Safari with desired browser
            print(f"Default browser set to application: {browser_bundle_id}")
        except subprocess.CalledProcessError as e:
            print(f"Error setting default browser: {e}")
    elif platform == "linux":
        try:
            # Set default browser using xdg-settings
            subprocess.run(["xdg-settings", "set", "default-web-browser", browser_name], check=True)
            print(f"Default browser set to {browser_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error setting default browser: {e}")
    elif platform == "windows":
        try:
            key = r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, "Progid", 0, winreg.REG_SZ, browser_path)
            print(f"Default browser set to {browser_path}")
        except Exception as e:
            print(f"Failed to set default browser: {e}")

        try:
            # Set file association to the desired browser
            subprocess.run(f"assoc .html=HtmlFile", shell=True, check=True)

            # Set the ftype command to associate HTTP/HTTPS links with the browser executable
            subprocess.run(f'ftype HtmlFile="{browser_exe_path}" -- "%1"', shell=True, check=True)

            print(f"Default Browser set to: {browser_exe_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error setting default browser: {e}")


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

    def set_url(self, url) -> None:
        """"""
        if isinstance(url, pyqt.QUrl):
            url = url.toString()
        if not self.is_locked():
            self.url = url
            return True
        return False

    # def store_url(self) -> None:
    #     """"""
    #     data = [
    #         [
    #             self.url_obj.url,
    #         ]
    #     ]
    #     table = "browse_history"
    #     self.app.model._store(table, data)


class NchantdWebChannel(pyqt.QWebChannel):
    """Nchantd Web Channel controls scripting"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        self.config = condor.Instruct(pxcfg).select("NchantdWebChannel").override(cfg)
        self.parent = parent
        super().__init__()


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
