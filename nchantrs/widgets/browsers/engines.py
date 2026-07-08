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
from os import environ

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.browsers.javascript.scripts import event_listener_middle_click
from nchantrs.widgets.browsers.pages import NchantdWebEnginePage
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from nchantrs.widgets.browsers.requests import NchantdRequestInterceptor
from nchantrs.widgets.browsers.downloads import NchantdDownloadManager, CodecDownloadThread

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = False
logma = Logma(__name__)
if not log:
    logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


# Set Qt environment variables before QApplication creation
def setup_qt_environment():
    """Configure Qt environment for better graphics compatibility"""
    # Force software rendering if hardware acceleration fails
    # environ["QT_QUICK_BACKEND"] = "software"
    # environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer --disable-gpu-sandbox --no-sandbox"
    # Set graphics backend
    # environ["QT_QPA_PLATFORM"] = "xcb"  # For Linux
    # Disable hardware acceleration problematic features
    environ["QTWEBENGINE_DISABLE_GPU_THREAD"] = "1"
    # Force OpenGL ES 2.0 for better compatibility
    environ["QT_OPENGL"] = "es2"
    # Alternative: use software OpenGL
    # environ["QT_OPENGL"] = "software"
    logma.info("Qt environment configured for graphics compatibility")


# # Call setup before any Qt widgets are created
# setup_qt_environment()


# class NchantdWebEngineView(NchantdWidgetMixin, pyqt.QWebEngineView):
#     """Custom web engine view with enhanced functionality"""
#
#     # Custom signals
#     urlNavigated = pyqt.Signal(pyqt.QUrl)
#     backAvailable = pyqt.Signal(bool)
#     forwardAvailable = pyqt.Signal(bool)
#
#     def __init__(self, profile=None, parent=None, cfg=None):
#         super().__init__(parent)
#         self.parent = parent
#         self.config = kahndor.Instruct(pxcfg).select("NchantdWebEngineView")
#         if self.parent:
#             self.config.override(parent.config)
#         self.config.override(cfg)
#         # Create custom profile if not provided
#         if profile is None:
#             profile = self.create_custom_profile()
#
#         # Create custom page with the profile
#         self.custom_page = NchantdWebEnginePage(profile, self)
#         self.setPage(self.custom_page)
#         self.setup_view()


