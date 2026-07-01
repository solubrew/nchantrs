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
from functools import partial
import json as j

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from subtrix.utilities import uuid
from nchantrs.libraries import pyqt
from kahndor.logma import Logma
from nchantrs.widgets.browsers.utilities import NchantdURL
from nchantrs.widgets.widgets import NchantdWidgetMixin
from nchantrs.widgets.browsers.javascript.scripts import media_pause, media_play

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
# logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "pages.yaml")


class NchantdWebEnginePage(NchantdWidgetMixin, pyqt.QWebEnginePage):
    """Custom web page with enhanced navigation handling"""

    # Navigation type constants
    NAVIGATION_TYPE_LINK_CLICKED = pyqt.QWebEnginePage.NavigationType.NavigationTypeLinkClicked
    # JavaScript console message level mapping
    JS_MESSAGE_LEVELS = {
        pyqt.QWebEnginePage.JavaScriptConsoleMessageLevel.InfoMessageLevel: "Info",
        pyqt.QWebEnginePage.JavaScriptConsoleMessageLevel.WarningMessageLevel: "Warning",
        pyqt.QWebEnginePage.JavaScriptConsoleMessageLevel.ErrorMessageLevel: "Error",
    }
    # Custom signals
    navigationRequested = pyqt.Signal(pyqt.QUrl, str)  # url, navigation_type
    pageLoadStarted = pyqt.Signal(pyqt.QUrl)
    pageLoadFinished = pyqt.Signal(pyqt.QUrl, bool)  # url, success
    create_certificate_error_dialog = pyqt.Signal(pyqt.QWebEngineCertificateError)

    def __init__(self, profile=None, parent=None):
        super().__init__(profile, parent)

    def initModel(self, cfg=None):
        """Initialize the model with audio and fullscreen settings."""
        super().initModel(cfg)
        # self.setAudioMuted(True)
        # self.fullScreenRequested.connect(self._on_fullscreen_requested)
        # self.featurePermissionRequested.connect(self._on_feature_permission)
        return self

    def initView(self, cfg=None):
        """Initialize view-specific connections."""
        # self.profile.downloadRequested.connect(self.handle_download)
        self.setup_page()
        return self

    def initWidget(self):
        """Initialize the complete widget by setting up model and view."""
        self.initModel()
        self.initView()
        return self

    def setup_page(self):
        """Initialize page settings and connections"""
        # Connect built-in signals
        self.loadStarted.connect(self.on_load_started)
        self.loadFinished.connect(self.on_load_finished)
        self.urlChanged.connect(self.on_url_changed)
        self.titleChanged.connect(self.on_title_changed)

        # Handle feature permissions
        self.featurePermissionRequested.connect(self.handle_feature_permission)

    def acceptNavigationRequest(self, url, navigation_type, is_main_frame):
        """Override to handle navigation requests"""
        self._log_navigation_details(url, navigation_type, is_main_frame)
        # if request_type == self.NAVIGATION_TYPE_LINK_CLICKED:
        #     if not self._handle_mouse_clicks(url):
        #         return False
        # url = NchantdURL(url)
        # logma.info(f"Navigate to {url}")
        navigation_types = {
            pyqt.QWebEnginePage.NavigationType.NavigationTypeLinkClicked: "Link Clicked",
            pyqt.QWebEnginePage.NavigationType.NavigationTypeFormSubmitted: "Form Submitted",
            pyqt.QWebEnginePage.NavigationType.NavigationTypeBackForward: "Back/Forward",
            pyqt.QWebEnginePage.NavigationType.NavigationTypeReload: "Reload",
            pyqt.QWebEnginePage.NavigationType.NavigationTypeRedirect: "Redirect",
            pyqt.QWebEnginePage.NavigationType.NavigationTypeOther: "Other",
        }
        nav_type_str = navigation_types.get(navigation_type, "Unknown")
        logma.info(f"Navigation request: {url.toString()} - Type: {nav_type_str} - Main frame: {is_main_frame}")
        # Emit custom signal
        self.navigationRequested.emit(url, nav_type_str)
        self._update_frame_state(is_main_frame)
        # Call parent implementation
        return super().acceptNavigationRequest(url, navigation_type, is_main_frame)

    @pyqt.Slot()
    def on_load_started(self):
        """Handle page load start"""
        current_url = self.url()
        logma.info(f"Page load started: {current_url.toString()}")
        self.pageLoadStarted.emit(current_url)

    @pyqt.Slot(bool)
    def on_load_finished(self, success):
        """Handle page load completion"""
        current_url = self.url()
        status = "successfully" if success else "with errors"
        logma.info(f"Page loaded {status}: {current_url.toString()}")
        self.pageLoadFinished.emit(current_url, success)

    @pyqt.Slot(pyqt.QUrl)
    def on_url_changed(self, url):
        """Handle URL changes"""
        logma.info(f"URL changed to: {url.toString()}")

    @pyqt.Slot(str)
    def on_title_changed(self, title):
        """Handle title changes"""
        logma.info(f"Page title changed to: {title}")

    @pyqt.Slot(pyqt.QUrl, "QWebEnginePage::Feature")
    def handle_feature_permission(self, url, feature):
        """Handle feature permission requests"""
        features = {
            pyqt.QWebEnginePage.Feature.Notifications: "Notifications",
            pyqt.QWebEnginePage.Feature.Geolocation: "Geolocation",
            pyqt.QWebEnginePage.Feature.MediaAudioCapture: "Audio Capture",
            pyqt.QWebEnginePage.Feature.MediaVideoCapture: "Video Capture",
            pyqt.QWebEnginePage.Feature.MediaAudioVideoCapture: "Audio/Video Capture",
            pyqt.QWebEnginePage.Feature.MouseLock: "Mouse Lock",
            pyqt.QWebEnginePage.Feature.DesktopVideoCapture: "Desktop Video Capture",
            pyqt.QWebEnginePage.Feature.DesktopAudioVideoCapture: "Desktop Audio/Video Capture",
        }
        feature_name = features.get(feature, "Unknown Feature")
        logma.info(f"Feature permission requested: {feature_name} for {url.toString()}")
        # Grant or deny permission (customize as needed)
        self.setFeaturePermission(url, feature, pyqt.QWebEnginePage.PermissionPolicy.PermissionDeniedByUser)

    def _log_navigation_details(self, url, request_type, is_main_frame):
        """Log navigation request details for debugging."""
        logma.info(f"Navigate to {url}")
        logma.info(f"Request Type: {request_type}")
        logma.info(f"Is Main Frame: {is_main_frame}")

    def javaScriptConsoleMessage(self, level, message, line_number, source_id):
        """Handle console messages from JavaScript"""
        if message.startswith("middleClick:"):
            url = message[len("middleClick:") :]
            logma.info(f"Middle-click on link: {url}")
            # Try to use parent manager to open a new tab if available
            if hasattr(self.parent(), "get_available_engine"):
                new_viewer = self.parent().get_available_engine()
                new_viewer.browser.setUrl(pyqt.QUrl(url))
                # Add to UI - usually the parent of NchantdWebManager would be the application/window
                if hasattr(self.parent().parent, "add_tab"):
                    self.parent().parent.add_tab(new_viewer)
            return

        # logma.debug(f"JS Console message: {message}")
        super().javaScriptConsoleMessage(level, message, line_number, source_id)

    def createWindow(self, type_):
        """Handle requests to create new windows (e.g. target="_blank").

        For app-style single-view embeds (the Jupyter notebook view), Jupyter
        opens a notebook via a new window/tab; there is no tab strip to receive
        it, so the request was previously dropped and double-click did nothing.
        When the owning view opts into in-place navigation we capture the
        intended URL with a throwaway page and load it into the current view.
        """
        view = self.parent()

        # A tabbed browser can still hand new windows to a pooled engine.
        if hasattr(view, "get_available_engine"):
            new_viewer = view.get_available_engine()
            return new_viewer.browser.page()

        # Decide whether new-window requests should open in this same view.
        in_place = False
        try:
            cfg = getattr(view, "config", None)
            dikt = getattr(cfg, "dikt", {}) if cfg is not None else {}
            in_place = bool(dikt.get("links_in_place", dikt.get("is_app", False)))
        except Exception:
            in_place = False

        if in_place:
            logma.info(f"[webpage] createWindow type={type_} in_place=True -> redirecting to current view")
            # Throwaway page captures the target URL, then we load it in-place.
            temp = pyqt.QWebEnginePage(self.profile(), self)

            def _redirect(url, _temp=temp):
                logma.info(f"[webpage] createWindow redirect -> loading {url.toString()} in current view")
                self.setUrl(url)
                _temp.deleteLater()

            temp.urlChanged.connect(_redirect)
            return temp

        logma.info(f"[webpage] createWindow type={type_} in_place=False -> default handling")
        return super().createWindow(type_)

    def _update_frame_state(self, is_main_frame):
        """Update internal frame state based on navigation context."""
        if not is_main_frame:
            self.is_main_frame = False


