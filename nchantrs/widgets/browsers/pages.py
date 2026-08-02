from typing import Any, Optional
'\n---\n<(META)>:\n    docid:\n    name:\n    description: >\n    version: 0.0.0.0.0.0\n    authority: filesystem\n    security: seclvl2\n    <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
from functools import partial
import json as j
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from subtrix.utilities import uuid
from nchantrs.libraries import pyqt
from kahndor.logma import Logma
from nchantrs.widgets.browsers.utilities import NchantdURL
from nchantrs.widgets.widgets import NchantdWidgetMixin
from nchantrs.widgets.browsers.javascript.scripts import media_pause, media_play
here = join(dirname(__file__), '')
log = False
logma = Logma(__name__)
if not log:
    logma.off()
pxcfg = join(here, '_data_', 'pages.yaml')
ENABLE_NEW_WINDOW_DELEGATION = False

class _RedirectCapturePage(pyqt.QWebEnginePage):
    """One-shot page returned from createWindow to capture a popup/new-window
    target URL and load it into an existing page instead.

    Chromium loads whatever page createWindow returns; if that page actually
    navigated it would create a second document/kernel session racing the
    original. So this page BLOCKS its own navigation (acceptNavigationRequest
    returns False), hands the URL to the target page, and self-destructs — the
    net effect is a single in-place navigation.
    """

    def __init__(self, target_page) -> None:
        super().__init__(target_page.profile(), target_page)
        self._target_page = target_page

    def acceptNavigationRequest(self, url, _type, _is_main_frame) -> bool:
        try:
            logma.info(f'[webpage] redirect-capture -> loading {url.toString()} in current view')
            self._target_page.setUrl(url)
        except Exception as e:
            logma.error(f'[webpage] redirect-capture failed: {e}')
        finally:
            self.deleteLater()
        return False

class _NewWindowCapturePage(pyqt.QWebEnginePage):
    """One-shot page returned from createWindow to capture a new-window target
    URL (target="_blank" / window.open) and hand it to a widget-supplied
    ``open_new_window(url)`` handler — e.g. "open in a new app tab, or focus the
    existing tab for this URL" — instead of spawning a detached Chromium window.

    Like _RedirectCapturePage it BLOCKS its own navigation and self-destructs, so
    Chromium does not actually load a second document; the handler decides what to
    do with the URL.
    """

    def __init__(self, source_page, on_url) -> None:
        super().__init__(source_page.profile(), source_page)
        self._on_url = on_url

    def acceptNavigationRequest(self, url, _type, _is_main_frame) -> bool:
        try:
            logma.info(f'[webpage] new-window capture -> {url.toString()}')
            self._on_url(url)
        except Exception as e:
            logma.error(f'[webpage] new-window capture handler failed: {e}')
        finally:
            self.deleteLater()
        return False

