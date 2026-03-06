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
import time
import inspect

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from subtrix.utilities import uuid
from nchantrs.libraries import pyqt
from nchantrs.themes.themes import NchantdTheme
from nchantrs.widgets.widgets import loadWidget
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
logma.off()
# Enable file logging to track issues without requiring console
logma.activate_file_handler(filename="nchantrs_applicationviews.log")

# ====================================================================================================================||
pxcfg = join(abspath(here), "_data_", "applicationviews.yaml")


class NchantdPantiesView(object):
    """"""

    def __init__(self, parent, cfg=None):
        """"""
        super().__init__()
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdPantiesView").override(cfg)
        if self.parent:
            self.config.override(parent.config)
        self.theme = None
        self.themes = None
        self.themes_path = None
        self.layout = None
        self.pre_view_init_ran = False
        self.post_view_init_ran = False
        # Get app from parent - NchantdCape/NchantdPanties has .main attribute
        # Don't use QApplication.instance() directly as it lacks .main
        self.app = self.parent

    def init_pre_view(self):
        """ """
        self.theme = NchantdTheme(self.app.main)
        self.themes = self.theme.themes
        self.set_theme(self.config.dikt["gui"]["desktop"]["theme"])
        self.pre_view_init_ran = True

    def init_post_view(self):
        """"""
        self.post_view_init_ran = True

    def initView(self):
        """"""
        if not self.pre_view_init_ran:
            self.init_pre_view()
        self.layout = pyqt.QHBoxLayout()
        if not self.post_view_init_ran:
            self.init_post_view()
        return self

    def set_theme(self, theme="midnight_mist"):
        """"""
        self.theme.set_theme(theme)

    # def paintEvent(self, event):
    #     """"""
    #     qp = pyqt.QPainter()
    #     qp.begin(self)
    #     path = BackgroundImages().application
    #     pixmap = pyqt.QPixmap(path)
    #     qp.drawPixmap(self.rect(), pixmap)
    #     qp.end()


class NchantdCapeView(NchantdPantiesView):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdCapeView"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initView(self, cfg=None):
        """"""
        super().initView()
        return self


class NchantdCloakView(NchantdPantiesView):
    """ """

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdCloakView").override(cfg))
        if self.parent:
            self.config.override(parent.config)
        self.menus = {}
        self.gui = self.app.primaryScreen()
        self.screens = self.app.screens()
        self.splitter = pyqt.QSplitter(self.app.main)
        self.panes = {}
        self.status_bar = None
        _time = self.parent.model.store.time.today_long()
        version = self.parent.model.get_current_version()
        self.status_message = f"{self.parent.app.application_name} - version: {version} || {_time}  "
        self.new_account_wizard = None

    def initView(self):  # ||
        """Initialize UI setting the main application layout and building
        landing widgets"""
        super().initView()
        self.set_theme()
        self._set_configurations()
        self.set_toolbar()
        self.build_panes()
        self.layout.addWidget(self.splitter)
        self.add_status_bar()
        self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignLeft)
        self.refresh_window_size()
        self.app.main.setCentralWidget(self.splitter)
        self.app.main.showMaximized()  # ||
        return self

    def add_status_bar(self):
        """"""
        self.status_bar = pyqt.QStatusBar()
        self.status_bar.setStyleSheet("color: red")
        self.add_status_bar_message()
        self.app.main.setStatusBar(self.status_bar)
        return self

    def add_status_bar_message(self, text=None):
        """"""
        if self.status_message is not None:
            if text is not None:
                self.status_message += f" ... {text}"
        self.set_status_bar_message(self.status_message)
        return self

    def build_panes(self):
        """"""
        dtop = self.config.dikt["gui"]["desktop"]
        style = "3Pane" if dtop["layout"]["style"] is None else dtop["layout"]["style"]
        for pos in self.config.dikt["gui"]["desktop"]["styles"][style]["positions"]:
            widget = self.configure_widget(dtop, pos)
            logma.info(f"Widget {widget} load")
            # Loads Main Panes for 1, 2, or 3 Pane Applications
            self.panes[pos] = loadWidget(self.parent, widget)
            if self.panes[pos] is None:
                raise Exception(f"Widget {widget} not loaded")
            self.create_objects(pos)
            self.splitter.addWidget(self.panes[pos])
        return self

    def configure_widget(self, dtop, pos):
        """"""
        default = {"name": "Generic", "widget": "nchantrs.widgets.tabsets.NchantdTabSet"}
        widget = dtop["layout"][pos] if dtop["layout"][pos]["widget"] is not None else default
        # Add apps which controls data systems access for configurations
        widget["apps"] = self.config.dikt.get("apps", [])
        widget["apps"].append("nchantrs")
        widget["pos"] = pos
        # widget["has_toolbox"] = False
        # if pos == "center":
        #     widget["has_toolbox"] = True
        return widget

    def create_objects(self, pos):
        """"""
        create_objects = True
        if pos == "right":
            create_objects = False
        self.panes[pos].initWidget({"create_objects": create_objects})
        return self

    def on_window_move(self, event):
        """"""
        self.refresh_window_size()

    def on_window_resize(self, event):
        """"""
        self.refresh_window_size()

    def refresh_window_size(self):
        # self._set_screen_geometry()
        self._set_application_size()

    def set_status_bar_message(self, text=""):
        """"""
        self.status_message = text
        self.status_bar.showMessage(self.status_message)
        return self

    def set_theme(self, theme="midnight_mist"):
        """"""
        super().set_theme(theme)
        self.app.main.setWindowTitle(self.parent.app.application_name)
        self.themes_path = join(here, "../themes")
        path = join(self.themes_path, "_data_", "icons", "midnight_icons", "full-length-nchantrs.svg")
        self.app.main.setWindowIcon(pyqt.QIcon(path))
        self._set_background()
        self.refresh_window_size()
        return self

    def set_toolbar(self):
        """"""
        toolbar = self.panes.get("toolbar", None)
        if toolbar is not None:
            self.splitter.addWidget(toolbar)
        return self

    def show_splash_screen(self):
        """ """
        cfg = self.config.dikt["dialogs"]["splash"]
        screen = dialogs.Sigil(cfg)
        screen.show()
        time.sleep(cfg["time"])
        screen.close()
        return self

    def take_screen_shot(self, save=False):
        """"""
        image = self.screen.grabWindow(0)
        if save:
            name = dt.datetime.now().strftime("%Y%m%d%H%M%S")
            self.screen.save(f"{name}_{uuid()}", "png")
        return image, self.gui.globalMousePosition()

    def _set_background(self, path=None):
        """"""
        if path:
            self.app.main.setStyleSheet(f"background-image: url({path});")

    def _set_configurations(self):
        """"""
        self.app.main.setAttribute(pyqt.Qt.WA_DeleteOnClose)
        self.app.main.setAutoFillBackground(True)
        self.app.main.MaxRecentFiles = self.config.dikt.get("max_recent_files", 10)
        self.app.main.windowList = []
        self.app.main.recentFileActions = []

    def _set_application_size(self):
        """"""
        self.app.main.setMinimumSize(300, 300)
        screen_geometry = self.gui.geometry()
        max_width = screen_geometry.width()
        max_height = screen_geometry.height()
        section = max_width / 6 - 2
        section_1 = section * 0.75 if section * 0.75 < 200 else 200
        self.splitter.setSizes([10, section_1, section * 4, section])
        self.app.main.setMaximumSize(max_width, max_height)
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
