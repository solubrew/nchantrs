from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
pxcfg = join(here, '_data_', '.yaml')
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings
from PySide6.QtCore import QUrl, pyqtSignal, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
from PySide6.QtCore import QStandardPaths
import os

class CloudflareAwareWebEnginePage(QWebEnginePage):
    """Enhanced page that handles Cloudflare challenges"""

    def __init__(self, profile, parent=None) -> None:
        super().__init__(profile, parent)
        self.challenge_timer = QTimer()
        self.challenge_timer.timeout.connect(self.check_for_challenges)

    def javaScriptConsoleMessage(self, level, message, line_number, source_id) -> None:
        """Override to handle Cloudflare-specific console messages"""
        if 'challenge-platform' in message or 'turnstile' in message.lower():
            if 'error' in message.lower():
                logma.error(f'Cloudflare Challenge Error: {message}')
            else:
                logma.debug(f'Cloudflare Challenge Info: {message}')
        elif 'was preloaded using link preload but not used' not in message:
            if level == QWebEnginePage.JavaScriptConsoleMessageLevel.ErrorMessageLevel:
                logma.error(f'JavaScript Error: {message} (Line: {line_number}, Source: {source_id})')
            elif level == QWebEnginePage.JavaScriptConsoleMessageLevel.WarningMessageLevel:
                logma.warning(f'JavaScript Warning: {message} (Line: {line_number}, Source: {source_id})')

    def check_for_challenges(self) -> None:
        """Check for and handle Cloudflare challenges"""
        js_code = "\n        (function() {\n            const challengeElements = document.querySelectorAll('[data-sitekey], .cf-browser-verification');\n            if (challengeElements.length > 0) {\n                // Try to ensure proper rendering\n                challengeElements.forEach(function(el) {\n                    el.style.visibility = 'visible';\n                    el.style.display = 'block';\n                });\n\n                // Dispatch events that might help with rendering\n                window.dispatchEvent(new Event('resize'));\n                document.dispatchEvent(new Event('DOMContentLoaded'));\n\n                return true;\n            }\n            return false;\n        })();\n        "
        self.runJavaScript(js_code)

class PersistentGoogleSession:
    """Manage persistent Google login sessions with Cloudflare handling."""

    def __init__(self, app_name='your_app') -> None:
        self.app_name = app_name
        self.profile = None
        self.setup_persistent_profile()

    def setup_persistent_profile(self) -> Any:
        """Create a persistent web profile for storing login data."""
        data_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        profile_path = os.path.join(data_path, 'WebProfile')
        self.profile = QWebEngineProfile(self.app_name)
        self.profile.setPersistentStoragePath(profile_path)
        settings = self.profile.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        self.profile.setHttpUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        self.profile.setHttpAcceptLanguage('en-US,en;q=0.9')
        return self.profile

    def create_web_view(self, parent=None) -> Any:
        """Create a QWebEngineView with persistent session and Cloudflare handling."""
        from PySide6.QtWebEngineWidgets import QWebEngineView
        page = CloudflareAwareWebEnginePage(self.profile, parent)
        web_view = QWebEngineView(parent)
        web_view.setPage(page)
        page.loadFinished.connect(lambda success: self._handle_page_load(page, success))
        return web_view

    def _handle_page_load(self, page, success) -> None:
        """Handle page load and check for Cloudflare challenges"""
        if success:
            page.challenge_timer.start(2000)
            js_code = "\n            (function() {\n                // Help with Cloudflare challenge rendering\n                setTimeout(function() {\n                    const challenges = document.querySelectorAll('[data-sitekey]');\n                    if (challenges.length > 0) {\n                        console.log('Cloudflare Turnstile widget detected, ensuring visibility...');\n                        challenges.forEach(function(widget) {\n                            widget.style.minHeight = '65px';\n                            widget.style.width = '300px';\n                            widget.style.display = 'block';\n                            widget.style.visibility = 'visible';\n                        });\n\n                        // Try to trigger Turnstile re-render\n                        if (window.turnstile && window.turnstile.ready) {\n                            window.turnstile.ready();\n                        }\n                    }\n                }, 1000);\n            })();\n            "
            page.runJavaScript(js_code)