class NchantdWebEnginePage(NchantdWidgetMixin, pyqt.QWebEnginePage):
    """Custom web page with enhanced navigation handling"""
    NAVIGATION_TYPE_LINK_CLICKED = pyqt.QWebEnginePage.NavigationType.NavigationTypeLinkClicked
    JS_MESSAGE_LEVELS = {pyqt.QWebEnginePage.JavaScriptConsoleMessageLevel.InfoMessageLevel: 'Info', pyqt.QWebEnginePage.JavaScriptConsoleMessageLevel.WarningMessageLevel: 'Warning', pyqt.QWebEnginePage.JavaScriptConsoleMessageLevel.ErrorMessageLevel: 'Error'}
    navigationRequested = pyqt.Signal(pyqt.QUrl, str)
    pageLoadStarted = pyqt.Signal(pyqt.QUrl)
    pageLoadFinished = pyqt.Signal(pyqt.QUrl, bool)
    create_certificate_error_dialog = pyqt.Signal(pyqt.QWebEngineCertificateError)

    def __init__(self, profile=None, parent=None) -> None:
        super().__init__(profile, parent)

    def initModel(self, cfg=None) -> Any:
        """Initialize the model with audio and fullscreen settings."""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """Initialize view-specific connections."""
        self.setup_page()
        return self

    def initWidget(self) -> Any:
        """Initialize the complete widget by setting up model and view."""
        self.initModel()
        self.initView()
        return self

    def createStandardContextMenu(self) -> None:
        logma.info(f'createStandardContextMenu called')
        return self

    def hitTestContent(self, position) -> None:
        logma.info(f'hitTestContent called')
        return self

    def setup_page(self) -> None:
        """Initialize page settings and connections"""
        self.loadStarted.connect(self.on_load_started)
        self.loadFinished.connect(self.on_load_finished)
        self.urlChanged.connect(self.on_url_changed)
        self.titleChanged.connect(self.on_title_changed)
        self.featurePermissionRequested.connect(self.handle_feature_permission)

    def acceptNavigationRequest(self, url, navigation_type, is_main_frame) -> Any:
        """Override to handle navigation requests"""
        self._log_navigation_details(url, navigation_type, is_main_frame)
        navigation_types = {pyqt.QWebEnginePage.NavigationType.NavigationTypeLinkClicked: 'Link Clicked', pyqt.QWebEnginePage.NavigationType.NavigationTypeFormSubmitted: 'Form Submitted', pyqt.QWebEnginePage.NavigationType.NavigationTypeBackForward: 'Back/Forward', pyqt.QWebEnginePage.NavigationType.NavigationTypeReload: 'Reload', pyqt.QWebEnginePage.NavigationType.NavigationTypeRedirect: 'Redirect', pyqt.QWebEnginePage.NavigationType.NavigationTypeOther: 'Other'}
        nav_type_str = navigation_types.get(navigation_type, 'Unknown')
        logma.info(f'Navigation request: {url.toString()} - Type: {nav_type_str} - Main frame: {is_main_frame}')
        self.navigationRequested.emit(url, nav_type_str)
        self._update_frame_state(is_main_frame)
        return super().acceptNavigationRequest(url, navigation_type, is_main_frame)

    @pyqt.Slot()
    def on_load_started(self) -> None:
        """Handle page load start"""
        current_url = self.url()
        logma.info(f'Page load started: {current_url.toString()}')
        self.pageLoadStarted.emit(current_url)

    @pyqt.Slot(bool)
    def on_load_finished(self, success) -> None:
        """Handle page load completion"""
        current_url = self.url()
        status = 'successfully' if success else 'with errors'
        logma.info(f'Page loaded {status}: {current_url.toString()}')
        self.pageLoadFinished.emit(current_url, success)

    @pyqt.Slot(pyqt.QUrl)
    def on_url_changed(self, url) -> None:
        """Handle URL changes"""
        logma.info(f'URL changed to: {url.toString()}')

    @pyqt.Slot(str)
    def on_title_changed(self, title) -> None:
        """Handle title changes"""
        logma.info(f'Page title changed to: {title}')

    @pyqt.Slot(pyqt.QUrl, 'QWebEnginePage::Feature')
    def handle_feature_permission(self, url, feature) -> None:
        """Handle feature permission requests"""
        features = {pyqt.QWebEnginePage.Feature.Notifications: 'Notifications', pyqt.QWebEnginePage.Feature.Geolocation: 'Geolocation', pyqt.QWebEnginePage.Feature.MediaAudioCapture: 'Audio Capture', pyqt.QWebEnginePage.Feature.MediaVideoCapture: 'Video Capture', pyqt.QWebEnginePage.Feature.MediaAudioVideoCapture: 'Audio/Video Capture', pyqt.QWebEnginePage.Feature.MouseLock: 'Mouse Lock', pyqt.QWebEnginePage.Feature.DesktopVideoCapture: 'Desktop Video Capture', pyqt.QWebEnginePage.Feature.DesktopAudioVideoCapture: 'Desktop Audio/Video Capture'}
        feature_name = features.get(feature, 'Unknown Feature')
        logma.info(f'Feature permission requested: {feature_name} for {url.toString()}')
        self.setFeaturePermission(url, feature, pyqt.QWebEnginePage.PermissionPolicy.PermissionDeniedByUser)

    def _log_navigation_details(self, url, request_type, is_main_frame) -> None:
        """Log navigation request details for debugging."""
        logma.info(f'Navigate to {url}')
        logma.info(f'Request Type: {request_type}')
        logma.info(f'Is Main Frame: {is_main_frame}')

    def javaScriptConsoleMessage(self, level, message, line_number, source_id) -> None:
        """Handle console messages from JavaScript"""
        if message.startswith('middleClick:'):
            url = message[len('middleClick:'):]
            logma.info(f'Middle-click on link: {url}')
            if hasattr(self.parent(), 'get_available_engine'):
                new_viewer = self.parent().get_available_engine()
                new_viewer.browser.setUrl(pyqt.QUrl(url))
                if hasattr(self.parent().parent, 'add_tab'):
                    self.parent().parent.add_tab(new_viewer)
            return
        super().javaScriptConsoleMessage(level, message, line_number, source_id)

    def _resolve_new_window_target(self) -> Optional[Any]:
        """Walk the owning view/widget chain for an object exposing
        ``open_new_window(url)``.

        The chain mixes Qt parent() methods and ``self.parent`` attributes set by
        the widget framework, so at each hop we take the attribute if present
        (not callable) else call the bound parent() method. Bounded to a few hops.
        """
        node = self.parent()
        for _ in range(6):
            if node is None:
                break
            if node is not self and hasattr(node, 'open_new_window'):
                return node
            nxt = getattr(node, 'parent', None)
            if callable(nxt):
                try:
                    nxt = nxt()
                except Exception:
                    nxt = None
            node = nxt
        return None

    def createWindow(self, type_) -> Any:
        """Handle requests to create new windows (e.g. target="_blank").

        For app-style single-view embeds (the Jupyter notebook view), Jupyter
        opens a notebook via a new window/tab; there is no tab strip to receive
        it, so the request was previously dropped and double-click did nothing.
        When the owning view opts into in-place navigation we capture the
        intended URL with a throwaway page and load it into the current view.
        """
        view = self.parent()
        if hasattr(view, 'get_available_engine'):
            new_viewer = view.get_available_engine()
            return new_viewer.browser.page()
        in_place = False
        try:
            cfg = getattr(view, 'config', None)
            dikt = getattr(cfg, 'dikt', {}) if cfg is not None else {}
            in_place = bool(dikt.get('links_in_place', dikt.get('is_app', False)))
        except Exception:
            in_place = False
        if in_place:
            logma.info(f'[webpage] createWindow type={type_} in_place=True -> capture+redirect to current view')
            return _RedirectCapturePage(self)
        target = self._resolve_new_window_target() if ENABLE_NEW_WINDOW_DELEGATION else None
        if target is not None:
            logma.info(f'[webpage] createWindow type={type_} -> delegating to {type(target).__name__}.open_new_window')
            return _NewWindowCapturePage(self, target.open_new_window)
        logma.info(f'[webpage] createWindow type={type_} in_place=False -> default handling')
        return super().createWindow(type_)

    def _update_frame_state(self, is_main_frame) -> None:
        """Update internal frame state based on navigation context."""
        if not is_main_frame:
            self.is_main_frame = False