# def initModel(self, cfg=None):
#     """"""
#     super().initModel(cfg)
#     self.download_manager = NchantdDownloadManager()
#     self.setup_download_handling()
#     self.loadFinished.connect(self.init_listeners)
#     return self
class NchantdWebEngineView(NchantdWidgetMixin, pyqt.QWebEngineView):
    """Custom web engine view with enhanced functionality"""

    # Custom signals
    urlNavigated = pyqt.Signal(pyqt.QUrl)
    backAvailable = pyqt.Signal(bool)
    forwardAvailable = pyqt.Signal(bool)

    def __init__(self, profile=None, parent=None, cfg=None):
        super().__init__(parent)
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdWebEngineView")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

        # Create custom profile if not provided
        if profile is None:
            # Important: Set the view as parent to the profile to ensure correct destruction order
            profile = self.create_custom_profile()

        # Create custom page with the profile
        try:
            # Set the view as parent to the page
            self.custom_page = NchantdWebEnginePage(profile, self)
            self.setPage(self.custom_page)
        except Exception as e:
            logma.error(f"Failed to create custom page: {e}")
            # Fallback to default page
            self.custom_page = None

        self.setup_view()

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        try:
            self.download_manager = NchantdDownloadManager()
            self.setup_download_handling()
        except Exception as e:
            logma.error(f"Failed to setup download manager: {e}")
            self.download_manager = None

        self.loadFinished.connect(self.init_listeners)
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def init_listeners(self):
        """"""
        script = event_listener_middle_click()
        self.page().runJavaScript(script)
        return self

    def _geo(self):
        """Compact geometry/visibility string for diagnostic logging."""
        try:
            s = self.size()
            p = self.parentWidget()
            ps = p.size() if p is not None else None
            return (
                f"size={s.width()}x{s.height()} visible={self.isVisible()} "
                f"hidden={self.isHidden()} url={self.url().toString()!r} "
                f"parent={type(p).__name__ if p is not None else None} "
                f"parent_size={ps.width()}x{ps.height() if ps is not None else '?'}"
                if ps is not None
                else f"size={s.width()}x{s.height()} visible={self.isVisible()} url={self.url().toString()!r} parent=None"
            )
        except Exception as e:
            return f"<geo error: {e}>"

    def showEvent(self, event):
        """Reactivate the page lifecycle and repaint when re-shown (Fix C).

        QWebEngineView drops its rendered frame when its page is hidden (e.g.
        on QTabWidget tab switches / rebuilds) and does not always repaint on
        re-show. Bring the page back to Active and force an update.
        """
        super().showEvent(event)
        logma.info(f"[webengine] showEvent | {self._geo()}")
        page = self.page()
        if page is not None:
            try:
                page.setLifecycleState(pyqt.QWebEnginePage.LifecycleState.Active)
                logma.info("[webengine] showEvent -> lifecycle set Active")
            except Exception as e:
                logma.error(f"[webengine] setLifecycleState failed: {e}")
        self.update()

    def resizeEvent(self, event):
        """Log resizes so we can see whether the view ever gets real geometry."""
        super().resizeEvent(event)
        try:
            s = event.size()
            logma.info(f"[webengine] resizeEvent | new={s.width()}x{s.height()} visible={self.isVisible()}")
        except Exception as e:
            logma.error(f"[webengine] resizeEvent log failed: {e}")

    def hideEvent(self, event):
        """Log hides (tab switch / rebuild) to correlate with blank-on-reshow."""
        super().hideEvent(event)
        logma.info(f"[webengine] hideEvent | {self._geo()}")

    def contextMenuEvent(self, event):
        """Handle right-click context menu"""
        menu = self.page().createStandardContextMenu()

        # Check if right-clicked on an image
        hit_test = self.page().hitTestContent(event.pos())
        if hit_test.isContentEditable():
            pass  # Let standard menu handle it

        # We can add custom actions here if needed
        # For example, a custom "Save image" if we want to bypass standard dialog

        menu.exec(self.mapToGlobal(event.pos()))

    def _resolve_app_model(self):
        """Reach the app model from a web view during __init__.

        self.app may not be wired yet this early, so fall back to the parent
        (the NchantdWebViewer), which has already resolved self.app.
        """
        for owner in (self, getattr(self, "parent", None)):
            app = getattr(owner, "app", None) if owner is not None else None
            model = getattr(app, "model", None) if app is not None else None
            if model is not None:
                return model
        return None

    def create_custom_profile(self):
        """Return the web engine profile this view should use.

        Preferred: a shared profile from the app-level pool
        (``app.model.get_web_profiles()``) — the default is one persistent
        profile shared by every view at a single storage path, which restores
        cookie/login persistence while avoiding the multi-object same-path
        corruption that previously blanked every view after the first.

        The viewer cfg may request a named profile via ``cfg["profile"]``.

        Fallback (pool/app unavailable): an off-the-record in-memory profile so
        the view still renders, just without persistence.
        """
        # 1) Try the app-level shared profile pool.
        try:
            model = self._resolve_app_model()
            if model is not None and hasattr(model, "get_web_profiles"):
                pool = model.get_web_profiles()
                name = None
                try:
                    name = self.config.dikt.get("profile")
                except Exception:
                    name = None
                if name:
                    profile = pool.get_or_create(name)
                else:
                    profile = pool.get_default_profile()
                logma.info(
                    f"[webengine] using shared pool profile name={name or 'default'} "
                    f"| off_the_record={profile.isOffTheRecord()} "
                    f"| storage={profile.persistentStoragePath()!r} | cache={profile.cachePath()!r}"
                )
                # NOTE: do NOT parent/interceptor here — the pool owns lifetime
                # and installs the interceptor once on the shared profile.
                return profile
            logma.warning("[webengine] app profile pool unavailable; using off-the-record fallback")
        except Exception as e:
            logma.error(f"[webengine] pool profile fetch failed ({e}); using off-the-record fallback", exc_info=True)

        # 2) Fallback: off-the-record, in-memory, no shared-path clash.
        try:
            # Local import avoids any import cycle between engines and profiles.
            from nchantrs.widgets.browsers.profiles import modern_user_agent

            profile = pyqt.QWebEngineProfile(self)
            profile.setHttpCacheType(pyqt.QWebEngineProfile.HttpCacheType.MemoryHttpCache)
            profile.setPersistentCookiesPolicy(pyqt.QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies)
            # Modern UA matched to the real engine (was legacy "CustomWebBrowser/1.0").
            profile.setHttpUserAgent(modern_user_agent())
            profile.setHttpAcceptLanguage("en-US,en;q=0.9")
            logma.info(
                f"[webengine] fallback profile created | off_the_record={profile.isOffTheRecord()} "
                f"| cache_type={profile.httpCacheType()}"
            )
            try:
                self.interceptor = NchantdRequestInterceptor(profile)
                profile.setUrlRequestInterceptor(self.interceptor)
            except Exception as e:
                logma.error(f"Failed to create request interceptor: {e}")
            return profile
        except Exception as e:
            logma.error(f"Failed to create custom profile: {e}")
            return pyqt.QWebEngineProfile.defaultProfile()

    # def create_custom_profile(self):
    #     """Create a custom web engine profile"""
    #     # Create a custom profile (can be persistent or off-the-record)
    #     profile = pyqt.QWebEngineProfile("CustomProfile", self)
    #     # Configure profile settings
    #     profile.setHttpCacheType(pyqt.QWebEngineProfile.HttpCacheType.DiskHttpCache)
    #     profile.setPersistentCookiesPolicy(pyqt.QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
    #     # Set custom user agent
    #     profile.setHttpUserAgent("CustomWebBrowser/1.0")
    #     # Create and install request interceptor
    #     self.interceptor = NchantdRequestInterceptor(profile)
    #     profile.setUrlRequestInterceptor(self.interceptor)
    #     return profile

    def go_back_in_history(self):
        """Go back in navigation history"""
        if self.page().history().canGoBack():
            logma.info("Going back in history")
            self.back()
        else:
            logma.info("Cannot go back - no history available")

    def go_forward_in_history(self):
        """Go forward in navigation history"""
        if self.page().history().canGoForward():
            logma.info("Going forward in history")
            self.forward()
        else:
            logma.info("Cannot go forward - no forward history available")

    @pyqt.Slot(pyqt.QWebEngineDownloadRequest)
    def handle_download_request(self, download_request: pyqt.QWebEngineDownloadRequest):
        """Handle download requests"""
        # Let download manager handle it
        download_id = self.download_manager.handle_download_request(download_request)
        if download_id:
            logma.info(f"Download started with ID: {download_id}")

    def navigate_to_url(self, url_string):
        """Navigate to a specific URL"""
        if not url_string.startswith(("http://", "https://", "file://")):
            url_string = f"https://{url_string}"
        url = pyqt.QUrl(url_string)
        if url.isValid():
            logma.info(f"Navigating to: {url.toString()}")
            self.setUrl(url)
        else:
            logma.info(f"Invalid URL: {url_string}")

    @pyqt.Slot()
    def on_history_changed(self):
        """Handle navigation history changes"""
        self.backAvailable.emit(self.history().canGoBack())
        self.forwardAvailable.emit(self.history().canGoForward())
        self.update_navigation_states()

    @pyqt.Slot(bool)
    def on_load_finished(self, success):
        """Handle page load completion - this is when history is updated"""
        logma.info(f"Page load finished - Success: {success}")
        self.backAvailable.emit(self.history().canGoBack())
        self.forwardAvailable.emit(self.history().canGoForward())
        self.update_navigation_states()

    @pyqt.Slot(pyqt.QUrl, str)
    def on_navigation_requested(self, url, nav_type):
        """Handle navigation requests from custom page"""
        logma.info(f"View received navigation request: {url.toString()} ({nav_type})")

    @pyqt.Slot(pyqt.QUrl)
    def on_page_load_started(self, url):
        """Handle page load start"""
        logma.info(f"View: Page load started for {url.toString()}")

    @pyqt.Slot(pyqt.QUrl, bool)
    def on_page_load_finished(self, url, success):
        """Handle page load completion"""
        logma.info(f"View: Page load finished for {url.toString()} - Success: {success}")

        # Update navigation button states
        self.update_navigation_states()

    @pyqt.Slot(pyqt.QUrl)
    def on_url_changed(self, url):
        """Handle URL changes in the view"""
        logma.info(f"View URL changed: {url.toString()}")
        self.urlNavigated.emit(url)
        self.update_navigation_states()

    def setup_download_handling(self):
        """Setup download request handling"""
        # Connect to profile's download signal
        profile = self.page().profile()
        profile.downloadRequested.connect(self.handle_download_request)

    def setup_view(self):
        """Initialize view connections and settings"""
        # Connect to signals that indicate navigation/history changes
        self.urlChanged.connect(self.on_url_changed)
        self.loadFinished.connect(self.on_load_finished)

        # # Connect custom page signals
        # self.custom_page.navigationRequested.connect(self.on_navigation_requested)
        # self.custom_page.pageLoadStarted.connect(self.on_page_load_started)
        # self.custom_page.pageLoadFinished.connect(self.on_page_load_finished)

    def reload_page(self):
        """Reload current page"""
        current_url = self.url()
        logma.info(f"Reloading page: {current_url.toString()}")
        self.reload()

    def update_navigation_states(self):
        """Update the state of navigation buttons"""
        history = self.page().history()
        can_go_back = history.canGoBack()
        can_go_forward = history.canGoForward()

        self.backAvailable.emit(can_go_back)
        self.forwardAvailable.emit(can_go_forward)

    def closeEvent(self, event):
        """Handle cleanup before destruction to avoid profile release warnings"""
        # Set page to None to decouple it from the profile before the view is destroyed
        # This helps ensuring the page is destroyed before the profile
        logma.info("NchantdWebEngineView.closeEvent - cleaning up page")
        self.setPage(pyqt.QWebEnginePage(self))
        if hasattr(self, "custom_page") and self.custom_page:
            self.custom_page.deleteLater()
            self.custom_page = None
        super().closeEvent(event)


