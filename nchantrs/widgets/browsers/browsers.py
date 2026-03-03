# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Nchantrs@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""  #																			||
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
from os import environ
from collections import deque
import datetime as dt
import queue
from os.path import dirname, join
from os import environ
from collections import deque
import datetime as dt
import queue

# Initialize Qt environment BEFORE importing PyQt modules
from nchantrs.widgets.browsers.graphics import configure_qt_for_webengine, setup_application_attributes

configure_qt_for_webengine()

# ===============================================================================||

# ===============================================================================||
from condor import condor
from subtrix.utilities import uuid
from nchantrs.dialogs.notifications import NchantdNotificationSigil
from nchantrs.libraries import pyqt
from nchantrs.widgets.browsers.engines import NchantdWebEngineView

# from nchantrs.widgets.browsers.pages import NchantdWebPage
from nchantrs.widgets.browsers.profiles import NchantdWebProfile
from nchantrs.widgets.browsers.requests import NchantdRequestInterceptor
from nchantrs.widgets.browsers.utilities import NchantdURL, NchantdWebChannel
from nchantrs.widgets.media.editors.selectors import NchantdDropDown
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from ogma.logma import Logma
from pyffice.web.url import PyfficeURLLibrary

# Set up Qt attributes after importing pyqt but before creating any widgets
try:
    setup_application_attributes()
except Exception as e:
    from ogma.logma import Logma

    logma = Logma(__name__)
    logma.warning(f"Could not set all Qt attributes: {e}")

from nchantrs.widgets.browsers.engines import NchantdWebEngineView

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
# logma.off()

# ===============================================================================||
pxcfg = join(here, "_data_", "browsers.yaml")


class NchantdWebManager(NchantdWidgetMixin, pyqt.QThread):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdWebManager")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.available_engines = queue.Queue([])
        self.active_engines = queue.Queue([])
        cfg = {}
        self.link_library = PyfficeURLLibrary(cfg)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        self.create_engines()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def create_engines(self):
        """"""
        wip_engine_size = 3
        for i in range(wip_engine_size - len(self.available_engines)):
            viewer = NchantdWebViewer(self)
            viewer.setHtml("<html><body><h1>Loading Complete</h1></body></html>")
            self.available_engines.put(viewer)

    def get_available_engine(self):
        """"""
        engine = self.available_engines.pop()
        self.create_engines()
        return engine

    def kill_engine(self):
        """"""

    def switch_to_web_app(self, engine):
        """
        TODO: change from browser/viewer to web app use the same engine but place it in a new Viewer Subclas
        :param engine:
        :return:
        """