class NchantdLocalServiceWebPage(NchantdWidgetMixin, pyqt.QWebEnginePage):
    """Custom web page optimized for local development"""

    def __init__(self, profile=None, parent=None) -> None:
        super().__init__(profile, parent)
        self.setup_page()

    def setup_page(self) -> None:
        """Initialize page for local development"""
        self.settings().setAttribute(self.settings().WebAttribute.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(self.settings().WebAttribute.LocalContentCanAccessFileUrls, True)
        self.settings().setAttribute(self.settings().WebAttribute.ErrorPageEnabled, True)
        self.loadFinished.connect(self.on_load_finished)
        self.featurePermissionRequested.connect(self.handle_feature_permission)

    @pyqt.Slot(bool)
    def on_load_finished(self, success) -> None:
        """Handle page load completion for local services"""
        if not success:
            current_url = self.url()
            if self._is_local_url(current_url):
                logma.info(f'Failed to load local service: {current_url.toString()}')

    @pyqt.Slot(pyqt.QUrl, 'QWebEnginePage::Feature')
    def handle_feature_permission(self, url, feature) -> None:
        """Handle feature permissions for local development"""
        if self._is_local_url(url):
            self.setFeaturePermission(url, feature, pyqt.QWebEnginePage.PermissionPolicy.PermissionGrantedByUser)
        else:
            self.setFeaturePermission(url, feature, pyqt.QWebEnginePage.PermissionPolicy.PermissionDeniedByUser)

    def _is_local_url(self, url: pyqt.QUrl) -> bool:
        """Check if URL is for a local service"""
        host = url.host().lower()
        return host in {'localhost', '127.0.0.1', '0.0.0.0', ''}
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings, QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

class CloudflareCompatiblePage(QWebEnginePage):

    def __init__(self, profile=None, parent=None) -> None:
        super().__init__(profile, parent)
        self.setup_cloudflare_compatibility()

    def setup_cloudflare_compatibility(self) -> None:
        """Configure page settings to better handle Cloudflare challenges"""
        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowGeolocationOnInsecureOrigins, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.TouchIconsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FocusOnNavigationEnabled, True)
        settings.setDefaultTextEncoding('UTF-8')