class NchantdGoogleDriveWidget(QWidget):
    """Enhanced Google Drive widget with persistent login."""
    file_selected = pyqtSignal(str)
    login_status_changed = pyqtSignal(bool)

    def __init__(self, parent=None, cfg=None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.config = cfg or {}
        self.session_manager = PersistentGoogleSession('nchantd_office')
        self.setup_ui()
        self.setup_login_detection()
        logma.info(f'NchantdGoogleDriveWidget initialized')

    def setup_ui(self) -> None:
        """Setup the user interface."""
        layout = QVBoxLayout(self)
        self.web_view = self.session_manager.create_web_view(self)
        layout.addWidget(self.web_view)
        self.setup_google_specific_settings()
        self.load_google_drive()

    def setup_google_specific_settings(self) -> None:
        """Configure settings specifically for Google services."""
        profile = self.web_view.page().profile()
        profile.setHttpAcceptLanguage('en-US,en;q=0.9')
        settings = self.web_view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanPaste, True)
        self.web_view.page().newWindowRequested.connect(self.handle_new_window)

    def check_auth_completion(self, url, popup_dialog) -> None:
        """Check if authentication is complete."""
        url_string = url.toString()
        if 'accounts.google.com' not in url_string and 'drive.google.com' in url_string:
            popup_dialog.close()
            self.web_view.reload()

    def setup_login_detection(self) -> None:
        """Setup automatic login status detection."""
        self.login_check_timer = QTimer()
        self.login_check_timer.timeout.connect(self.check_login_status)
        self.login_check_timer.start(5000)

    def check_login_status(self) -> None:
        """Check if user is logged into Google."""
        js_code = '\n        (function() {\n            // Check for Google account indicators\n            const accountButton = document.querySelector(\'[data-ogsr-up]\') || \n                                document.querySelector(\'.gb_A\') ||\n                                document.querySelector(\'[aria-label*="Account"]\');\n\n            const isLoggedIn = accountButton !== null;\n\n            return {\n                logged_in: isLoggedIn,\n                account_element: accountButton ? accountButton.getAttribute(\'aria-label\') : null,\n                current_url: window.location.href\n            };\n        })();\n        '
        self.web_view.page().runJavaScript(js_code, self.handle_login_status)

    def handle_login_status(self, result) -> None:
        """Handle login status check result."""
        if result and isinstance(result, dict):
            is_logged_in = result.get('logged_in', False)
            self.login_status_changed.emit(is_logged_in)
            if is_logged_in:
                logger.info('User logged in: %s', result.get('account_element', 'Unknown'))
            else:
                logger.info('User not logged in to Google')

    def load_google_drive(self) -> None:
        """Load Google Drive."""
        drive_url = 'https://drive.google.com'
        self.web_view.load(QUrl(drive_url))

    def force_login(self) -> None:
        """Force Google login page."""
        login_url = 'https://accounts.google.com/signin'
        self.web_view.load(QUrl(login_url))

    def clear_session(self) -> None:
        """Clear stored session data."""
        profile = self.web_view.page().profile()
        profile.clearHttpCache()
        cookie_store = profile.cookieStore()
        cookie_store.deleteAllCookies()
        logger.info('Session data cleared')

    def get_cookies(self) -> None:
        """Get current cookies (for debugging)."""
        profile = self.web_view.page().profile()
        cookie_store = profile.cookieStore()

        def cookie_added(cookie) -> None:
            logger.debug('Cookie: %s = %s', cookie.name(), cookie.value())
        cookie_store.cookieAdded.connect(cookie_added)
        js_code = 'document.cookie;'
        self.web_view.page().runJavaScript(js_code)