class NchantdLocalServiceWebPage(NchantdWidgetMixin, pyqt.QWebEnginePage):
    """Custom web page optimized for local development"""

    def __init__(self, profile=None, parent=None):
        super().__init__(profile, parent)
        self.setup_page()

    def setup_page(self):
        """Initialize page for local development"""
        # Enable development features
        self.settings().setAttribute(self.settings().WebAttribute.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(self.settings().WebAttribute.LocalContentCanAccessFileUrls, True)
        self.settings().setAttribute(self.settings().WebAttribute.ErrorPageEnabled, True)

        # Connect signals
        self.loadFinished.connect(self.on_load_finished)
        self.featurePermissionRequested.connect(self.handle_feature_permission)

    @pyqt.Slot(bool)
    def on_load_finished(self, success):
        """Handle page load completion for local services"""
        if not success:
            current_url = self.url()
            if self._is_local_url(current_url):
                logma.info(f"Failed to load local service: {current_url.toString()}")
                # Could inject custom error page or retry logic

    @pyqt.Slot(pyqt.QUrl, "QWebEnginePage::Feature")
    def handle_feature_permission(self, url, feature):
        """Handle feature permissions for local development"""
        if self._is_local_url(url):
            # Be more permissive with local services for development
            self.setFeaturePermission(url, feature, pyqt.QWebEnginePage.PermissionPolicy.PermissionGrantedByUser)
        else:
            self.setFeaturePermission(url, feature, pyqt.QWebEnginePage.PermissionPolicy.PermissionDeniedByUser)

    def _is_local_url(self, url: pyqt.QUrl) -> bool:
        """Check if URL is for a local service"""
        host = url.host().lower()
        return host in {"localhost", "127.0.0.1", "0.0.0.0", ""}


from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings, QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl


class CloudflareCompatiblePage(QWebEnginePage):
    def __init__(self, profile=None, parent=None):
        super().__init__(profile, parent)
        self.setup_cloudflare_compatibility()

    def setup_cloudflare_compatibility(self):
        """Configure page settings to better handle Cloudflare challenges"""
        settings = self.settings()

        # Essential settings for Cloudflare compatibility
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowGeolocationOnInsecureOrigins, False)

        # Enable features that Cloudflare might check for
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.TouchIconsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FocusOnNavigationEnabled, True)

        # Set realistic browser viewport
        settings.setDefaultTextEncoding("UTF-8")


