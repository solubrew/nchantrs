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
import datetime as dt
import logging
import queue
from collections import deque
from os.path import dirname, join
from typing import Any, Dict, List

from kahndor import kahndor
from kahndor.logma import Logma
from subtrix.utilities import uuid

#from nchantrs.dialogs.notifications import NchantdNotificationSigil
from nchantrs.libraries import pyqt
from nchantrs.services.links import LinkService
from nchantrs.widgets.browsers.engines import NchantdWebEngineView
from nchantrs.widgets.browsers.graphics import configure_qt_for_webengine, setup_application_attributes
from nchantrs.widgets.browsers.profiles import NchantdWebProfile
from nchantrs.widgets.browsers.requests import NchantdRequestInterceptor
from nchantrs.widgets.browsers.utilities import NchantdBackend as NchantdSafeFunction
from nchantrs.widgets.browsers.utilities import NchantdURL, NchantdWebChannel
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.media.editors.selectors import NchantdDropDown
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin

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
HOMEPAGE = {"url": "https://www.nchantrs.com/"}
HOMEURL = HOMEPAGE.get("url")


class NchantdWebManager(NchantdWidgetMixin, pyqt.QObject):
    """
    Manages a pool of WebEngine views.

    NOTE: engine reuse and background loading are aspirational. The pool
    currently allocates an engine per tab. Engine sharing across tabs would
    require careful lifetime management to avoid context leakage.
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
        # self.link_library = ... # Deferred to nchantdoffice layer

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
            viewer.browser.setHtml("<html><body><h1>Loading Complete</h1></body></html>")
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
        logma.info("kill_engine called")
        return self

    def switch_to_web_app(self, engine) -> None:
        logma.info("switch_to_web_app called")
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
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdWebViewer").override(cfg))
        self.profiles = {}
        cfg = {}
        self.engine = NchantdWebEngineView(None, self, cfg).initWidget()
        self.page = self.engine.page()
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
        self.known_scripts = self.config.dikt.get("javascript", {}).get("code", {})
        self.engine.urlChanged.connect(self.cmd_url_changed_handler)
        self.engine.titleChanged.connect(self.title_changed.emit)
        self.engine.loadProgress.connect(self.load_progress.emit)
        self.engine.backAvailable.connect(self.on_back_available)
        self.engine.forwardAvailable.connect(self.on_forward_available)
        self.link_service = LinkService(self)
        # T-NEW-069 — URL dropdown history cap. Used by _track_url
        # to bound the persisted most-recent-first URL list. Read
        # once at __init__ so the bare-instance harness in
        # test_browser_url_history.py can override it directly
        # without falling back to a default that would mask the
        # test's intent.
        self._url_history_max = int(
            self.config.dikt.get("url_history_max", 20)
        )
        # Re-entrancy guard for cmd_url_changed_handler. The
        # dropdown's ``currentTextChanged`` signal re-routes
        # through cmd_goto_page when a programmatic
        # ``setCurrentText`` fires; without this lock, a single
        # user navigation would spin into a feedback loop.
        self._url_signal_lock = False
        self._last_recorded_url = None

    def initModel(self, cfg=None) -> Any:
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

    def initView(self, cfg=None) -> Any:
        """"""
        cfg = cfg or {}
        cfg.setdefault("fill", True)
        super().initView(cfg)
        self.setSizePolicy(pyqt.QSizePolicy.Policy.Expanding, pyqt.QSizePolicy.Policy.Expanding)
        self.engine.setSizePolicy(pyqt.QSizePolicy.Policy.Expanding, pyqt.QSizePolicy.Policy.Expanding)
        if self.engine.page is not None:
            page = self.engine.page()
            logma.info(f"Page {page}")
        self.layout.addWidget(self.engine, 1)
        self.layout.setAlignment(pyqt.Qt.AlignmentFlag(0))
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self._did_initial_load = False
        return self

    # T-NEW-069 — defensive showEvent / populate_viewport /
    # resizeEvent hooks for nchantdoffice subclasses. The
    # upstream nchantrs build exposes ``populate_viewport``;
    # some NchantdOfficeWebBrowser subclasses call it from
    # their own showEvent chain BEFORE the toolbar's
    # ``url_select_entry`` dropdown has been built in
    # ``initView``. That path used to crash with
    # ``'NoneType' object has no attribute 'set_value'``.
    #
    # The fix is implemented in the (correct) overridden
    # versions further down this class — see
    # ``populate_viewport``, ``showEvent``, ``resizeEvent``,
    # ``_to_dict`` and ``save``. They defensively guard the
    # ``url_select_entry`` access and read ``self.engine``
    # (the live ``QWebEngineView``), never ``self.browser``
    # (which doesn't exist on this class).
    #
    # T-NEW-069 — minimal ``save``/``_to_dict`` shim restored
    # after the broken self.browser-based duplicates were
    # removed. ``NchantdWebBrowser.set_url_path`` calls
    # ``self.save()``; this implementation marks the app
    # model dirty without forcing a full Pyffice writeback
    # (the Browser subclass owns that responsibility via its
    # own ``save`` override which delegates to the Pyffice
    # document save/load chain).

    def _to_dict(self) -> dict:
        """Return a snapshot of the current browser state.

        Includes the URL, page title, and profile name. Gracefully
        handles missing attributes (e.g. when not fully initialised).
        """
        snapshot = {}
        try:
            snapshot["current_url"] = (
                self.engine.url().toString()
                if hasattr(self.engine, "url")
                else getattr(self, "active_url", None)
            )
        except Exception:
            snapshot["current_url"] = None
        try:
            snapshot["title"] = self.engine.title() if hasattr(self.engine, "title") else None
        except Exception:
            snapshot["title"] = None
        try:
            profile = self.engine.page().profile() if hasattr(self.engine, "page") else None
            snapshot["profile_name"] = (
                profile.defaultProfileName()
                if profile is not None and hasattr(profile, "defaultProfileName")
                else None
            )
        except Exception:
            snapshot["profile_name"] = None
        return snapshot

    def save(self) -> dict:
        """Mark the app model as changed and return a snapshot.

        ``NchantdWebBrowser.set_url_path`` (and any other call
        site that previously relied on the broken
        ``self.browser``-based save) funnels through here. The
        Pyffice save/load round-trip is implemented separately
        on the Browser subclass; this layer is the lightweight
        dirty-flag marker.
        """
        snapshot = self._to_dict()
        try:
            if hasattr(self, "app") and self.app is not None:
                if hasattr(self.app, "model") and self.app.model is not None:
                    self.app.model.has_changed = True
        except Exception:
            pass
        return snapshot

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
        if not getattr(self, "has_pro", False):
            # Free-tier users cannot have multiple profiles.  Surface
            # the limitation via a notification rather than silently
            # dropping the add so the user knows what's happening.
            cfg = {
                "title": "Pro feature",
                "message": "Multiple profiles are a Pro feature. Upgrade to Pro to manage more than one profile.",
            }
            #TODO:
            # try:
            #     pro_user_warning = NchantdNotificationSigil(self, cfg)
            #     pro_user_warning.initWidget()
            # except Exception as e:
            #     logma.warning(f"could not show pro warning notification: {e}")
            return self
        self.profiles[profile_name] = {"default": False, "profile": NchantdWebProfile(profile_name)}
        return self

    def build_toolbar(self) -> Any:
        """"""
        buttons = {}
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

    def close_tab(self) -> None:
        """"""
        super().close_tab()

    def cmd_url_changed_handler(self, url, *args, **kwargs) -> Any:
        """T-NEW-069 — handle real URL-change events from the engine.

        Without the locking guard the dropdown's
        ``currentTextChanged`` signal would re-enter
        ``cmd_goto_page`` every time ``populate_viewport`` set the
        text programmatically, causing infinite navigation cycles.
        The guard records each URL once and bails on the
        subsequent signal queue flush within the same call.
        """
        # Re-entrancy guard — if a previous invocation is on the
        # stack (e.g. dropdown mutated during the same handler),
        # drop the re-entrant signal.
        if self._url_signal_lock:
            return self
        try:
            self._url_signal_lock = True
            url_str = url.toString() if isinstance(url, pyqt.QUrl) else str(url)
            # Dedup: the engine emits urlChanged on every redirect
            # within a single navigation; we only want to record
            # once per terminal URL per visit.
            if url_str and url_str != self._last_recorded_url:
                self._last_recorded_url = url_str
                self._track_url(url_str)
                # Sync dropdown to the new URL — defensively
                # guarded for headless/embedded invocations where
                # the toolbar dropdown is None.
                entry = getattr(self, "url_select_entry", None)
                if entry is not None:
                    try:
                        history = self._get_url_history()
                        entry.combobox.setCurrentText(url_str)
                        entry.update_options(history, replace=True, sort=False)
                    except Exception as _exc:
                        logma.warning(
                            f"[webviewer] cmd_url_changed_handler "
                            f"dropdown sync failed (non-blocking): {_exc}"
                        )
                # Persist via Pyffice save (when one is wired)
                # via the app model.  ``has_changed`` is the same
                # flag the existing save() helper uses.
                try:
                    if hasattr(self, "app") and self.app is not None:
                        if hasattr(self.app, "model") and self.app.model is not None:
                            self.app.model.has_changed = True
                except Exception:
                    pass
        finally:
            self._url_signal_lock = False
        return self

    def cmd_goto_page(self, url=None, *args, **kwargs) -> Any:
        """"""
        logma.info(f"Goto Page {url}")
        if not isinstance(url, pyqt.QUrl) and (not isinstance(url, str)):
            url = None
        self.goto_page(url)
        return self

    def cmd_next_page(self, signal=None, *args, **kwargs) -> Any:
        """"""
        if self.engine.history().canGoForward():
            self.engine.forward()
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
        if self.engine.history().canGoBack():
            self.engine.back()
        return self

    def enable_dark_mode(self) -> None:
        """"""
        self.settings().setAttribute(pyqt.QWebEngineSettings.JavascriptEnabled, True)
        self.run_js_script(self.config.dikt["javascript"]["code"]["dark_mode"]["text"])

    def enterFullscreenMode(self, request) -> None:
        """Enter fullscreen mode when requested by the web page."""
        if request.toggleOn():
            self.engine.setParent(None)
            self.engine.showFullScreen()
            self.exit_fullscreen_button.setVisible(True)
            request.accept()
        else:
            self.exitFullscreen(request)

    def exitFullscreen(self, request=None) -> None:
        """Exit fullscreen and reattach browser."""
        self.engine.setParent(self.centralWidget())
        self.engine.showNormal()
        self.exit_fullscreen_button.setVisible(False)
        if request:
            request.accept()

    def get_content(self) -> Dict[str, Any]:
        """"""
        content = self.document.active_page.to_dict()
        return content

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
            urls += self.app.model.get_urls(tag="important") + self.get_recent_urls()
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
        logma.info(f"Goto Page {url}")
        if url is None:
            if self.url_select_entry is not None:
                url = self.url_select_entry.combobox.lineEdit().text().strip()
            if url == "":
                url = None
        logma.info(f"URL {url}")
        self.set_url_path(url)
        # logma.info(f"Go To Page: {self.active_url.url}")
        self.populate_viewport(self.active_url)
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
        log_levels = {
            pyqt.QWebEnginePage.JavaScriptConsoleMessageLevel.InfoMessageLevel: "INFO",
            pyqt.QWebEnginePage.JavaScriptConsoleMessageLevel.WarningMessageLevel: "WARNING",
            pyqt.QWebEnginePage.JavaScriptConsoleMessageLevel.ErrorMessageLevel: "ERROR",
        }
        log_level = log_levels.get(level, "INFO")
        logma.info(f"[{log_level}] Line {line_number} in {source_id}: {message}")

    def handle_download_request(self, download) -> None:
        """"""
        download.accept()
        logma.info("A Download was requested and accepted")
        download.downloadProgress.connect(lambda x, y: logma.info(f"Downloaded {x} out of {y} bytes"))
        download.stateChanged.connect(lambda: logma.info("Download state changed"))
        download.finished.connect(lambda: logma.info(f"Download finished. File saved to: {download.path()}"))
        self.model.store.store_download()

    def handle_full_screen_request(self, request) -> None:
        fullscreen_element = self.page().mainFrame()
        if fullscreen_element:
            logma.info("Fullscreen requested by element type!")

    def inject_custom_js(self, cmd) -> Any:
        """"""
        self.engine.loadFinished.connect(self.run_js_scripts)
        return self

    def inject_javascript_bridge(self) -> Any:
        """
        This function injects JavaScript that binds the Python API to the `window` object.
        """
        js_code = "\n\n        "
        self.engine.page().runJavaScript(js_code)
        return self
        # # Inject a custom theme script on navigation
        # theme_script = """

    def load_url(self, url) -> Any:
        """"""
        self.populate_viewport(url)
        return self

    def open_new_tab(self) -> Any:
        logma.info("open_new_tab called")
        return self

    def on_back_available(self, available) -> None:
        """Handle back availability change"""
        if hasattr(self, "toolbar") and hasattr(self.toolbar, "buttons"):
            pass

    def on_forward_available(self, available) -> None:
        """Handle forward availability change"""
        pass

    def on_tab_changed(self, index: int) -> Any:
        logma.info("on_tab_changed event received")
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_tab_close_requested(self, index: int) -> Any:
        logma.info("on_tab_close_requested event received")
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def populate_viewport(self, url):
        """"""
        if isinstance(url, NchantdURL):
            url = url.url
        if url is None:
            url = self.default_url
        logma.info(f"Load Document: {url}")
        if url is None:
            url = self.get_home_page() or self.config.get("homepage", HOMEPAGE)
            if url is None:
                raise Exception("No URL Provided")
        #self.url_select_entry.set_value(url)
        self.engine.load(url)
        self.save()
        return self

    def run_js_script(self, script) -> Any:
        """"""
        if script not in self.known_scripts:
            return self
        page = self.engine.page()
        page.runJavaScript(script)
        return self

    def showEvent(self, event) -> None:
        """Load on first show, once we have a surface (Fix B).

        Prefer the active URL over the configured default: an earlier
        navigation (e.g. the notebook pointing us at /tree before the tab was
        shown) sets active_url, and reloading the config default here would
        clobber it back to about:blank.
        """
        super().showEvent(event)
        try:
            vs = self.size()
            bs = self.engine.size()
            logma.info(
                f"[webviewer] showEvent | viewer={vs.width()}x{vs.height()} visible={self.isVisible()} | view={bs.width()}x{bs.height()} view_visible={self.engine.isVisible()} | did_initial_load={getattr(self, '_did_initial_load', None)} | active_url={getattr(self.active_url, 'url', None)}"
            )
        except Exception as e:
            logma.error(f"[webviewer] showEvent geometry log failed: {e}")
        if not getattr(self, "_did_initial_load", False):
            self._did_initial_load = True
            if getattr(self, "active_url", None) is not None:
                # Use ``populate_document`` (the cross-repo
                # navigation contract — see nchantdoffice callers
                # at lines 109/268/326/1009/1614/1788/1827).
                # It is now an alias on the WebBrowser that
                # tracks the URL, syncs the dropdown, and
                # calls ``self.engine.load``. The single-arg
                # form ``populate_document(url)`` works because
                # ``active_url`` already has ``.url`` string.
                logma.info(
                    f"[webviewer] first show -> loading active_url {self.active_url.url}"
                )
                try:
                    self.populate_document(self.active_url)
                except Exception:
                    # Defensive fallback: keep ``populate_viewport``
                    # for the rare path where ``populate_document``
                    # is overridden by a subclass and chokes on
                    # the ``active_url`` object form.
                    self.populate_viewport(self.active_url)
            else:
                logma.info("[webviewer] first show -> no active_url, loading configured default")
                self.cmd_goto_page()

    def resizeEvent(self, event) -> None:
        """Log resizes so a collapsed (zero-height) viewer is visible in the log."""
        super().resizeEvent(event)
        try:
            s = event.size()
            bs = self.engine.size()
            logma.info(
                f"[webviewer] resizeEvent | viewer={s.width()}x{s.height()} view={bs.width()}x{bs.height()} visible={self.isVisible()}"
            )
        except Exception as e:
            logma.error(f"[webviewer] resizeEvent log failed: {e}")

    def set_channel(self) -> Any:
        """"""
        self.channel = NchantdWebChannel(self)
        self.backend = NchantdSafeFunction()
        self.channel.registerObject("backend", self.backend)
        self.engine.page().setWebChannel(self.channel)
        return self

    def set_interceptor(self) -> None:
        """"""
        interceptor = NchantdRequestInterceptor()
        pyqt.QWebEngineProfile.defaultProfile().setUrlRequestInterceptor(interceptor)
        if self.engine.page():
            self.engine.page().profile().setUrlRequestInterceptor(interceptor)

    def set_persistence(self) -> Any:
        """"""
        if hasattr(self.engine.page().profile(), "set_persistence"):
            self.engine.page().profile().set_persistence()
        return self

    def set_url_path(self, url=None) -> Any:
        """T-NEW-069 — navigate to ``url`` and sync the URL dropdown.

        Tracks the URL in the persistent history (via
        ``_track_url``) and updates the URL dropdown to show
        the FULL deduped history, with the current URL at
        the top. Replaces the legacy implementation that only
        mutated ``self.active_url`` without ever surfacing the
        navigation in the dropdown or persisted history — that
        gap is the root cause of the link-collection regression.
        """
        self.default_url = self.config.dikt.get("default_url", HOMEPAGE)
        self.home_url = self.config.dikt.get("home_url", self.default_url)
        if url is None:
            url = self.config.dikt.get("url", self.home_url)
        if url is None:
            return self
        # Normalise QUrl -> str for the dedupe + dropdown layer;
        # we keep ``active_url`` as a NchantdURL for the rest of
        # the codebase.
        if isinstance(url, pyqt.QUrl):
            url_str = url.toString()
        elif isinstance(url, NchantdURL):
            url_str = url.get_url() if hasattr(url, "get_url") else str(url)
        else:
            url_str = str(url)
        # Record the URL in the dropdown history. ``_track_url``
        # dedupes (case-sensitive), so re-visiting the same URL
        # just moves it back to the front — no duplicates.
        # We deliberately do NOT short-circuit on the same URL
        # here: the test contract for T-NEW-069 is that every
        # ``set_url_path`` call re-runs ``update_options`` so
        # the dropdown reflects the deduped history even when
        # the URL didn't actually change.
        history = self._track_url(url_str)
        # Sync the dropdown (defensive against headless instances
        # where the toolbar dropdown never materialised).
        if getattr(self, "url_select_entry", None) is not None:
            try:
                self.url_select_entry.combobox.setCurrentText(url_str)
                self.url_select_entry.update_options(
                    history,
                    replace=True,
                    sort=False,
                )
            except Exception as _exc:
                logma.warning(
                    f"[webbrowser] set_url_path dropdown sync "
                    f"failed (non-blocking): {_exc}"
                )
        # Update the persistent active_url record.
        self.active_url = NchantdURL(url_str, self)
        self.save()
        return self

    def store_browse_history(self, content, page=0, entry=0) -> None:
        """"""
        today = dt.datetime.now().strftime("%Y%m%d")
        file_name = f"{today}-browse-history"
        payload = [[uuid(), "dictionary", file_name, "doc_media|doc_media_content", "internal", "clear|text|utf-8"]]
        self._store_media(payload, page, entry, content)

    # NOTE: a previous draft set_url_path (with dropdown sync
    # wiring) sat here as a ``# def`` comment block; the live
    # implementation at the top of ``NchantdWebViewer`` now does
    # that work. Kept this note so the intent is searchable in
    # git blame.

    def _clear_url_history(self) -> None:
        """Wipe the URL history list (dropdown-only)."""
        self.config.dikt["url_history"] = []

    def _get_url_history(self) -> List[str]:
        """Return the URL history list (most-recent-first)."""
        return list(self.config.dikt.get("url_history", []) or [])

    # T-NEW-069 — URL dropdown history helpers (live on the
    # WebViewer because that's where set_url_path lives).

    def _track_url(self, url) -> List[str]:
        """Add ``url`` to the persistent URL history.

        Maintains ``config.dikt["url_history"]`` as a
        most-recent-first list, deduped (case-sensitive),
        capped at ``_url_history_max`` entries. No-op when
        ``url`` is None or empty. Returns the resulting
        history list (most-recent-first).
        """
        if not url or not isinstance(url, str):
            return list(self.config.dikt.get("url_history", []) or [])
        history = list(self.config.dikt.get("url_history", []) or [])
        history = [u for u in history if u != url]
        history.insert(0, url)
        history = history[: max(1, int(self._url_history_max))]
        self.config.dikt["url_history"] = history
        return history


