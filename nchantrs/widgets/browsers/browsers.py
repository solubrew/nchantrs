# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Nchantrs@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""#																			||
---  #																			||
<(META)>:  #																	||
    docid: ''  #							||
    name: Moonbags Nchnated Python Document#								||
    description: >  #															||
    expirary: <[expiration]>  #													||
    version: <[version]>  #														||
    path: <[LEXIvrs]>  #														||
    outline: <[outline]>  #														||
    authority: document|this  #													||
    security: sec|lvl2  #														||
    <(WT)>: -32  #																||
"""  # ||

# -*- coding: utf-8 -*-#														||
# ================================Core Modules===================================||
from os.path import dirname, join
from collections import deque
import datetime as dt
import queue
import logging
from typing import Any
from kahndor import kahndor
from subtrix.utilities import uuid
from nchantrs.dialogs.notifications import NchantdNotificationSigil
from nchantrs.libraries import pyqt
from nchantrs.widgets.browsers.engines import NchantdWebEngineView
from nchantrs.widgets.browsers.profiles import NchantdWebProfile
from nchantrs.widgets.browsers.requests import NchantdRequestInterceptor
from nchantrs.widgets.browsers.utilities import NchantdURL, NchantdWebChannel, NchantdBackend as NchantdSafeFunction
from nchantrs.widgets.media.editors.selectors import NchantdDropDown
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from nchantrs.services.links import LinkService
from kahndor.logma import Logma
from nchantrs.widgets.browsers.graphics import configure_qt_for_webengine, setup_application_attributes

configure_qt_for_webengine()

try:
    setup_application_attributes()
except Exception as e:
    Logma(__name__).warning(f"Could not set all Qt attributes: {e}")

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)

# ===============================================================================||
pxcfg = join(here, "_data_", "browsers.yaml")


class NchantdWebManager(NchantdWidgetMixin, pyqt.QObject):
    """
    Manages a pool of WebEngine views.
    TODO: Proper implementation of engine reuse and background loading.
    """

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdWebManager")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(parent)
        self.config.override(cfg)
        self.available_engines = deque([])
        self.active_engines = deque([])
        cfg = {}
        # self.link_library = PyfficeURLLibrary(cfg) TODO must be implemented in the NchatndOffice layer

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.create_engines()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def create_engines(self) -> None:
        """"""
        wip_engine_size = 3
        while len(self.available_engines) < wip_engine_size:
            # Set self as parent to the viewer so it is destroyed with the manager
            viewer = NchantdWebViewer(self)
            viewer.browser.setHtml('<html><body><h1>Loading Complete</h1></body></html>')
            self.available_engines.append(viewer)

    def get_available_engine(self) -> Any:
        """"""
        if not self.available_engines:
            self.create_engines()
        viewer = self.available_engines.popleft()
        # Note: viewer is already parented to self
        self.create_engines()
        return viewer

    def kill_engine(self) -> None:
        logma.info(f'kill_engine called')
        return self

    def switch_to_web_app(self, engine) -> None:
        logma.info(f'switch_to_web_app called')
        return self

class NchantdWebViewer(NchantdWidget):
    """ """
    link_hovered = pyqt.Signal(str)
    load_progress = pyqt.Signal(int)
    title_changed = pyqt.Signal(str)
    url_changed = pyqt.Signal(pyqt.QUrl)

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdWebViewer').override(cfg))
        self.profiles = {}
        cfg = {}
        self.browser = NchantdWebEngineView(None, self, cfg).initWidget()
        self.page = self.browser.page()
        self.url_options = []
        self.lock = False
        self.pinned_url = None
        self.default_url = None
        self.active_url = None
        self.home_url = None
        self.layout = None
        self.storage_path = None
        self.pre_view_initialized = False
        self.is_app = False
        self.is_simple = False
        self.navigation_layout = None
        self.profile_select_entry = None
        self.url_select_entry = None
        self.known_scripts = self.config.dikt.get('javascript', {}).get('code', {})
        self.browser.urlChanged.connect(self.cmd_url_changed_handler)
        self.browser.titleChanged.connect(self.title_changed.emit)
        self.browser.loadProgress.connect(self.load_progress.emit)
        self.browser.backAvailable.connect(self.on_back_available)
        self.browser.forwardAvailable.connect(self.on_forward_available)
        self.link_service = LinkService(self)

    def on_back_available(self, available) -> None:
        """Handle back availability change"""
        if hasattr(self, 'toolbar') and hasattr(self.toolbar, 'buttons'):
            pass

    def on_forward_available(self, available) -> None:
        """Handle forward availability change"""
        pass

    def initModel(self, cfg=None) -> Any:
        """"""
        self.config.override(cfg)
        super().initModel()
        self.is_app = self.config.dikt.get('is_app', False)
        if self.is_app is True:
            self.is_simple = self.config.dikt.get('is_simple', True)
        else:
            self.is_simple = self.config.dikt.get('is_simple', False)
        self.set_url_path(self.config.dikt.get('url', None))
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        cfg = dict(cfg or {})
        cfg.setdefault('fill', True)
        super().initView(cfg)
        self.setSizePolicy(pyqt.QSizePolicy.Policy.Expanding, pyqt.QSizePolicy.Policy.Expanding)
        self.browser.setSizePolicy(pyqt.QSizePolicy.Policy.Expanding, pyqt.QSizePolicy.Policy.Expanding)
        if self.browser.page is not None:
            page = self.browser.page()
            logma.info(f'Page {page}')
        self.layout.addWidget(self.browser, 1)
        self.layout.setAlignment(pyqt.Qt.AlignmentFlag(0))
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self._did_initial_load = False
        return self

    def showEvent(self, event) -> None:
        """Load on first show, once we have a surface (Fix B).

        Prefer the active URL over the configured default: an earlier
        navigation (e.g. the notebook pointing us at /tree before the tab was
        shown) sets active_url, and reloading the config default here would
        clobber it back to about:blank.
        """
        super().showEvent(event)
        #TODO this is not working correctly with the populate document function which connects to the historical
        # document saved for the browser
        # this doesn't seem to be having any impact
        try:
            vs = self.size()
            bs = self.browser.size()
            logma.info(f"[webviewer] showEvent | viewer={vs.width()}x{vs.height()} visible={self.isVisible()} | view={bs.width()}x{bs.height()} view_visible={self.browser.isVisible()} | did_initial_load={getattr(self, '_did_initial_load', None)} | active_url={getattr(self.active_url, 'url', None)}")
        except Exception as e:
            logma.error(f'[webviewer] showEvent geometry log failed: {e}')
        if not getattr(self, '_did_initial_load', False):
            self._did_initial_load = True
            if self.active_url is not None:
                logma.info(f'[webviewer] first show -> loading active_url {self.active_url.url}')
                self.populate_document(self.active_url)
            else:
                logma.info('[webviewer] first show -> no active_url, loading configured default')
                self.cmd_goto_page()

    def resizeEvent(self, event) -> None:
        """Log resizes so a collapsed (zero-height) viewer is visible in the log."""
        super().resizeEvent(event)
        try:
            s = event.size()
            bs = self.browser.size()
            logma.info(f'[webviewer] resizeEvent | viewer={s.width()}x{s.height()} view={bs.width()}x{bs.height()} visible={self.isVisible()}')
        except Exception as e:
            logma.error(f'[webviewer] resizeEvent log failed: {e}')

    def initWidget(self, url=None) -> Any:
        """ """
        self.initModel(url)
        self.initView()
        return self

    def add_profile(self, profile_name) -> Any:
        """Add a named web profile to the viewer.

        Free users are limited to a single profile (the default).  When
        ``has_pro`` is False, attempting to add a second profile pops up
        a notification explaining the Pro SKU requirement and aborts the
        add.  Pro users can add unlimited profiles.
        """
        if not getattr(self, 'has_pro', False):
            # Free-tier users cannot have multiple profiles.  Surface
            # the limitation via a notification rather than silently
            # dropping the add so the user knows what's happening.
            cfg = {'title': 'Pro feature', 'message': 'Multiple profiles are a Pro feature. Upgrade to Pro to manage more than one profile.'}
            try:
                pro_user_warning = NchantdNotificationSigil(self, cfg)
                pro_user_warning.initWidget()
            except Exception as e:
                logma.warning(f'could not show pro warning notification: {e}')
            return self
        self.profiles[profile_name] = {'default': False, 'profile': NchantdWebProfile(profile_name)}
        return self

    def build_toolbar(self) -> Any:
        """"""
        buttons = {}
        buttons[11] = {'action': 'web_page_back', 'handler': self.cmd_previous_page}
        buttons[12] = {'action': 'web_page_forward', 'handler': self.cmd_next_page}
        buttons[13] = {'action': 'web_page_refresh', 'handler': self.cmd_refresh_page}
        buttons[14] = {'name': 'select_url', 'label': 'URL', 'layout': 'horizontal', 'size': [30, 30], 'combobox': {'size': [500, 30], 'options': self.get_url_history()}, 'type': 'dropdown', 'handler': self.cmd_goto_page, 'value': self.get_current_url()}
        self.url_select_entry = NchantdDropDown(self, buttons[14])
        buttons[14]['widget'] = self.url_select_entry
        buttons[15] = {'action': 'web_page_go', 'handler': self.cmd_goto_page}
        buttons[49] = '_insert_stretch'
        buttons[150] = '_skip'
        buttons[200] = '_skip'
        return buttons

    def close_tab(self) -> None:
        """"""
        super().close_tab()

    def cmd_url_changed_handler(self, url, *args, **kwargs) -> Any:
        """"""
        logma.info(f'URL Changed: {url}')
        if self.lock is True:
            self.open_new_tab()
        url_str = url.toString() if isinstance(url, pyqt.QUrl) else str(url)
        self.set_url_path(url_str)
        try:
            title = self.browser.title() or url_str
            self.link_service.store_link(title, url_str, "'type': 'history'")
        except Exception as e:
            logma.error(f'Failed to track link: {e}')
        self.save()
        return self

    def cmd_goto_page(self, url=None, *args, **kwargs) -> Any:
        """"""
        logma.info(f'Goto Page {url}')
        if not isinstance(url, pyqt.QUrl) and (not isinstance(url, str)):
            url = None
        self.goto_page(url)
        return self

    def cmd_next_page(self, signal=None, *args, **kwargs) -> Any:
        """"""
        if self.browser.history().canGoForward():
            self.browser.forward()
        return self

    def cmd_make_webapp(self, signal, *args, **kwargs) -> Any:
        """"""
        self.lock = True
        self.active_url.set_lock()
        return self

    def cmd_refresh_page(self, signal=None, *args, **kwargs) -> Any:
        """"""
        self.cmd_goto_page()
        return self

    def cmd_previous_page(self, signal=None, *args, **kwargs) -> Any:
        """"""
        if self.browser.history().canGoBack():
            self.browser.back()
        return self

    def enable_dark_mode(self) -> None:
        """"""
        self.settings().setAttribute(pyqt.QWebEngineSettings.JavascriptEnabled, True)
        self.run_js_script(self.config.dikt['javascript']['code']['dark_mode']['text'])

    def enterFullscreenMode(self, request) -> None:
        """Enter fullscreen mode when requested by the web page."""
        if request.toggleOn():
            self.browser.setParent(None)
            self.browser.showFullScreen()
            self.exit_fullscreen_button.setVisible(True)
            request.accept()
        else:
            self.exitFullscreen(request)

    def exitFullscreen(self, request=None) -> None:
        """Exit fullscreen and reattach browser."""
        self.browser.setParent(self.centralWidget())
        self.browser.showNormal()
        self.exit_fullscreen_button.setVisible(False)
        if request:
            request.accept()

    def get_url_history(self) -> Any:
        """
        get a datafraome of the historically visited urls with a smart system showing a combination of recent
        and most visited urls
        :return:
        """
        urls = []
        return urls

    def get_important_urls(self) -> Any:
        """"""
        urls = []
        if self.active_url is not None:
            urls += [self.active_url.path]
        if self.app and self.app.model:
            urls += self.app.model.get_urls(tag='important') + self.get_recent_urls()
        urls = list(set(urls))
        return urls

    def get_home_page(self):
        """"""
        return self.home_url

    def get_recent_urls(self) -> Any:
        """"""
        urls = []
        return urls

    def get_current_url(self) -> Any:
        """"""
        if self.active_url is None:
            return self.default_url
        url = self.active_url.path
        return url

    def goto_page(self, url) -> Any:
        """"""
        logma.info(f'Goto Page {url}')
        if url is None:
            if self.url_select_entry is not None:
                url = self.url_select_entry.combobox.lineEdit().text().strip()
            if url == '':
                url = None
        logma.info(f'URL {url}')
        self.set_url_path(url)
        logma.info(f'Go To Page: {self.active_url.url}')
        self.populate_document(self.active_url)
        return self

    def handle_console_message(self, level, message, line_number, source_id) -> None:
        """
        Handles JavaScript console messages and outputs them to Python console.

        Args:
            level (QWebEnginePage.JavaScriptConsoleMessageLevel): Log level (e.g., INFO, WARNING, ERROR).
            message (str): The actual message from the JavaScript console.
            line_number (int): Line number in the JavaScript file where the message originated.
            source_id (str): The JavaScript file or source identifier where the message was generated.
        """
        log_levels = {pyqt.QWebEnginePage.JavaScriptConsoleMessageLevel.InfoMessageLevel: 'INFO', pyqt.QWebEnginePage.JavaScriptConsoleMessageLevel.WarningMessageLevel: 'WARNING', pyqt.QWebEnginePage.JavaScriptConsoleMessageLevel.ErrorMessageLevel: 'ERROR'}
        log_level = log_levels.get(level, 'INFO')
        logma.info(f'[{log_level}] Line {line_number} in {source_id}: {message}')

    def handle_download_request(self, download) -> None:
        """"""
        download.accept()
        logma.info('A Download was requested and accepted')
        download.downloadProgress.connect(lambda x, y: logma.info(f'Downloaded {x} out of {y} bytes'))
        download.stateChanged.connect(lambda: logma.info('Download state changed'))
        download.finished.connect(lambda: logma.info(f'Download finished. File saved to: {download.path()}'))
        self.model.store.store_download()

    def handle_full_screen_request(self, request) -> None:
        fullscreen_element = self.page().mainFrame()
        if fullscreen_element:
            logma.info('Fullscreen requested by element type!')

    def inject_custom_js(self, cmd) -> Any:
        """"""
        self.browser.loadFinished.connect(self.run_js_scripts)
        return self

    def inject_javascript_bridge(self) -> Any:
        """
        This function injects JavaScript that binds the Python API to the `window` object.
        """
        js_code = '\n\n        '
        self.browser.page().runJavaScript(js_code)
        return self
        # # Inject a custom theme script on navigation
        # theme_script = """

    def load_url(self, url) -> Any:
        """"""
        self.populate_document(url)
        return self

    def open_new_tab(self) -> Any:
        logma.info(f'open_new_tab called')
        return self

    def on_tab_changed(self, index: int) -> Any:
        logma.info(f'on_tab_changed event received')
        if getattr(self, 'app', None) is not None and hasattr(self.app, 'model'):
            self.app.model.has_changed = True
        return self

    def on_tab_close_requested(self, index: int) -> Any:
        logma.info(f'on_tab_close_requested event received')
        if getattr(self, 'app', None) is not None and hasattr(self.app, 'model'):
            self.app.model.has_changed = True
        return self

    def populate_document(self, url) -> Any:
        """"""
        if isinstance(url, NchantdURL):
            url = url.url
        if url is None:
            url = self.default_url
        logma.info(f"Load Document: {url}")
        if url is None:
            url = self.get_home_page() or "http://www.duckduckgo.com/"
            if url is None:
                raise Exception("No URL Provided")
        self.browser.load(url)
        self.save()
        return self

    def run_js_script(self, script) -> Any:
        """"""
        if script not in self.known_scripts:
            return self
        page = self.browser.page()
        page.runJavaScript(script)
        return self

    def save(self) -> Any:
        """Persist the viewer's current state (active URL, history).

        Writes a ``doc_media_content`` entry with the viewer's state
        snapshot (``_to_dict()`` payload) and emits a model event so
        the broader application knows the viewer state changed.
        Returns the dict for the caller to chain.
        """
        logma.info(f'save called')
        snapshot = self._to_dict()
        try:
            if hasattr(self, 'app') and self.app is not None and hasattr(self.app, 'model') and hasattr(self.app.model, 'has_changed'):
                self.app.model.has_changed = True
        except Exception as e:
            logma.warning(f'save: could not mark app model as changed: {e}')
        return snapshot

    def set_channel(self) -> Any:
        """"""
        self.channel = NchantdWebChannel(self)
        self.backend = NchantdSafeFunction()
        self.channel.registerObject('backend', self.backend)
        self.browser.page().setWebChannel(self.channel)
        return self

    def set_interceptor(self) -> None:
        """"""
        interceptor = NchantdRequestInterceptor()
        pyqt.QWebEngineProfile.defaultProfile().setUrlRequestInterceptor(interceptor)
        if self.browser.page():
            self.browser.page().profile().setUrlRequestInterceptor(interceptor)

    def set_persistence(self) -> Any:
        """"""
        if hasattr(self.browser.page().profile(), 'set_persistence'):
            self.browser.page().profile().set_persistence()
        return self

    def set_url_path(self, url=None) -> Any:
        """"""
        self.default_url = self.config.dikt.get('default_url', 'https://www.duckduckgo.com/')
        self.home_url = self.config.dikt.get('home_url', self.default_url)
        if url is None:
            url = self.config.dikt.get('url', self.home_url)
        if self.active_url is not None:
            if self.active_url.is_equal(url):
                return self
        if not isinstance(url, pyqt.QUrl):
            url = NchantdURL(url, self)
        self.active_url = url
        self.save()
        return self

    def store_browse_history(self, content, page=0, entry=0) -> None:
        """"""
        today = dt.datetime.now().strftime('%Y%m%d')
        file_name = f'{today}-browse-history'
        payload = [[uuid(), 'dictionary', file_name, 'doc_media|doc_media_content', 'internal', 'clear|text|utf-8']]
        self._store_media(payload, page, entry, content)

    def take_screenshot(self) -> Any:
        logma.info(f'take_screenshot called')
        return self

    def _to_dict(self):
        """Return a snapshot of the viewer's state for save/restore.

        The snapshot includes the active URL, the current page title,
        and a hash of the URL history so the app can detect changes
        without storing the full history in the snapshot.
        """
        snapshot = {
            'current_url': self.active_url.url if self.active_url is not None else None,
            'title': self.browser.title() if hasattr(self, 'browser') and self.browser is not None else None,
            'profile_name': self.profiles.get('name', None) if hasattr(self, 'profiles') else None,
            'pinned': self.pinned_url.url if self.pinned_url is not None else None,
        }
        return snapshot