class CloudflareCompatibleView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create enhanced profile
        self.profile = self.create_enhanced_profile()

        # Create page with enhanced settings
        self.custom_page = CloudflareCompatiblePage(self.profile, self)
        self.setPage(self.custom_page)

        # Inject JavaScript to help with challenge detection
        self.page().loadFinished.connect(self.inject_cloudflare_helpers)

    def create_enhanced_profile(self):
        """Create a profile that mimics a real browser more closely"""
        profile = QWebEngineProfile.defaultProfile()

        # Set a realistic user agent that includes all necessary browser features
        user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        profile.setHttpUserAgent(user_agent)

        # Set additional HTTP headers
        profile.setHttpAcceptLanguage("en-US,en;q=0.9")

        return profile

    def inject_cloudflare_helpers(self, success):
        """Inject JavaScript to help with Cloudflare challenge rendering"""
        if not success:
            return

        js_code = """
        (function() {
            // Ensure window properties that Cloudflare might check
            if (!window.chrome) {
                window.chrome = {
                    runtime: {},
                    loadTimes: function() { return {}; },
                    csi: function() { return {}; }
                };
            }

            // Ensure navigator properties
            if (!navigator.webdriver) {
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => false,
                });
            }

            // Add missing navigator properties
            if (!navigator.plugins.length) {
                const plugin = {
                    description: "Portable Document Format",
                    filename: "internal-pdf-viewer",
                    length: 1,
                    name: "Chrome PDF Plugin"
                };
                navigator.plugins[0] = plugin;
            }

            // Trigger any pending challenge callbacks
            if (window.turnstile && window.turnstile.ready) {
                window.turnstile.ready();
            }

            // Force challenge widget to render if present
            setTimeout(function() {
                const challenges = document.querySelectorAll('[data-sitekey]');
                challenges.forEach(function(challenge) {
                    if (challenge && !challenge.innerHTML.trim()) {
                        // Try to trigger re-render
                        const event = new Event('DOMContentLoaded');
                        document.dispatchEvent(event);
                    }
                });
            }, 2000);
        })();
        """

        self.page().runJavaScript(js_code)


