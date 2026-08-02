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
from os.path import abspath, dirname, join
import datetime as dt
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from kahndor.logma import Logma
from typing import Optional, Dict, List, Any, Tuple
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
from PySide6.QtCore import QStandardPaths
import os

class PersistentGoogleSession:
    """Manage persistent Google login sessions."""

    def __init__(self, app_name='your_app') -> None:
        self.app_name = app_name
        self.profile = None
        self.setup_persistent_profile()

    def setup_persistent_profile(self) -> None:
        """Create a persistent web profile for storing login data."""
        data_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        profile_path = os.path.join(data_path, 'WebProfile')
        self.profile = QWebEngineProfile(self.app_name)
        self.profile.setPersistentStoragePath(profile_path)
        settings = self.profile.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        self.profile.setHttpUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        return self.profile

    def create_web_view(self, parent=None) -> None:
        """Create a QWebEngineView with persistent session."""
        from PySide6.QtWebEngineWidgets import QWebEngineView
        from PySide6.QtWebEngineCore import QWebEnginePage
        page = QWebEnginePage(self.profile, parent)
        web_view = QWebEngineView(parent)
        web_view.setPage(page)
        return web_view