class NchantdWebEngineViewH264(NchantdWidgetMixin, pyqt.QWebEngineView):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent)
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdWebEngineView")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    #     self.installEventFilter(self)  # Install the event filter
    #
    # def eventFilter(self, source, event):
    #     # Check for mouse press events
    #     if isinstance(event, pyqt.QHoverEvent):
    #         return self
    #     logma.info(f"eventFilter: {event}")
    #
    #     if event.type() == pyqt.QEvent.Type.MouseButtonPress:
    #         # Check if the middle button was pressed
    #         if event.button() == pyqt.Qt.MiddleButton:
    #             # Get the position of the click
    #             pos = event.position().toPoint()
    #
    #             # Perform a hit test to get the element under the mouse
    #             self.page().hitTestContent(pos).then(self._handle_hit_test)
    #             return True  # Consume the event
    #     return super().eventFilter(source, event)

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        self.loadFinished.connect(self.init_listeners)
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def init_listeners(self):
        """"""
        script = event_listener_middle_click()
        self.page().runJavaScript(script)
        return self

    def closeEvent(self, event):
        """"""
        page = self.page()
        page.deleteLater()
        self.setPage(None)
        super().closeEvent(event)
        return self

    def contextMenuEvent(self, event):
        menu = pyqt.QMenu(self)
        download_action = menu.addAction("Download video")
        action = menu.exec(self.mapToGlobal(event.pos()))
        if action == download_action:
            self.download_current_video()

    def download_current_video(self):
        js = """
        (function(){
            const v = document.querySelector('video');
            if (!v) return JSON.stringify({ok:false, reason:'no-video'});
            const src = v.currentSrc || v.src || (v.querySelector('source') ? v.querySelector('source').src : '');
            return JSON.stringify({ok: !!src, src, isBlob: src.startsWith('blob:')});
        })();
        """
        self.page().runJavaScript(js, self._handle_video_src)

    def setup_codec(self):
        """Initial codec setup."""
        if self.downloader.is_available():
            library_path = self.downloader.get_library_path()
            self.status_label.setText(f"OpenH264 available: {library_path}")
            self.download_button.setText("Codec Ready")
            self.download_button.setEnabled(False)
            self.setup_webengine_settings()
        else:
            self.status_label.setText("OpenH264 not available - download required")

    def setup_webengine_settings(self):
        """Configure WebEngine settings for media playback."""
        settings = self.web_view.settings()
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)

        # Enable hardware acceleration if available
        if self.downloader.is_available():
            library_path = self.downloader.get_library_path()
            # Set codec path via environment (must be done before QApplication creation ideally)

    def download_codec(self):
        """Download OpenH264 codec in background thread."""
        self.download_button.setEnabled(False)
        self.status_label.setText("Starting download...")

        self.download_thread = CodecDownloadThread(self.downloader)
        self.download_thread.progress.connect(self.status_label.setText)
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.start()

    def on_download_finished(self, success: bool, message: str):
        """Handle download completion."""
        self.status_label.setText(message)

        if success:
            self.download_button.setText("Codec Ready")
            self.setup_webengine_settings()
        else:
            self.download_button.setEnabled(True)
            self.download_button.setText("Retry Download")

    def test_h264_video(self):
        """Load a test page with H.264 video."""
        test_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>H.264 Test</title>
        </head>
        <body>
            <h1>H.264 Video Test</h1>
            <video width="640" height="480" controls autoplay>
                <source src="https://sample-videos.com/zip/10/mp4/mp4-4K/SampleVideo_1280x720_1mb.mp4" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <p>If the codec is working, you should see the video above.</p>

            <script>
                // Check codec support
                const video = document.createElement('video');
                const canPlayH264 = video.canPlayType('video/mp4; codecs="avc1.42E01E"');
                console.log('H.264 support:', canPlayH264);

                document.body.innerHTML += '<p>H.264 Support: ' + canPlayH264 + '</p>';
            </script>
        </body>
        </html>
        """

        self.web_view.setHtml(test_html)

    def _handle_video_src(self, result_json):
        try:
            data = __import__("json").loads(result_json or "{}")
        except Exception:
            data = {"ok": False}
        if not data.get("ok"):
            logma.info("No downloadable video source found.")
            return
        src = data["src"]
        if data.get("isBlob"):
            logma.info("The video uses a blob: URL (MSE). Direct download is not available.")
            return
        url = pyqt.QUrl(src)
        if not url.isValid():
            logma.info("Invalid video URL.")
            return
        # Ask where to save
        suggested = url.fileName() or "video.mp4"
        path, _ = pyqt.QFileDialog.getSaveFileName(self, "Save video as", suggested)
        if not path:
            return

        # Use WebEngine's downloader
        req = self.page().profile().download(url, path)
        req.downloadProgress.connect(lambda r, t: logma.info(f"Progress: {r}/{t}"))
        try:
            req.finished.connect(lambda: logma.info("Download finished:", path))
        except AttributeError:
            req.stateChanged.connect(lambda _: logma.info("Download state:", req.state()))

    # def mousePressEvent(self, event):
    #     """"""
    #     logma.info("Mouse Press Event")
    #
    # def onLeftClick(self, event):
    #     """"""
    #     logma.info(f"onLeftClick: {event}")
    #     super().onLeftClick(event)
    #     pos = event.position().toPoint()
    #     self.page().hitTestContent(pos).then(self.goto_page)
    #     return self
    #
    # def onMiddleClick(self, event):
    #     """"""
    #     logma.info(f"onMiddleClick: {event}")
    #     super().onMiddleClick(event)
    #     pos = event.position().toPoint()
    #     # Fetch the URL underneath the point where the user clicked
    #     self.page().hitTestContent(pos).then(self.open_new_tab)
    #     return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