# class NchantdWebPage(NchantdWidgetMixin, pyqt.QWebEnginePage):
#     """A custom web page implementation with enhanced navigation and security features."""
#
#     create_certificate_error_dialog = pyqt.Signal(pyqt.QWebEngineCertificateError)
#
#     # Navigation type constants
#     NAVIGATION_TYPE_LINK_CLICKED = pyqt.QWebEnginePage.NavigationTypeLinkClicked
#
#     # JavaScript console message level mapping
#     JS_MESSAGE_LEVELS = {
#         pyqt.QWebEnginePage.JavaScriptConsoleMessageLevel.InfoMessageLevel: "Info",
#         pyqt.QWebEnginePage.JavaScriptConsoleMessageLevel.WarningMessageLevel: "Warning",
#         pyqt.QWebEnginePage.JavaScriptConsoleMessageLevel.ErrorMessageLevel: "Error",
#     }
#
#     def __init__(self, parent=None, profile=None, intercept=False, cfg=None):
#         """Initialize the web page with configuration and event handlers."""
#         if profile is None:
#             profile = self.parent.default_profile
#         super().__init__(profile, parent)
#         self.parent = parent
#         self.profile = profile
#         self.config = kahndor.Instruct(pxcfg).select("NchantdWebPage")
#         self.config.override(cfg)
#         self.selectClientCertificate.connect(self.handle_select_client_certificate)
#         self.certificateError.connect(self.handle_certificate_error)
#         self.is_main_frame = True
#         self.view = None
#
#     def initModel(self, cfg=None):
#         """Initialize the model with audio and fullscreen settings."""
#         super().initModel(cfg)
#         self.setAudioMuted(True)
#         self.fullScreenRequested.connect(self._on_fullscreen_requested)
#         self.featurePermissionRequested.connect(self._on_feature_permission)
#         return self
#
#     def initView(self, cfg=None):
#         """Initialize view-specific connections."""
#         self.profile.downloadRequested.connect(self.handle_download)
#         return self
#
#     def initWidget(self):
#         """Initialize the complete widget by setting up model and view."""
#         self.initModel()
#         self.initView()
#         return self
#
#     def acceptNavigationRequest(self, url, request_type, is_main_frame):
#         """Handle navigation requests with mouse click detection and frame tracking."""
#         self._log_navigation_details(url, request_type, is_main_frame)
#
#         if request_type == self.NAVIGATION_TYPE_LINK_CLICKED:
#             if not self._handle_mouse_clicks(url):
#                 return False
#
#         self._update_frame_state(is_main_frame)
#         url = NchantdURL(url)
#         logma.info(f"Navigate to {url}")
#         return super().acceptNavigationRequest(url, request_type, is_main_frame)
#
#     def certificateError(self, certificateError: pyqt.QWebEngineCertificateError):
#         """Handle SSL certificate errors by automatically ignoring them."""
#         logma.info(f"Certificate Error: {certificateError.errorDescription()}")
#         certificateError.ignoreCertificateError()
#         return True
#
#     def createWindow(self, window_type):
#         """Handle window creation requests."""
#         return self
#
#     def featurePermissionRequested(self, url, feature):
#         """Handle feature permission requests from web content."""
#         logma.info(f"Feature Permission Requested: {feature} for {url.toString()}")
#
#     def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):
#         """Process JavaScript console messages and handle click events."""
#         if self._handle_javascript_click_events(msg):
#             return self
#
#         formatted_msg = self._format_console_message(level, msg, linenumber, source_id)
#         logma.warning(formatted_msg)
#         return self
#
#     def handle_certificate_error(self, error):
#         """Handle certificate errors with deferred dialog creation."""
#         error.defer()
#         pyqt.QTimer.singleShot(0, partial(self._emit_create_certificate_error_dialog, error))
#
#     def handle_download(self, download: pyqt.QWebEngineDownloadRequest):
#         """Handle file downloads with user-selected save location."""
#         path, _ = pyqt.QFileDialog.getSaveFileName(self.view, "Save video as", download.suggestedFileName())
#         if not path:
#             return
#         download.setDownloadDirectory(path)
#         download.setDownloadFileName(path)
#         download.accept()
#
#         self._setup_download_monitoring(download, path)
#         return self
#
#     def handle_select_client_certificate(self, selection):
#         """Select the first available client certificate."""
#         selection.select(selection.certificates()[0])
#         return self
#
#     def hard_stop(self):
#         """Stop all media and clear the page."""
#         self.runJavaScript(media_pause())
#         self.setAudioMuted(True)
#         self.setUrl(pyqt.QUrl("about:blank"))
#         return self
#
#     def onLeftClick(self, event, msg=None):
#         """Handle left mouse click events."""
#         logma.info(f"onLeftClick: {event}")
#         super().onLeftClick(event)
#         if event:
#             pos = event.position().toPoint()
#             self.page().hitTestContent(pos).then(self.goto_page)
#         return self
#
#     def onMiddleClick(self, event, msg=None):
#         """Handle middle mouse click events to open new tabs."""
#         logma.info(f"onMiddleClick: {event}")
#         super().onMiddleClick(event)
#         if event:
#             pos = event.position().toPoint()
#             self.page().hitTestContent(pos).then(self.open_new_tab)
#         return self
#
#     def open_new_tab(self, signal, *args, **kwargs):
#         """Open a new tab with the specified configuration."""
#         cfg = args[0]["action"].action
#         if isinstance(cfg["parameters_dict"], str):
#             cfg["parameters_dict"] = j.loads(cfg["parameters_dict"].replace("'", '"'))
#         tcfg = self._build_tab_config(cfg)
#         params = cfg["parameters_dict"]
#         tab_data = [
#             tcfg,
#             tcfg["did"],
#             tcfg["pid"],
#             tcfg["position"],
#             tcfg["widget"],
#             params,
#             tcfg["type"],
#             "center",
#             "db",
#             True,
#         ]
#         self.app.model.add_tab(tab_data)
#         self._update_ui_after_tab_creation(tcfg["position"])
#         return self
#
#     def pause_and_mute(self):
#         """Pause media playback and mute audio."""
#         self.setAudioMuted(True)
#         self.runJavaScript(media_pause())
#         self._set_lifecycle_state_if_supported("Frozen")
#         return self
#
#     def resume_and_unmute(self):
#         """Resume media playback and unmute audio."""
#         self._set_lifecycle_state_if_supported("Active")
#         self.setAudioMuted(False)
#         self.runJavaScript(media_play())
#         return self
#
#     def show_cookies(self):
#         """Display cookies for the current page."""
#         cookie_store = self.profile.cookieStore()
#
#         def handle_cookie(cookie):
#             logma.info(f"Cookie Name: {cookie.name().data().decode()}")
#             logma.info(f"Cookie Value: {cookie.value().data().decode()}")
#
#         cookie_store.cookiesForUrl(self.web_view.url(), handle_cookie)
#
#     def unsupportedContent(self, reply):
#         """Handle unsupported content by downloading it."""
#         logma.info(f"Unsupported content: {reply.url().toString()}")
#         reply.download()
#
#     def _build_tab_config(self, cfg):
#         """Build tab configuration dictionary."""
#         pid = self.app.view.panes["left"].tree.model.current_node.nid
#         pos = len(self.app.view.panes["center"].model.tabsdata)
#         code = cfg["lookup_code_txt"][-len(cfg["lookup_code_txt"]) + cfg["lookup_code_txt"].rfind("_") + 1 :]
#         did = uuid()
#         name = f"{code.lower().replace(' ', '')} {did[-5:]}"
#         widget = cfg["widget_txt"]
#
#         return {
#             "name": name,
#             "widget": widget,
#             "type": cfg["lookup_code_txt"],
#             "did": did,
#             "pid": pid,
#             "tid": uuid(),
#             "position": pos,
#             "tabset": "center",
#             "context": "",
#             "version": 0,
#             "hash": "",
#             "policy_fk": None,
#             "content": {},
#             "syntax": "",
#         }
#
#     def _handle_javascript_click_events(self, msg):
#         """Handle click events triggered from JavaScript."""
#         click_handlers = {
#             "middleClick:": self.onMiddleClick,
#             "leftClick:": self.onLeftClick,
#             "rightClick:": self.onRightClick,
#             "doubleLeftClick:": self.onLeftDoubleClick,
#         }
#
#         for click_type, handler in click_handlers.items():
#             if click_type in msg:
#                 handler(None, msg)
#                 return True
#         return False
#
#     def _format_console_message(self, level, msg, linenumber, source_id):
#         """Format JavaScript console message for logging."""
#         level_name = self.JS_MESSAGE_LEVELS.get(level, "Unknown")
#         return f"JavaScript {level_name}: {msg} (Line: {linenumber}, Source: {source_id})"
#
#     def _update_frame_state(self, is_main_frame):
#         """Update internal frame state based on navigation context."""
#         if not is_main_frame:
#             self.is_main_frame = False
#
#     def _update_ui_after_tab_creation(self, position):
#         """Update UI elements after creating a new tab."""
#         self.app.view.panes["left"].tree.model.current_node.updateTabs("center")
#         self.app.view.panes["center"].setCurrentIndex(position)
#
#     def _set_lifecycle_state_if_supported(self, state):
#         """Set lifecycle state if the feature is supported."""
#         if hasattr(pyqt.QWebEnginePage, "LifecycleState"):
#             try:
#                 state_attr = getattr(pyqt.QWebEnginePage.LifecycleState, state)
#                 self.setLifecycleState(state_attr)
#             except (AttributeError, Exception):
#                 pass
#
#     def _setup_download_monitoring(self, download, path):
#         """Setup progress monitoring for downloads."""
#         download.downloadProgress.connect(lambda recvd, total: logma.info(f"Progress: {recvd}/{total} bytes"))
#         download.finished.connect(lambda: logma.info(f"Download finished: {path}"))
#
#     def _log_navigation_details(self, url, request_type, is_main_frame):
#         """Log navigation request details for debugging."""
#         logma.info(f"Navigate to {url}")
#         logma.info(f"Request Type: {request_type}")
#         logma.info(f"Is Main Frame: {is_main_frame}")
#
#     def _handle_mouse_clicks(self, url):
#         """Handle different mouse click types for navigation requests."""
#         logma.info(f"Button {pyqt.QApplication.mouseButtons()} pressed")
#
#         mouse_button = pyqt.QApplication.mouseButtons()
#         if mouse_button == pyqt.Qt.MiddleButton:
#             self.onMiddleClick(event)
#             logma.info(f"Middle-click detected on: {url}")
#             return False  # Prevent navigation in current view
#         elif mouse_button == pyqt.Qt.LeftButton:
#             self.onLeftClick(event)
#
#         return True
#
#     def _emit_create_certificate_error_dialog(self, error):
#         """Emit signal to create certificate error dialog."""
#         self.create_certificate_error_dialog.emit(error)
#
#     def _on_fullscreen_requested(self, request):
#         """Handle fullscreen requests."""
#         request.accept()
#
#     def _on_feature_permission(self, url, feature):
#         """Handle feature permission requests by denying them by default."""
#         self.setFeaturePermission(url, feature, pyqt.QWebEnginePage.PermissionPolicy.PermissionDeniedByUser)