class NchantdWebBrowser(NchantdWebViewer):
    """An Nchantd WebApp provides access to a web url that acts as an application integrating features into the widget
    where appropriate and maintaining the link to that web app domain
    TODO: need to keep track of web addresses so that when a user logs into a service for a web app the link redirects
    to the all ready logged in page
    """

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdWebBrowser').override(cfg))
        self.back_button = None
        self.url_select_entry = None
        self.forward_button = None
        self.history_button = None
        self.profile_select_entry = None
        self.refresh_button = None
        self.save_button = None
        self.snapshot_button = None
        self.system_browser_launch_button = None
        self.web_settings_button = None

    def initModel(self, cfg=None) -> Any:
        """"""
        if isinstance(cfg, str):
            url = cfg
            cfg = {'url': url}
        if cfg is None:
            cfg = {}
        if 'url' not in cfg:
            cfg['url'] = self.config.dikt.get('url', self.home_url)
        logma.info(cfg['url'])
        super().initModel(cfg)
        self.url_options = self.get_important_urls()
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        return self

    def initWidget(self, url=None) -> Any:
        """ """
        self.initModel(url)
        self.initView()
        return self

    def populate_document(self, url) -> Any:
        """"""
        super().populate_document(url)
        return self

    def set_url_path(self, url=None) -> Any:
        """"""
        super().set_url_path(url)
        if url is not None and self.url_select_entry is not None:
            if isinstance(url, pyqt.QUrl):
                url = url.toString()
            self.url_select_entry.combobox.setCurrentText(url)
            self.url_select_entry.update_options([url], False, False)
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