class NchantdWebViewer(NchantdWidget):
    """ """

    link_hovered = pyqt.Signal(str)
    load_progress = pyqt.Signal(int)
    title_changed = pyqt.Signal(str)
    url_changed = pyqt.Signal(pyqt.QUrl)
    # fav_icon_changed = pyqt.Signal(pyqt.QIcon)
    # web_action_enabled_changed = pyqt.Signal(pyqt.QWebEnginePage.WebAction, bool)
    # dev_tools_requested = pyqt.Signal(pyqt.QWebEnginePage)
    # find_text_finished = pyqt.Signal(pyqt.QWebEngineFindTextResult)

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdWebViewer"))
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.profiles = {}
        # self.default_profile = NchantdWebProfile(self.app.model.user.name, None, True)
        # self.default_profile = NchantdWebProfile.defaultProfile()
        # logma.info(f"Environment Variables: {environ["QTWEBENGINE_CHROMIUM_FLAGS"]}")
        cfg = {}
        self.browser = NchantdWebEngineView(None, self, cfg).initWidget()
        # cfg = {}
        # self.profile = NchantdWebProfile(self.app.model.slug, self.browser, False, self, cfg)
        # if self.profile.persistence is False:
        #     self.profile.initProfile()
        # cfg = {}
        # page = NchantdWebPage(self, self.profile, True, cfg).initWidget()
        # self.browser.setPage(page)
        # self.set_persistence()
        self.page = None
        # self.profiles[self.app.model.user.name] = {"default": True, "profile": self.profile}
        self.que = deque([])
        self.fque = deque([])
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
        self.known_scripts = self.config.dikt["javascript"]["code"]
        self.has_pro = self.app.model.user.has_pro
        self.browser.urlChanged.connect(self.cmd_url_changed_handler)

    def initModel(self, cfg=None):
        """"""
        self.config.override(cfg)
        super().initModel()
        self.is_app = self.config.dikt.get("is_app", False)
        if self.is_app is True:
            self.is_simple = self.config.dikt.get("is_simple", True)
        else:
            self.is_simple = self.config.dikt.get("is_simple", False)
        self.set_url_path(self.config.dikt.get("url", None))
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        # if self.page is None:
        #     page = None if self.config.dikt.get("page", None) is None else self.config.dikt["page"]
        #     self.set_page(page)
        self.browser.setSizePolicy(pyqt.QSizePolicy.Policy.Expanding, pyqt.QSizePolicy.Policy.Expanding)
        self.cmd_goto_page()
        # Access the page and connect the signal
        page = self.browser.page()  # Get QWebEnginePage object
        logma.info(f"Page {page}")
        # page.javaScriptConsoleMessage.connect(self.handle_console_message)  # Connect the signal
        self.layout.addWidget(self.browser)
        self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        return self

    def initWidget(self, url=None):
        """ """
        self.initModel(url)
        self.initView()
        return self

    def add_profile(self, profile_name):
        """"""
        if not self.has_pro:
            # TODO create user warning system and tell them that only pro users can have multiple profiles
            cfg = {}
            pro_user_warning = NchantdNotificationSigil(self, cfg)
            pro_user_warning.initWidget()
            return self
        self.profiles[profile_name] = {"default": False, "profile": NchantdWebProfile(profile_name)}
        return self

    def build_toolbar(self):
        """"""
        buttons = {}
        if self.is_simple is False:
            # TOOD this shouldl be in the NchantdOffice Browser not here
            if self.has_pro:
                cfg = {
                    "label": "Profile",
                    "layout": "horizontal",
                    "size": [10, 20],
                    "drop_down": {"size": [100, 20]},
                    "options": ["default"],
                }
                self.profile_select_entry = NchantdDropDown(self, cfg).initWidget()
                buttons[0] = {"name": "get_pro", "widget": self.profile_select_entry}
            else:
                cfg = {
                    "text": "Get Pro",
                    "handler": self.app.view.switch_to_account_tab,
                    "height": 24,
                }
                self.profile_select_entry = NchantdButton(self, cfg).initWidget()
                buttons[10] = {"name": "get_pro_features", "widget": self.profile_select_entry}

        buttons[11] = {"action": "web_page_back", "handler": self.cmd_previous_page}
        buttons[12] = {"action": "web_page_forward", "handler": self.cmd_next_page}
        buttons[13] = {"action": "web_page_refresh", "handler": self.cmd_refresh_page}
        buttons[14] = {
            "name": "select_url",
            "label": "URL",
            "layout": "horizontal",
            "size": [30, 30],
            "combobox": {"size": [500, 30], "options": self.get_url_history()},
            "type": "dropdown",
            "handler": self.cmd_goto_page,
            "value": self.get_current_url(),
        }
        self.url_select_entry = NchantdDropDown(self, buttons[14])
        buttons[14]["widget"] = self.url_select_entry
        buttons[15] = {"action": "web_page_go", "handler": self.cmd_goto_page}
        buttons[49] = "_insert_stretch"
        buttons[150] = "_skip"
        buttons[200] = "_skip"
        return buttons

    def close_tab(self):
        """"""
        super().close_tab()

    # @pyqt.Slot()
    # def navigate_to_url(self):
    #     """Navigate to URL from input field"""
    #     url_text = self.url_input.text().strip()
    #     if url_text:
    #         self.web_view.navigate_to_url(url_text)
    #
    # @pyqt.Slot(pyqt.QUrl)
    # def update_url_input(self, url):
    #     """Update URL input field when navigation occurs"""
    #     self.url_input.setText(url.toString())

    def cmd_url_changed_handler(self, url, *args, **kwargs):
        """"""
        logma.info(f"URL Changed: {url}")
        if self.lock is True:
            self.open_new_tab()
        if isinstance(url, pyqt.QUrl):
            url = url.toString()
        self.set_url_path(url)
        logma.info(f"URL Changed: {url}")
        self.save()
        return self

    def cmd_goto_page(self, url=None, *args, **kwargs):
        """"""
        logma.info(f"Goto Page {url}")
        if not isinstance(url, pyqt.QUrl) and not isinstance(url, str):
            url = None
        self.goto_page(url)
        return self

    def cmd_next_page(self, signal=None, *args, **kwargs):
        """"""
        if len(self.fque) > 0:
            next_url = self.fque.pop()
            self.goto_page(next_url)
        if len(self.fque) == 0:
            pass
            # TODO figure out to set the button this handler is connected to be disabled
        return self

    def cmd_make_webapp(self, signal, *args, **kwargs):
        """"""
        self.lock = True
        self.active_url.set_lock()
        # self.parent.switch_to_WebApp(self)
        return self

    def cmd_refresh_page(self, signal=None, *args, **kwargs):
        """"""
        self.cmd_goto_page()
        return self

    def cmd_previous_page(self, signal=None, *args, **kwargs):
        """"""
        if len(self.que) == 0:
            return self
        previous_url = self.que.pop()
        self.fque.append(previous_url)
        self.goto_page(previous_url)
        return self

    def enable_dark_mode(self):
        """"""
        self.settings().setAttribute(pyqt.QWebEngineSettings.JavascriptEnabled, True)
        self.run_js_script(self.config.dikt["javascript"]["code"]["dark_mode"]["text"])

    def enterFullscreenMode(self, request):
        """Enter fullscreen mode when requested by the web page."""
        if request.toggleOn():
            self.browser.setParent(None)  # Detach from the main layout
            self.browser.showFullScreen()
            request.accept()  # Accept the fullscreen request
        else:
            self.browser.setParent(self.centralWidget())  # Reattach to the main layout
            self.browser.showNormal()
            request.accept()  # Accept the fullscreen exit request
        if request.toggleOn():
            # Detach browser and enter fullscreen
            self.browser.setParent(None)
            self.browser.showFullScreen()
            self.exit_fullscreen_button.setVisible(True)
            request.accept()
        else:
            # Exit fullscreen
            self.exitFullscreen(request)

    def exitFullscreen(self, request=None):
        """Exit fullscreen and reattach browser."""
        self.browser.setParent(self.centralWidget())
        self.browser.showNormal()
        self.exit_fullscreen_button.setVisible(False)
        if request:
            request.accept()

    def get_url_history(self):
        """
        get a datafraome of the historically visited urls with a smart system showing a combination of recent
        and most visited urls
        :return:
        """
        urls = []
        return urls

    def get_important_urls(self):
        """"""
        urls = []
        if self.active_url is not None:
            urls += [self.active_url.path]
        urls += self.app.model.get_urls(tag="important") + self.get_recent_urls()
        urls = list(set(urls))
        return urls

    def get_recent_urls(self):
        """"""
        urls = []
        return urls

    def get_current_url(self):
        """"""
        if self.active_url is None:
            return self.default_url
        url = self.active_url.path
        return url

    def goto_page(self, url):
        """"""
        logma.info(f"Goto Page {url}")
        if url is None:
            if self.url_select_entry is not None:
                url = self.url_select_entry.combobox.lineEdit().text().strip()
            if url == "":
                url = None
        logma.info(f"URL {url}")
        self.set_url_path(url)
        logma.info(f"Go To Page: {self.active_url.url}")
        self.populate_document(self.active_url)
        return self

    def handle_console_message(self, level, message, line_number, source_id):
        """
        Handles JavaScript console messages and outputs them to Python console.

        Args:
            level (QWebEnginePage.JavaScriptConsoleMessageLevel): Log level (e.g., INFO, WARNING, ERROR).
            message (str): The actual message from the JavaScript console.
            line_number (int): Line number in the JavaScript file where the message originated.
            source_id (str): The JavaScript file or source identifier where the message was generated.
        """
        log_levels = {
            pyqt.QWebEnginePage.JavaScriptConsoleMessageLevel.InfoMessageLevel: "INFO",
            pyqt.QWebEnginePage.JavaScriptConsoleMessageLevel.WarningMessageLevel: "WARNING",
            pyqt.QWebEnginePage.JavaScriptConsoleMessageLevel.ErrorMessageLevel: "ERROR",
        }

        # Get log level name, default to 'INFO'
        log_level = log_levels.get(level, "INFO")

        # Print the message in Python console
        logma.info(f"[{log_level}] Line {line_number} in {source_id}: {message}")

    def handle_download_request(self, download):
        """"""
        download.accept()
        logma.info("A Download was requested and accepted")
        download.downloadProgress.connect(lambda x, y: logma.info(f"Downloaded {x} out of {y} bytes"))
        download.stateChanged.connect(lambda: logma.info("Download state changed"))
        download.finished.connect(lambda: logma.info(f"Download finished. File saved to: {download.path()}"))
        self.model.store.store_download()

    def handle_full_screen_request(self, request):
        fullscreen_element = self.page().mainFrame()
        if fullscreen_element:  # Check the requested element
            logma.info("Fullscreen requested by element type!")
        # Continue request handling as implemented above

    def inject_custom_js(self, cmd):
        """"""
        self.browser.loadFinished.connect(self.run_js_scripts)
        return self

    def inject_javascript_bridge(self):
        """
        This function injects JavaScript that binds the Python API to the `window` object.
        """
        js_code = """

        """
        # Execute the setup script in WebKit
        self.browser.page().runJavaScript(js_code)
        return self
        # # Inject a custom theme script on navigation
        # theme_script = """

        # """
        # self.runJavaScript(theme_script)

    def open_new_tab(self):
        """"""
        self.panes["toolbar"].add_document(args=[{"action": action}])
        return self

    def on_tab_changed(self, index: int):
        # Pause/mute every other tab, resume/unmute the active one
        for i in range(self.tabs.count()):
            view: BrowserTab = self.tabs.widget(i)
            if i == index:
                view.resume_and_unmute()
            else:
                view.pause_and_mute()
        return self

    def on_tab_close_requested(self, index: int):
        view: BrowserTab = self.tabs.widget(index)
        if view:
            view.hard_stop()
            self.tabs.removeTab(index)
            view.deleteLater()
        return self

    def populate_document(self, url):
        """"""
        if isinstance(url, NchantdURL):
            url = url.url
        if url is None:
            url = self.default_url
        logma.info(f"Load Document: {url}")
        self.browser.load(url)
        self.save()
        return self

    def run_js_script(self, script):
        """"""
        if script not in self.known_scripts:
            return self
        page = self.browser.page()
        page.runJavaScript(script)
        return self

    def save(self):
        """"""
        return self

    def set_channel(self):
        """"""
        self.channel = NchantdWebChannel(self)
        self.backend = NchantdSafeFunction()
        self.channel.registerObject("backend", self.backend)
        self.page.setWebChannel(self.channel)
        return self

    def set_interceptor(self):
        """"""
        interceptor = NchantdRequestInterceptor()
        self.default_profile.setUrlRequestInterceptor(interceptor)
        if self.page is None:
            self.set_page()
        self.page.setUrlRequestInterceptor(interceptor)

    # def set_page(self, page=None):
    #     """"""
    #     if page is None:
    #         page = NchantdWebPage
    #     self.page = page(self, self.profile, self.browser)
    #     self.browser.setPage(self.page)
    #     return self

    def set_persistence(self):
        """"""
        self.profile.set_persistence()
        return self

    def set_url_path(self, url=None):
        """"""
        self.default_url = self.config.dikt.get("default_url", "https://www.duckduckgo.com/")
        self.home_url = self.config.dikt.get("home_url", self.default_url)
        if url is None:
            url = self.config.dikt.get("url", self.home_url)
        if self.active_url is not None:
            if self.active_url.is_equal(url):
                return self
        if not isinstance(url, pyqt.QUrl):
            url = NchantdURL(url, self)
        # if self.active_url is not None and self.page.is_main_frame is True:
        #     # if self.active_url.is_valid():
        #     self.que.append(self.active_url.url)
        self.active_url = url
        self.save()
        return self

    def store_browse_history(self, content, page=0, entry=0):
        """"""
        today = dt.datetime.now().strftime("%Y%m%d")
        file_name = f"{today}-browse-history"
        payload = [
            [
                uuid(),
                "dictionary",
                file_name,
                "doc_media|doc_media_content",
                "internal",
                "clear|text|utf-8",
            ]
        ]
        self._store_media(payload, page, entry, content)

    def take_screenshot(self):
        """Create a Static image of the active url web page"""
        return self