# class NchantdWebPage(NchantdWidgetMixin, pyqt.QWebEnginePage):
#     """"""
#
#     create_certificate_error_dialog = pyqt.Signal(pyqt.QWebEngineCertificateError)
#
#     def __init__(self, parent=None, profile=None, intercept=False, cfg=None):
#         """"""
#         if profile is None:
#             profile = self.parent.default_profile
#         super().__init__(profile, parent)
#         self.parent = parent
#         self.profile = profile
#         self.config = kahndor.Instruct(pxcfg).select("NchantdWebPage")
#         self.config.override(cfg)
#         self.selectClientCertificate.connect(self.handle_select_client_certificate)
#         self.certificateError.connect(self.handle_certificate_error)
#         self.is_main_frame = True
#         self.view = None
#
#     def initModel(self, cfg=None):
#         """"""
#         super().initModel(cfg)
#         self.setAudioMuted(True)
#         # self.setZoomFactor(1.0)
#         self.fullScreenRequested.connect(self._on_fullscreen_requested)
#         self.featurePermissionRequested.connect(self._on_feature_permission)
#         return self
#
#     def initView(self, cfg=None):
#         """"""
#         self.profile.downloadRequested.connect(self.handle_download)
#         return self
#
#     def initWidget(self):
#         """"""
#         self.initModel()
#         self.initView()
#         return self
#
#     def acceptNavigationRequest(self, url, request_type, is_main_frame):
#         """
#
#         Request Tyeps:
#             NavigationType.NavigationTypeFormSubmitted
#             NavigationType.NavigationTypeOther
#             NavigationType.NavigationTypeRedirect
#             NavigationType.NavigationTypeLinkClicked
#
#
#         :param url:
#         :param request_type:
#         :param is_main_frame:
#         :return:
#         """
#         logma.info(f"Navigate to {url}")
#         logma.info(f"Request Type: {request_type}")
#         logma.info(f"Is Main Frame: {is_main_frame}")
#         if request_type == pyqt.QWebEnginePage.NavigationTypeLinkClicked:
#             logma.info(f"Button {pyqt.QApplication.mouseButtons()} pressed")
#             if pyqt.QApplication.mouseButtons() == pyqt.Qt.MiddleButton:
#                 self.onMiddleClick(event)
#                 logma.info(f"Middle-click detected on: {url}")
#                 # Call parent's method to open a new tab for middle-clicked links
#                 # self.parent.open_new_tab(url)  # Custom method in the parent
#                 return False  # Prevent the current view from navigating
#             elif pyqt.QApplication.mouseButtons() == pyqt.Qt.LeftButton:
#                 self.onLeftClick(event)
#         state = "change_page"
#         if not is_main_frame:
#             state = "pull_resources"
#             self.is_main_frame = False
#         url = NchantdURL(url)
#         logma.info(f"Navigate to {url}")
#         return super().acceptNavigationRequest(url, request_type, is_main_frame)
#
#     def certificateError(self, certificateError: pyqt.QWebEngineCertificateError):
#         logma.info(f"Certificate Error: {certificateError.errorDescription()}")
#
#         # Automatically ignore the certificate error (not recommended for production)
#         certificateError.ignoreCertificateError()
#         return True
#
#     def createWindow(self, window_type):
#         """"""
#
#         return self
#
#     def featurePermissionRequested(self, url, feature):
#         """"""
#         logma.info(f"Feature Permission Requested: {feature} for {url.toString()}")
#         # Grant permission for specific features
#         # if feature == pyqt.QWebEnginePage.Geolocation:
#         #     # ask user
#         #     self.setFeaturePermission(url, feature, pyqt.QWebEnginePage.PermissionGrantedByUser)
#         #     return self
#         # elif feature == pyqt.QWebEnginePage.Notifications:
#         #     self.setFeaturePermission(url, feature, pyqt.QWebEnginePage.PermissionGrantedByUser)
#         #     return self
#         # elif feature == pyqt.QWebEnginePage.MediaAudioCapture:
#         #     # ask user
#         #     self.setFeaturePermission(url, feature, pyqt.QWebEnginePage.PermissionGrantedByUser)
#         #     return self
#         # elif feature == pyqt.QWebEnginePage.MediaVideoCapture:
#         #     # ask user
#         #     self.setFeaturePermission(url, feature, pyqt.QWebEnginePage.PermissionGrantedByUser)
#         #     return self
#         # elif feature == pyqt.QWebEnginePage.MediaAudioVideoCapture:
#         #     # ask user
#         #     self.setFeaturePermission(url, feature, pyqt.QWebEnginePage.PermissionGrantedByUser)
#         #     return self
#         # elif feature == pyqt.QWebEnginePage.DesktopAudioVideoCapture:
#         #     # ask user
#         #     self.setFeaturePermission(url, feature, pyqt.QWebEnginePage.PermissionGrantedByUser)
#         #     return self
#         # elif feature == pyqt.QWebEnginePage.MouseLock:
#         #     # ask user
#         #     self.setFeaturePermission(url, feature, pyqt.QWebEnginePage.PermissionGrantedByUser)
#         #     return self
#         # self.setFeaturePermission(url, feature, pyqt.QWebEnginePage.PermissionDeniedByUser)
#         # return self
#
#     def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):
#         """"""
#         levels = {
#             pyqt.QWebEnginePage.InfoMessageLevel: "Info",
#             pyqt.QWebEnginePage.WarningMessageLevel: "Warning",
#             pyqt.QWebEnginePage.ErrorMessageLevel: "Error",
#         }
#         event = None
#         if "middleClick:" in msg:  # Check if the message indicates a middle click
#             self.onMiddleClick(event, msg)
#         elif "leftClick:" in msg:
#             self.onLeftClick(event, msg)
#         elif "rightClick:" in msg:
#             self.onRightClick(event, msg)
#         elif "doubleLeftClick:" in msg:
#             self.onLeftDoubleClick(event, msg)
#             # url = msg.replace("middleClick:", "").strip()
#             # if url:  # If it's a valid URL, open it in a new tab
#             #     logma.info(f"Middle-click detected on {url}")
#             #     self.open_new_tab(pyqt.QUrl(url))
#         else:
#             msg = f"JavaScript {levels[level]}: {msg} (Line: {linenumber}, Source: {source_id})"
#         logma.warning(msg)
#         # self.app.model.store.store_app_event("background_error", "javascript", msg)
#         return self
#
#     def handle_certificate_error(self, error):
#         """"""
#         error.defer()
#         pyqt.QTimer.singleShot(0, partial(self._emit_create_certificate_error_dialog, error))
#
#     def handle_download(self, download: pyqt.QWebEngineDownloadRequest):
#         """"""
#         # Accept the download and save it to a custom location
#         path, _ = pyqt.QFileDialog.getSaveFileName(self.view, "Save video as", download.suggestedFileName())
#         if not path:
#             return
#         download.setDownloadDirectory(path)
#         download.setDownloadFileName(path)
#         download.accept()
#         # Optional: monitor progress
#         [DONE]
#         download.downloadProgress.connect(lambda recvd, total: logma.info(f"Progress: {recvd}/{total} bytes"))
#         download.finished.connect(lambda: logma.info(f"Download finished: {path}"))
#         return self
#
#     def handle_select_client_certificate(self, selection):
#         """"""
#         selection.select(selection.certificates()[0])
#         return self
#
#     def open_new_tab(self, signal, *args, **kwargs):
#         """"""
#         cfg = args[0]["action"].action
#         if isinstance(cfg["parameters_dict"], str):
#             cfg["parameters_dict"] = j.loads(cfg["parameters_dict"].replace("'", '"'))
#         pid = self.app.view.panes["left"].tree.model.current_node.nid
#         pos = len(self.app.view.panes["center"].model.tabsdata)
#         code = cfg["lookup_code_txt"][-len(cfg["lookup_code_txt"]) + cfg["lookup_code_txt"].rfind("_") + 1 :]
#         did = uuid()
#         name = f"{code.lower().replace(' ', '')} {did[-5:]}"
#         widget = args[0]["action"].action["widget_txt"]
#         # db = self.app.model.instance.db  [DONE]
#         db = "db"
#         context = ""
#         content = {}
#         syntax = ""
#         doc_type = cfg["lookup_code_txt"]
#         document = {
#             "name": name,
#             "widget": widget,
#             "type": doc_type,
#             "did": did,
#             "pid": pid,
#             "tid": uuid(),
#             "position": pos,
#             "tabset": "center",
#             "context": context,
#             "version": 0,
#             "hash": "",
#             "policy_fk": None,
#             "content": content,
#             "syntax": syntax,
#         }
#         params = cfg["parameters_dict"]
#         self.app.model.add_tab(document, did, pid, pos, widget, params, doc_type, "center", db, True)
#         self.app.view.panes["left"].tree.model.current_node.updateTabs("center")
#         self.app.view.panes["center"].setCurrentIndex(pos)
#         return self
#
#     def onLeftClick(self, event, msg=None):
#         """"""
#         logma.info(f"onLeftClick: {event}")
#         super().onLeftClick(event)
#         pos = event.position().toPoint()
#         self.page().hitTestContent(pos).then(self.goto_page)
#         return self
#
#     def onMiddleClick(self, event, msg=None):
#         """"""
#         logma.info(f"onMiddleClick: {event}")
#         super().onMiddleClick(event)
#         pos = event.position().toPoint()
#         # Fetch the URL underneath the point where the user clicked
#         self.page().hitTestContent(pos).then(self.open_new_tab)
#         return self
#
#     def pause_and_mute(self):
#         self.setAudioMuted(True)
#         self.runJavaScript(media_pause())
#         # Optional: freeze background page if supported
#         if hasattr(pyqt.QWebEnginePage, "LifecycleState"):
#             try:
#                 self.setLifecycleState(pyqt.QWebEnginePage.LifecycleState.Frozen)
#             except Exception:
#                 pass
#         return self
#
#     def resume_and_unmute(self):
#         # Unfreeze first
#         if hasattr(pyqt.QWebEnginePage, "LifecycleState"):
#             try:
#                 self.page().setLifecycleState(pyqt.QWebEnginePage.LifecycleState.Active)
#             except Exception:
#                 pass
#         self.setAudioMuted(False)
#         # Only resume items that explicitly intended to play
#         self.runJavaScript(media_play())
#         return self
#
#     def hard_stop(self):
#         # Stop media and free resources before closing
#         self.runJavaScript(media_pause())
#         self.setAudioMuted(True)
#         self.setUrl(pyqt.QUrl("about:blank"))
#         return self
#
#     def show_cookies(self):
#         """"""
#         cookie_store = self.profile.cookieStore()
#
#         # cookie_store.cookieAdded.connect(lambda cookie: logma.info("New Cookie Added:", cookie.toRawForm().data()))
#         # Function to handle each cookie
#         def handle_cookie(cookie):
#             logma.info(f"Cookie Name: {cookie.name().data().decode()}")
#             logma.info(f"Cookie Value: {cookie.value().data().decode()}")
#
#         # Get all cookies
#         cookie_store.cookiesForUrl(self.web_view.url(), handle_cookie)
#
#     def unsupportedContent(self, reply):
#         logma.info(f"Unsupported content: {reply.url().toString()}")
#
#         # Start downloading the content instead
#         reply.download()
#
#     def _emit_create_certificate_error_dialog(self, error):
#         """"""
#         self.create_certificate_error_dialog.emit(error)
#
#     def _on_fullscreen_requested(self, request):
#         """"""
#         # Allow full-screen when user interacts; you can add your own UI toggle
#         request.accept()
#
#     def _on_feature_permission(self, url, feature):
#         """"""
#         # Optionally handle camera/mic/screen capture requests
#         # For audio-only pages, you can deny by default and show a prompt in your app.
#         self.setFeaturePermission(url, feature, pyqt.QWebEnginePage.PermissionDeniedByUser)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