class CloudflareCompatibleView(QWebEngineView):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.profile = self.create_enhanced_profile()
        self.custom_page = CloudflareCompatiblePage(self.profile, self)
        self.setPage(self.custom_page)
        self.page().loadFinished.connect(self.inject_cloudflare_helpers)

    def create_enhanced_profile(self) -> str:
        """Create a profile that mimics a real browser more closely"""
        profile = QWebEngineProfile.defaultProfile()
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        profile.setHttpUserAgent(user_agent)
        profile.setHttpAcceptLanguage('en-US,en;q=0.9')
        return profile

    def inject_cloudflare_helpers(self, success) -> None:
        """Inject JavaScript to help with Cloudflare challenge rendering"""
        if not success:
            return
        js_code = '\n        (function() {\n            // Ensure window properties that Cloudflare might check\n            if (!window.chrome) {\n                window.chrome = {\n                    runtime: {},\n                    loadTimes: function() { return {}; },\n                    csi: function() { return {}; }\n                };\n            }\n\n            // Ensure navigator properties\n            if (!navigator.webdriver) {\n                Object.defineProperty(navigator, \'webdriver\', {\n                    get: () => false,\n                });\n            }\n\n            // Add missing navigator properties\n            if (!navigator.plugins.length) {\n                const plugin = {\n                    description: "Portable Document Format",\n                    filename: "internal-pdf-viewer",\n                    length: 1,\n                    name: "Chrome PDF Plugin"\n                };\n                navigator.plugins[0] = plugin;\n            }\n\n            // Trigger any pending challenge callbacks\n            if (window.turnstile && window.turnstile.ready) {\n                window.turnstile.ready();\n            }\n\n            // Force challenge widget to render if present\n            setTimeout(function() {\n                const challenges = document.querySelectorAll(\'[data-sitekey]\');\n                challenges.forEach(function(challenge) {\n                    if (challenge && !challenge.innerHTML.trim()) {\n                        // Try to trigger re-render\n                        const event = new Event(\'DOMContentLoaded\');\n                        document.dispatchEvent(event);\n                    }\n                });\n            }, 2000);\n        })();\n        '
        self.page().runJavaScript(js_code)