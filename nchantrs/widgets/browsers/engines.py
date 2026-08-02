from typing import Any, Optional, Union
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
from os import environ
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.browsers.javascript.scripts import event_listener_middle_click
from nchantrs.widgets.browsers.pages import NchantdWebEnginePage
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from nchantrs.widgets.browsers.requests import NchantdRequestInterceptor
from nchantrs.widgets.browsers.downloads import NchantdDownloadManager, CodecDownloadThread
here = join(dirname(__file__), '')
log = False
logma = Logma(__name__)
if not log:
    logma.off()
pxcfg = join(here, '_data_', '.yaml')

def setup_qt_environment() -> None:
    """Configure Qt environment for better graphics compatibility"""
    environ['QTWEBENGINE_DISABLE_GPU_THREAD'] = '1'
    environ['QT_OPENGL'] = 'es2'
    logma.info('Qt environment configured for graphics compatibility')

class NchantdWebEngineView(NchantdWidgetMixin, pyqt.QWebEngineView):
    """Custom web engine view with enhanced functionality"""
    urlNavigated = pyqt.Signal(pyqt.QUrl)
    backAvailable = pyqt.Signal(bool)
    forwardAvailable = pyqt.Signal(bool)

    def __init__(self, profile=None, parent=None, cfg=None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdWebEngineView')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        if profile is None:
            profile = self.create_custom_profile()
        try:
            self.custom_page = NchantdWebEnginePage(profile, self)
            self.setPage(self.custom_page)
        except Exception as e:
            logma.error(f'Failed to create custom page: {e}')
            self.custom_page = None
        self.setup_view()

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        try:
            self.download_manager = NchantdDownloadManager()
            self.setup_download_handling()
        except Exception as e:
            logma.error(f'Failed to setup download manager: {e}')
            self.download_manager = None
        self.loadFinished.connect(self.init_listeners)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def init_listeners(self) -> Any:
        """"""
        script = event_listener_middle_click()
        self.page().runJavaScript(script)
        return self

    def _geo(self) -> Union[Any, str]:
        """Compact geometry/visibility string for diagnostic logging."""
        try:
            s = self.size()
            p = self.parentWidget()
            ps = p.size() if p is not None else None
            return f"size={s.width()}x{s.height()} visible={self.isVisible()} hidden={self.isHidden()} url={self.url().toString()!r} parent={(type(p).__name__ if p is not None else None)} parent_size={ps.width()}x{(ps.height() if ps is not None else '?')}" if ps is not None else f'size={s.width()}x{s.height()} visible={self.isVisible()} url={self.url().toString()!r} parent=None'
        except Exception as e:
            return f'<geo error: {e}>'

    def showEvent(self, event) -> None:
        """Reactivate the page lifecycle and repaint when re-shown (Fix C).

        QWebEngineView drops its rendered frame when its page is hidden (e.g.
        on QTabWidget tab switches / rebuilds) and does not always repaint on
        re-show. Bring the page back to Active and force an update.
        """
        super().showEvent(event)
        logma.info(f'[webengine] showEvent | {self._geo()}')
        page = self.page()
        if page is not None:
            try:
                page.setLifecycleState(pyqt.QWebEnginePage.LifecycleState.Active)
                logma.info('[webengine] showEvent -> lifecycle set Active')
            except Exception as e:
                logma.error(f'[webengine] setLifecycleState failed: {e}')
        self.update()

    def resizeEvent(self, event) -> None:
        """Log resizes so we can see whether the view ever gets real geometry."""
        super().resizeEvent(event)
        try:
            s = event.size()
            logma.info(f'[webengine] resizeEvent | new={s.width()}x{s.height()} visible={self.isVisible()}')
        except Exception as e:
            logma.error(f'[webengine] resizeEvent log failed: {e}')

    def hideEvent(self, event) -> None:
        """Log hides (tab switch / rebuild) to correlate with blank-on-reshow."""
        super().hideEvent(event)
        logma.info(f'[webengine] hideEvent | {self._geo()}')

    def contextMenuEvent(self, event) -> None:
        """Handle right-click context menu"""
        menu = self.page().createStandardContextMenu()
        hit_test = self.page().hitTestContent(event.pos())
        if hit_test is not None:
            if hit_test.isContentEditable():
                pass
        if menu is None:
            return
        menu.exec(self.mapToGlobal(event.pos()))

    def _resolve_app_model(self) -> Optional[Any]:
        """Reach the app model from a web view during __init__.

        self.app may not be wired yet this early, so fall back to the parent
        (the NchantdWebViewer), which has already resolved self.app.
        """
        for owner in (self, getattr(self, 'parent', None)):
            app = getattr(owner, 'app', None) if owner is not None else None
            model = getattr(app, 'model', None) if app is not None else None
            if model is not None:
                return model
        return None

    def create_custom_profile(self) -> Union[Any, str]:
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
        try:
            model = self._resolve_app_model()
            if model is not None and hasattr(model, 'get_web_profiles'):
                pool = model.get_web_profiles()
                name = None
                try:
                    name = self.config.dikt.get('profile')
                except Exception:
                    name = None
                if name:
                    profile = pool.get_or_create(name)
                else:
                    profile = pool.get_default_profile()
                logma.info(f"[webengine] using shared pool profile name={name or 'default'} | off_the_record={profile.isOffTheRecord()} | storage={profile.persistentStoragePath()!r} | cache={profile.cachePath()!r}")
                return profile
            logma.warning('[webengine] app profile pool unavailable; using off-the-record fallback')
        except Exception as e:
            logma.error(f'[webengine] pool profile fetch failed ({e}); using off-the-record fallback', exc_info=True)
        try:
            from nchantrs.widgets.browsers.profiles import DEFAULT_USER_AGENT, install_google_login_ua_script
            profile = pyqt.QWebEngineProfile(self)
            profile.setHttpCacheType(pyqt.QWebEngineProfile.HttpCacheType.MemoryHttpCache)
            profile.setPersistentCookiesPolicy(pyqt.QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies)
            profile.setHttpUserAgent(DEFAULT_USER_AGENT)
            profile.setHttpAcceptLanguage('en-US,en;q=0.9')
            install_google_login_ua_script(profile)
            logma.info(f'[webengine] fallback profile created | off_the_record={profile.isOffTheRecord()} | cache_type={profile.httpCacheType()}')
            try:
                self.interceptor = NchantdRequestInterceptor(profile)
                profile.setUrlRequestInterceptor(self.interceptor)
            except Exception as e:
                logma.error(f'Failed to create request interceptor: {e}')
            return profile
        except Exception as e:
            logma.error(f'Failed to create custom profile: {e}')
            return pyqt.QWebEngineProfile.defaultProfile()

    def go_back_in_history(self) -> None:
        """Go back in navigation history"""
        if self.page().history().canGoBack():
            logma.info('Going back in history')
            self.back()
        else:
            logma.info('Cannot go back - no history available')

    def go_forward_in_history(self) -> None:
        """Go forward in navigation history"""
        if self.page().history().canGoForward():
            logma.info('Going forward in history')
            self.forward()
        else:
            logma.info('Cannot go forward - no forward history available')

    @pyqt.Slot(pyqt.QWebEngineDownloadRequest)
    def handle_download_request(self, download_request: pyqt.QWebEngineDownloadRequest) -> None:
        """Handle download requests"""
        download_id = self.download_manager.handle_download_request(download_request)
        if download_id:
            logma.info(f'Download started with ID: {download_id}')

    def navigate_to_url(self, url_string) -> None:
        """Navigate to a specific URL"""
        if not url_string.startswith(('http://', 'https://', 'file://')):
            url_string = f'https://{url_string}'
        url = pyqt.QUrl(url_string)
        if url.isValid():
            logma.info(f'Navigating to: {url.toString()}')
            self.setUrl(url)
        else:
            logma.info(f'Invalid URL: {url_string}')

    @pyqt.Slot()
    def on_history_changed(self) -> None:
        """Handle navigation history changes"""
        self.backAvailable.emit(self.history().canGoBack())
        self.forwardAvailable.emit(self.history().canGoForward())
        self.update_navigation_states()

    @pyqt.Slot(bool)
    def on_load_finished(self, success) -> None:
        """Handle page load completion - this is when history is updated"""
        logma.info(f'Page load finished - Success: {success}')
        self.backAvailable.emit(self.history().canGoBack())
        self.forwardAvailable.emit(self.history().canGoForward())
        self.update_navigation_states()

    @pyqt.Slot(pyqt.QUrl, str)
    def on_navigation_requested(self, url, nav_type) -> None:
        """Handle navigation requests from custom page"""
        logma.info(f'View received navigation request: {url.toString()} ({nav_type})')

    @pyqt.Slot(pyqt.QUrl)
    def on_page_load_started(self, url) -> None:
        """Handle page load start"""
        logma.info(f'View: Page load started for {url.toString()}')

    @pyqt.Slot(pyqt.QUrl, bool)
    def on_page_load_finished(self, url, success) -> None:
        """Handle page load completion"""
        logma.info(f'View: Page load finished for {url.toString()} - Success: {success}')
        self.update_navigation_states()

    @pyqt.Slot(pyqt.QUrl)
    def on_url_changed(self, url) -> None:
        """Handle URL changes in the view"""
        logma.info(f'View URL changed: {url.toString()}')
        self.urlNavigated.emit(url)
        self.update_navigation_states()

    def setup_download_handling(self) -> None:
        """Setup download request handling"""
        profile = self.page().profile()
        profile.downloadRequested.connect(self.handle_download_request)

    def setup_view(self) -> None:
        """Initialize view connections and settings"""
        self.urlChanged.connect(self.on_url_changed)
        self.loadFinished.connect(self.on_load_finished)

    def reload_page(self) -> None:
        """Reload current page"""
        current_url = self.url()
        logma.info(f'Reloading page: {current_url.toString()}')
        self.reload()

    def update_navigation_states(self) -> None:
        """Update the state of navigation buttons"""
        history = self.page().history()
        can_go_back = history.canGoBack()
        can_go_forward = history.canGoForward()
        self.backAvailable.emit(can_go_back)
        self.forwardAvailable.emit(can_go_forward)

    def closeEvent(self, event) -> None:
        """Handle cleanup before destruction to avoid profile release warnings"""
        logma.info('NchantdWebEngineView.closeEvent - cleaning up page')
        self.setPage(pyqt.QWebEnginePage(self))
        if hasattr(self, 'custom_page') and self.custom_page:
            self.custom_page.deleteLater()
            self.custom_page = None
        super().closeEvent(event)

class NchantdWebEngineViewH264(NchantdWidgetMixin, pyqt.QWebEngineView):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent)
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdWebEngineView')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        self.loadFinished.connect(self.init_listeners)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def init_listeners(self) -> Any:
        """"""
        script = event_listener_middle_click()
        self.page().runJavaScript(script)
        return self

    def closeEvent(self, event) -> Any:
        """"""
        page = self.page()
        page.deleteLater()
        self.setPage(None)
        super().closeEvent(event)
        return self

    def contextMenuEvent(self, event) -> None:
        menu = pyqt.QMenu(self)
        download_action = menu.addAction('Download video')
        action = menu.exec(self.mapToGlobal(event.pos()))
        if action == download_action:
            self.download_current_video()

    def download_current_video(self) -> None:
        js = "\n        (function(){\n            const v = document.querySelector('video');\n            if (!v) return JSON.stringify({ok:false, reason:'no-video'});\n            const src = v.currentSrc || v.src || (v.querySelector('source') ? v.querySelector('source').src : '');\n            return JSON.stringify({ok: !!src, src, isBlob: src.startsWith('blob:')});\n        })();\n        "
        self.page().runJavaScript(js, self._handle_video_src)

    def setup_codec(self) -> None:
        """Initial codec setup."""
        if self.downloader.is_available():
            library_path = self.downloader.get_library_path()
            self.status_label.setText(f'OpenH264 available: {library_path}')
            self.download_button.setText('Codec Ready')
            self.download_button.setEnabled(False)
            self.setup_webengine_settings()
        else:
            self.status_label.setText('OpenH264 not available - download required')

    def setup_webengine_settings(self) -> None:
        """Configure WebEngine settings for media playback."""
        settings = self.web_view.settings()
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        if self.downloader.is_available():
            library_path = self.downloader.get_library_path()

    def download_codec(self) -> None:
        """Download OpenH264 codec in background thread."""
        self.download_button.setEnabled(False)
        self.status_label.setText('Starting download...')
        self.download_thread = CodecDownloadThread(self.downloader)
        self.download_thread.progress.connect(self.status_label.setText)
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.start()

    def on_download_finished(self, success: bool, message: str) -> None:
        """Handle download completion."""
        self.status_label.setText(message)
        if success:
            self.download_button.setText('Codec Ready')
            self.setup_webengine_settings()
        else:
            self.download_button.setEnabled(True)
            self.download_button.setText('Retry Download')

    def test_h264_video(self) -> None:
        """Load a test page with H.264 video."""
        test_html = '\n        <!DOCTYPE html>\n        <html>\n        <head>\n            <title>H.264 Test</title>\n        </head>\n        <body>\n            <h1>H.264 Video Test</h1>\n            <video width="640" height="480" controls autoplay>\n                <source src="https://sample-videos.com/zip/10/mp4/mp4-4K/SampleVideo_1280x720_1mb.mp4" type="video/mp4">\n                Your browser does not support the video tag.\n            </video>\n            <p>If the codec is working, you should see the video above.</p>\n\n            <script>\n                // Check codec support\n                const video = document.createElement(\'video\');\n                const canPlayH264 = video.canPlayType(\'video/mp4; codecs="avc1.42E01E"\');\n                console.log(\'H.264 support:\', canPlayH264);\n\n                document.body.innerHTML += \'<p>H.264 Support: \' + canPlayH264 + \'</p>\';\n            </script>\n        </body>\n        </html>\n        '
        self.web_view.setHtml(test_html)

    def _handle_video_src(self, result_json) -> None:
        try:
            data = __import__('json').loads(result_json or '{}')
        except Exception:
            data = {'ok': False}
        if not data.get('ok'):
            logma.info('No downloadable video source found.')
            return
        src = data['src']
        if data.get('isBlob'):
            logma.info('The video uses a blob: URL (MSE). Direct download is not available.')
            return
        url = pyqt.QUrl(src)
        if not url.isValid():
            logma.info('Invalid video URL.')
            return
        suggested = url.fileName() or 'video.mp4'
        path, _ = pyqt.QFileDialog.getSaveFileName(self, 'Save video as', suggested)
        if not path:
            return
        req = self.page().profile().download(url, path)
        req.downloadProgress.connect(lambda r, t: logma.info(f'Progress: {r}/{t}'))
        try:
            req.finished.connect(lambda: logma.info('Download finished:', path))
        except AttributeError:
            req.stateChanged.connect(lambda _: logma.info('Download state:', req.state()))