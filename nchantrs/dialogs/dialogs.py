# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
    docid: <^(UUID)^>
    name:
    description: >
    expirary: <[expiration]>
    version: <[version]>
    authority: document|this
    security: sec|lvl2
    <(WT)>: -32
"""

# -*- coding: utf-8 -*-
# ================================Core Modules===================================||
from os.path import abspath, dirname, join
from sys import argv

# ===============================================================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.views.applicationviews import NchantdCapeView
from nchantrs.widgets.applications.applications import NchantdPanties
from nchantrs.models.applicationmodels import NchantdCapeModel
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.widgets import NchantdWidgetMixin, loadWidget
from nchantrs.widgets.controls.button_groups import NchantdAcceptButtons, NchantdOkButtons
from nchantrs.themes.themes import NchantdTheme
from nchantrs.widgets.widgets import NchantdWidget
from ogma.logma import Logma

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ===============================================================================||
pxcfg = join(abspath(here), "_data_", "dialogs.yaml")  # ||


class NchantdCape(NchantdPanties):
    """Cape is the base class leveraging dialogs to create single pane applications"""

    def __init__(self, name, instance=None, parent=None, cfg=None, args=None, log_file=None):
        """
        :param name:
        :param cfg:
        """
        # NOTE: We do NOT call super().__init__() here because NchantdPanties
        # extends QApplication and we don't want to reinitialize it.
        # The QApplication is already created by the time we get here.
        self.config = condor.Instruct(pxcfg).select("NchantdCape")
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg).addArgs(args)
        logma.info(f"NchantdCape Config: {self.config.dikt}")

        self.application_name = name
        self.name = name
        self.parent = parent

        # Create a main window widget to hold the content instead of being the window
        self.main_widget = pyqt.QMainWindow()
        self.main_widget.setWindowTitle(name)
        # QMainWindow doesn't have finished signal, use destroyed or closeEvent instead
        self.main_widget.destroyed.connect(self.quit)

        self.model = NchantdCapeModel(self)
        self.view = NchantdCapeView(self)
        self.user = self.model.user
        self.newApplication = True
        self.src = None

        # Track initialization state
        self._init_view_called = False

    @property
    def main(self):
        """Expose main_widget as main for compatibility with theme initialization"""
        return self.main_widget

    def initView(self, cfg=None):
        """Initialize UI setting the main application layout and building
        landing widgets"""
        # Guard against double initialization
        if hasattr(self, "_init_view_called") and self._init_view_called:
            import traceback

            logma.critical(f"NchantdCape.initView() called TWICE! Second call blocked.")
            logma.critical(f"Call stack for second call:")
            for line in traceback.format_stack():
                logma.critical(f"  {line.strip()}")
            return self
        self._init_view_called = True

        if cfg is None:
            cfg = {}
        logma.critical(f"NchantdCape.initView() STARTING NOW")
        logma.critical(f"cfg passed: {cfg}")

        # Create central widget for the main window
        central_widget = pyqt.QWidget()
        self.main_layout = pyqt.QVBoxLayout()
        central_widget.setLayout(self.main_layout)
        self.main_widget.setCentralWidget(central_widget)

        # Now add the widget since layout is initialized
        if cfg.get("widget", None):
            logma.info(f"Add Widget {cfg['widget']}")
            self.add_widget(cfg["widget"])
        else:
            # Add a welcome label as placeholder
            logma.info("No widget provided - adding welcome placeholder")
            welcome_label = pyqt.QLabel("Welcome to NchantdAXN")
            welcome_label.setAlignment(pyqt.Qt.AlignCenter)
            font = pyqt.QFont()
            font.setPointSize(16)
            font.setBold(True)
            welcome_label.setFont(font)
            self.main_layout.addWidget(welcome_label)

        self.main_widget.MaxRecentFiles = 10
        self.main_widget.windowList = []
        self.main_widget.recentFileActs = []
        self.main_widget.show()

        return self

    def add_widget(self, widget):
        """"""
        logma.info(f"Adding widget: {widget}")
        try:
            widget_instance = widget(self)
            logma.info(f"Widget instance created: {widget_instance}")

            widget_instance.initWidget()
            logma.info(f"Widget initialized: {widget_instance}")

            self.main_layout.addWidget(widget_instance)
            logma.info(f"Widget added to layout")

            widget_instance.show()
            self.main_widget.update()
            logma.info(f"Widget displayed")
        except Exception as e:
            logma.error(f"Error adding widget: {e}")
            import traceback

            traceback.print_exc()
        return self

    def initApp(self, cfg=None):
        """Initialize and run the application"""
        # Initialize model
        self.initModel()
        # Initialize view
        self.initView(cfg)

        # Run Qt event loop - use the QApplication instance's exec() method
        logma.critical("Main widget shown - starting Qt event loop")
        pyqt.QApplication.instance().exec()

        logma.info(f"Application exiting")
        return 0

    def closeEvent(self, event):
        """Handle application close event"""
        logma.info(f"NchantdCape Close Event")
        event.accept()
        self.quit()
        return self

    # def closeEvent(self, event):
    #     """"""
    #     logma.info(f"Window Close Event")
    #     self.main.close()
    #     self.exit()
    #     super().closeEvent(event)


class NchantdClip(pyqt.QDialog):
    """"""

    def __init__(self, name, args, widget, cfg=None):
        """ """
        self.app = pyqt.QApplication(args)
        super().__init__()
        self.setWindowTitle(name)
        self.resize(300, 200)
        # Create a layout for the dialog
        layout = pyqt.QVBoxLayout()
        # Add the widget passed in the constructor
        logma.info(f"Widget {widget}")
        logma.info(f"Type {type(widget)}")
        layout.addWidget(widget().initWidget())

    def initApp(self):
        """"""
        self.exec()
        self.app.exec()


class NchantdSigilMixin(NchantdWidgetMixin):
    """"""

    def init_variables(self, name="generic"):
        """"""
        super().init_variables()
        self.layout = None
        self.pane = None
        self.ok = None
        self.buttons = None
        self.new = True
        self.open = False
        self.dtop = self.config.dikt["gui"]["dialogs"].get(name, None)
        if self.dtop is None:
            self.dtop = self.config.dikt["gui"]["dialogs"].get("base", None)
        # logma.info(f"Parent {self.parent}")
        # self.model = self.parent.model
        self.new_form_field = None
        self.new_form_field_style = None
        self.add_field_button = None
        return self

    def validate(self):
        """"""
        return self

    def accept_(self, *args, **kwargs):
        """"""
        logma.info(f"Accept")
        self.validate()
        # super().accept()
        self.set_ok()
        return self

    def add_field(self, field_wdgt):
        """"""
        self.layout.addWidget(field_wdgt)
        return self

    def add_accept_buttons(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {"buttons": {"ok": {"handler": self.accept}, "cancel": {"handler": self.reject}}}
        self.buttons = NchantdAcceptButtons(self, cfg).initWidget()
        layout = pyqt.QHBoxLayout()
        layout.addWidget(self.buttons)
        layout.setAlignment(self.getAlignment("right"))
        self.layout.addLayout(layout)

    def add_ok_button(self):
        """"""
        cfg = {"buttons": {"ok": {"handler": self.accept}, "cancel": {"handler": self.reject}}}
        self.buttons = NchantdOkButtons(self, cfg).initWidget()
        layout = pyqt.QHBoxLayout()
        layout.addWidget(self.buttons)
        layout.setAlignment(self.getAlignment("right"))
        self.layout.addLayout(layout)

    def buildPane(self, style="1pane"):
        """"""
        cnt = 0
        for position in self.config.dikt["styles"][style]["positions"]:
            logma.info(f"Load Widget {self.dtop['layout'][position]}")
            self.pane[position] = loadWidget(self, self.dtop["layout"][position], style)
            self.pane[position].initWidget()
            self.model.registerListener(self.pane[position])
            self.layout.addWidget(self.pane[position], cnt)
            cnt += 1

    def getData(self):
        if self.records == None:
            return self.defaults
        return self.records

    def hide_title(self):
        """"""
        self.setWindowFlags(pyqt.Qt.FramelessWindowHint)

    def increase_font_size(self, value):
        """"""

    def increase_height(self, value):
        """"""
        if "%" in value:
            height = self.height() * (1 + int(value.replace("%", "")) / 100)
            self.resize(self.width(), height)
        else:
            height = self.height() + int(value)
            self.resize(self.width(), height)

    def increase_width(self, value):
        """"""
        if "%" in value:
            width = self.width() * (1 + int(value.replace("%", "")) / 100)
            self.resize(width, self.height())
        else:
            width = self.width() + int(value)
            self.resize(width, self.height())

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None):
        """Build the dialog from the provided parameters"""
        super().initView(cfg)
        # Ensure the dialog stays on top
        self.setWindowFlags(
            self.windowFlags() | pyqt.Qt.Dialog | pyqt.Qt.SubWindow
        )  # | pyqt.Qt.WindowStaysOnTopHintowFlags
        self.setWindowTitle(self.dtop.get("title", ""))  # ||
        # self.set_size()

        tablenode = False
        self.pane = {}
        self.setAttribute(pyqt.Qt.WA_DeleteOnClose)  # ||
        theme = NchantdTheme(self)
        theme.set_theme("midnight_mist")
        # self.layout = pyqt.QVBoxLayout()
        # if log:
        #     logma.info(f"Config Position {self.dtop['layout']['center']}")
        style = self.dtop["layout"]["style"]  # Gets the Pane type of the application (1Pane, 2Pane, 3Pane, 4Pane)
        if style is None:
            style = "1Pane"
        singlepane = False
        if style == "1Pane":
            singlepane = True
        # logma.info(f"Single Pane {singlepane}")
        if self.config.dikt.get("build", None):
            self.buildPane(style)
        return self

    def initWidget(self):
        """"""
        # logma.info(f"Init Model")
        self.initModel()
        # logma.info(f"Init View")
        self.initView()
        return self

    def reject_(self, signal=None, *args, **kwargs):
        """"""
        return self

    def run(self, cfg=None):
        """"""
        self.exec_()

    def set_ok(self):
        """"""
        self.ok = True
        return self

    def setDefaults(self, defaults):
        """ """
        self.defaults = defaults
        return self

    def set_font_size(self, size):
        """"""

    def set_position(self, where="center"):
        """"""
        match where:
            case "center":
                x, y = self.set_position_center()
            case "right":
                x, y = self.set_position_right()
        return x, y

    def set_position_center(self):
        """"""
        x = self.app.view.gui.geometry().center().x() - self.geometry().width() // 2
        y = self.app.view.gui.geometry().center().y() - self.geometry().height() // 2
        self.move(x, y)
        return x, y

    def set_position_right(self):
        """"""
        x = self.app.view.gui.geometry().center().x() - self.geometry().width() * 0.8
        y = self.app.view.gui.geometry().center().y() - self.geometry().height() // 2
        self.move(x, y)
        return x, y

    def set_size(self, width=400, height=200, left=150, top=250):
        """"""
        left_ = None
        top_ = None
        width_ = None
        height_ = None
        if "size" in self.dtop.keys():
            left_ = self.dtop["size"].get("left", left)
            top_ = self.dtop["size"].get("top", top)
            width_ = self.dtop["size"].get("width", width)
            height_ = self.dtop["size"].get("height", height)
        if left_ is not None:
            left = left_
        if top_ is not None:
            top = top_
        if width_ is not None:
            width = width_
        if height_ is not None:
            height = height_
        self.setGeometry(left, top, width, height)

    def setSource(self, src):
        self.src = src
        return self


class NchantdSigil(NchantdSigilMixin, pyqt.QDialog):
    """Sigil is the base class for individual dialogs used to interact with the
    user these Sigils allow the user to alter their Cloak"""

    def __init__(self, name, parent=None, cfg: dict = {}):
        """
        :param name:
        :param parent:
        :param cfg:
        """
        super().__init__(parent)
        self.config = condor.Instruct(pxcfg).select("NchantdSigil")
        if parent:
            self.config.override(parent.config)
        self.init_variables(name)
        # Initialize layout after init_variables
        if self.layout is None:
            self.layout = pyqt.QVBoxLayout()
            self.setLayout(self.layout)
        if hasattr(self.app, "model"):  # TODO ensure that this will work may need to switch to NchantdClip
            self.model = self.app.model
        self.config.override(cfg)
        # Set minimum size to 10% of screen
        self._set_minimum_size()

    # def __init__(self, name, parent=None, cfg: dict = {}):
    #     """
    #     :param name:
    #     :param parent:
    #     :param cfg:
    #     """
    #     super().__init__(parent)
    #     # if hasattr(parent.app, "main"):
    #     #    super().__init__(parent.app.main)
    #     # else:
    #     #    super().__init__(parent)
    #     self.config = condor.Instruct(pxcfg).select("NchantdSigil")
    #     if parent:
    #         self.config.override(parent.config)
    #     self.init_variables(name)
    #     self.model = self.app.model
    #     self.config.override(cfg)

    # def closeEvent(self, event):
    #     """"""
    #     # super().closeEvent(arg__1)
    #     # self.close()
    #     # return self
    #     logma.info(f"NchantdSigil Close Event")
    #     # Accept the event to allow the dialog to close
    #     event.accept()
    #     return self
    def closeEvent(self, event):
        """Handle close event and emit finished signal"""
        logma.info(f"NchantdSigil Close Event")
        event.accept()
        # Emit finished signal to notify parent application
        self.finished.emit(0)
        return self

    def initView(self, cfg=None):
        """Build the dialog from the provided parameters"""
        super().initView(cfg)
        # Ensure the dialog stays on top
        self.setWindowFlags(self.windowFlags() | pyqt.Qt.Dialog | pyqt.Qt.SubWindow)
        self.setWindowTitle(self.dtop.get("title", ""))

        tablenode = False
        self.pane = {}
        self.setAttribute(pyqt.Qt.WA_DeleteOnClose)
        theme = NchantdTheme(self)
        theme.set_theme("midnight_mist")

        # CRITICAL: Ensure layout is set on the dialog itself BEFORE any widgets are added
        if self.layout is None:
            self.layout = pyqt.QVBoxLayout()
            self.setLayout(self.layout)
            logma.info(f"NchantdSigil.initView - created and set layout: {self.layout}")
        else:
            logma.info(f"NchantdSigil.initView - layout already exists: {self.layout}")

        style = self.dtop["layout"]["style"]
        if style is None:
            style = "1Pane"
        singlepane = False
        if style == "1Pane":
            singlepane = True

        if self.config.dikt.get("build", None):
            self.buildPane(style)

        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def _set_minimum_size(self):
        """Set dialog minimum size to 10% of screen dimensions"""
        # Get the primary screen geometry
        screen = pyqt.QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.geometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()

            # Calculate 10% of screen dimensions
            min_width = int(screen_width * 0.1)
            min_height = int(screen_height * 0.1)

            # Set minimum size
            self.setMinimumWidth(min_width)
            self.setMinimumHeight(min_height)

            logma.info(f"Dialog minimum size set to {min_width}x{min_height} (10% of {screen_width}x{screen_height})")