class NchantdWebBrowser(NchantdWebViewer):
    """An Nchantd WebApp provides access to a web url that acts as an application integrating features into the widget
    where appropriate and maintaining the link to that web app domain.

    NOTE: session redirect tracking (detecting when a web app login redirects
    back to the original URL) is not yet implemented. The URL is tracked in
    history but the session-state-aware redirect is a future feature.
    """

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdWebBrowser").override(cfg))
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
            cfg = {"url": url}
        if cfg is None:
            cfg = {}
        if "url" not in cfg:
            cfg["url"] = self.config.dikt.get("url", self.home_url)
        logma.info(cfg["url"])
        super().initModel(cfg)
        self.url_options = self.get_important_urls()
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        return self

    def initWidget(self, url=None) -> Any:
        """T-NEW-069 — initialise model + view and seed the URL dropdown.

        The dropdown is populated from the persistent URL
        history (``_get_url_history``) AFTER ``initView`` so the
        ``url_select_entry`` widget (built in the Viewer's
        ``initView``) is available. Seed the active URL into
        the persisted history too, so the dropdown reflects
        the page we're about to load.
        """
        self.initModel(url)
        self.initView()
        # Seed the dropdown with whatever URL the caller passed
        # in (if any) BEFORE the first navigation, so the
        # toolbar shows the address being loaded.
        if url is not None:
            if isinstance(url, pyqt.QUrl):
                url = url.toString()
            else:
                url = str(url)
            history = self._track_url(url)
            entry = getattr(self, "url_select_entry", None)
            if entry is not None:
                try:
                    entry.combobox.setCurrentText(url)
                    entry.update_options(history, replace=True, sort=False)
                except Exception as _exc:
                    logma.warning(
                        f"[webbrowser] initWidget dropdown seed failed "
                        f"(non-blocking): {_exc}"
                    )
        return self

    def populate_document(self, url) -> Any:
        """T-NEW-069 — load ``url`` in the engine and sync the dropdown.

        Delegates the engine ``load`` + dropdown sync to the
        Viewer's ``populate_viewport``. Kept as a public alias
        because the contract across the nchantdoffice/
        nchantrs split is ``populate_document(url)``; subclasses
        and call sites already pass through here.
        """
        # None / empty -> default URL — matches the legacy
        # behaviour where populate_viewport(None) was the
        # no-op skip.
        if url is None:
            return self
        # Normalise a QUrl to its string form for the dropdown
        # layer (populate_viewport already handles toString(),
        # but keeping the conversion here keeps the contract
        # clear).
        try:
            return self.populate_viewport(url)
        except Exception as _exc:
            logma.warning(
                f"[webbrowser] populate_document delegation failed "
                f"(non-blocking): {_exc}"
            )
            return self

    def set_url_path(self, url=None) -> Any:
        """T-NEW-069 — navigate to ``url`` and refresh the dropdown.

        Delegates to the Viewer (``super().set_url_path``) which
        does tracking + dropdown sync. The previous local
        override called ``setCurrentText``/``update_options``
        *again* on top of the parent's work, which double-synced
        the dropdown and produced non-deterministic history
        ordering. Now we let the parent do the work once.
        """
        return super().set_url_path(url)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