class NchantdWebBrowser(NchantdWebViewer):
    """An Nchantd WebApp provides access to a web url that acts as an application integrating features into the widget
    where appropriate and maintaining the link to that web app domain
    TODO: need to keep track of web addresses so that when a user logs into a service for a web app the link redirects
    to the all ready logged in page
    """

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdWebBrowser")
        if parent:
            self.config.override(parent.config)
        super().__init__(self.parent, self.config)
        self.config.override(cfg)
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

    def initModel(self, cfg=None):
        """"""

        if cfg is None:
            cfg = {}
        cfg["url"] = self.config.dikt.get("url", self.home_url)
        logma.info(cfg["url"])
        super().initModel(cfg)
        self.url_options = self.get_important_urls()
        return self

    def initView(self, cfg=None):
        """"""

        super().initView(cfg)
        return self

    def initWidget(self, url=None):
        """ """
        self.initModel(url)
        self.initView()
        return self

    def populate_document(self, url):
        """"""
        super().populate_document(url)
        return self

    def set_url_path(self, url=None):
        """"""
        super().set_url_path(url)
        if url is not None:
            if isinstance(url, pyqt.QUrl):
                url = url.toString()
            self.url_select_entry.combobox.setCurrentText(url)
            self.url_select_entry.update_options([url], False, False)
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