class NchantdSplashDialog(NchantdSigil):
    """ """

    def __init__(self):
        """ """

    def buildDialog(self):
        """ """
        return self


class NchantdBroach(NchantdWidget):
    """"""

    def __init__(self, name, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdBroach"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        # self.setWindowTitle("Floating Widget")
        # self.setWindowFlags(pyqt.Qt.Window | pyqt.Qt.WindowStaysOnTopHint)  # Acts as a top-level, always-on-top widget
        self.setWindowFlags(pyqt.Qt.Widget)
        self.resize(300, 150)
        self.show()
        self.raise_()

        # self.layout.addWidget(pyqt.QLabel("I am a floating widget!"))
        # close_button = pyqt.QPushButton("Close Floating Widget")
        # close_button.clicked.connect(self.close)
        # self.layout.addWidget(close_button)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


# def setExistingDirectory(self):
#     options = pyqt.QFileDialog.DontResolveSymlinks | pyqt.QFileDialog.ShowDirsOnly
#     label = "Choose Report Directory"
#     dirtext = self.Widgets["dirlabel"].text()
#     directory = pyqt.QFileDialog.getExistingDirectory(self, label, dirtext, options=options)
#     if directory:  # ||
#         self.Widgets["dirlabel"].setText(directory)  # ||
#     model = pyqt.FileListModel()
#     model.setDirPath(self.Widgets["dirlabel"].text())  # ||
#     self.Widgets["dirbrowser"].clear()
#     self.flist = model.fileList
#     for d in self.flist:
#         self.Widgets["dirbrowser"].append(d)
#     outpath = self.Widgets["dirlabel"].text()
#     self.outputFile = outpath


# ==============================Source Materials=================================||
"""

"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
