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

    def __init__(self, name, instance=None, parent=None, cfg=None, args=None):
        """
        :param name:
        :param cfg:
        
        NOTE: We intentionally do NOT call super().__init__() because that would
        start the Qt event loop and block. Instead, we set up necessary attributes
        manually and defer Qt initialization.
        """
        print("="*60)
        print("NchantdCape.__init__ STARTING (NO super().__init__)")
        print(f"name: {name}, cfg: {cfg}")
        print(f"QApplication.instance(): {pyqt.QApplication.instance()}")
        print(f"args: {args}")
        print("="*60)
        
        logma.critical("="*60)
        logma.critical("NchantdCape.__init__ STARTING")
        logma.critical(f"QApplication.instance(): {pyqt.QApplication.instance()}")
        logma.critical("="*60)
        
        # Set up config manually (like parent does, but without blocking)
        config = condor.Instruct(pxcfg).select("NchantdPanties").addArgs(args)
        if self.config is None:
            self.config = config
        else:
            self.config.override(config)
        self.config.override(pxcfg).select("NchantdCape").override(cfg).addArgs(args)
        logma.info(f"NchantdCape Config: {self.config.dikt}")
        self.parent = parent
        
        # Set up application attributes manually (without starting event loop)
        self.application_name = name
        self.slug = self.application_name.lower().replace(" ", "_")
        self.application_NCD = "da1e9bb0-1dab-48de-ac28-9afa91568a39"
        self.dialogs = {}
        self.reset = None
        self.app = self  # Set app to self (like parent NchantdPanties does)
        self.primary_focus = None
        self.is_installable = self.config.dikt.get("is_installable", False)
        self.is_install_optional = self.config.dikt.get("is_install_optional", False)
        self.is_install_selected = False

        # Create a main window widget to hold the content instead of a separate dialog
        print("Creating main_widget...")
        logma.critical("About to create QMainWindow...")
        logma.critical(f"QApplication.instance() before QMainWindow: {pyqt.QApplication.instance()}")
        
        # CRITICAL: Create QApplication BEFORE creating QMainWindow
        logma.critical("Creating QApplication...")
        if pyqt.QApplication.instance() is None:
            self._qapp = pyqt.QApplication(['nchantdaxn'])
            logma.critical(f"QApplication created: {pyqt.QApplication.instance()}")
        else:
            logma.critical(f"QApplication already exists: {pyqt.QApplication.instance()}")
        
        self.main_widget = pyqt.QMainWindow()
        logma.critical(f"QApplication.instance() after QMainWindow: {pyqt.QApplication.instance()}")
        self.main_widget.setWindowTitle(name)
        # CRITICAL: Prevent recursive quit by using a flag
        self._quitting = False
        # QMainWindow doesn't have finished signal, use destroyed or closeEvent instead
        self.main_widget.destroyed.connect(self._on_main_widget_destroyed)
        print("main_widget created")

        print("Creating model and view...")
        self.model = NchantdCapeModel(self)
        self.view = NchantdCapeView(self)
        self.user = self.model.user
        self.newApplication = True
        self.src = None
        print("Model and view created")

        # CRITICAL: Initialize the view immediately after setup
        # This ensures main_layout is created before any widget operations
        print(f"About to call initView(cfg={cfg})...")
        try:
            self.initView(cfg)
        except Exception as e:
            print(f"CRITICAL ERROR in initView: {e}")
            import traceback
            traceback.print_exc()
            raise
        print("initView completed")

    @property
    def main(self):
        """Expose main_widget as main for compatibility with theme initialization"""
        return self.main_widget

    def quit(self):
        """Exit the application"""
        print("quit() called")
        # Prevent recursive quit
        if getattr(self, '_quitting', False):
            print("Already quitting - ignoring")
            return self
        self._quitting = True
        if self.app:
            self.app.quit()
        return self

    def _on_main_widget_destroyed(self):
        """Handle main_widget destruction without recursive quit"""
        print("_on_main_widget_destroyed() called")
        if not getattr(self, '_quitting', False):
            self._quitting = True
            if self.app:
                self.app.quit()
        return self

    def exit(self, code=0):
        """Exit the application with code"""
        print(f"exit({code}) called")
        if self.app:
            self.app.exit(code)
        return self

    def initView(self, cfg=None):
        """Initialize UI setting the main application layout and building
        landing widgets"""
        # FORCE PRINT - to ensure we see this in all cases
        print("="*60)
        print("NchantdCape.initView() STARTING NOW")
        print(f"cfg passed: {cfg}")
        print("="*60)

        logma.critical("="*60)
        logma.critical("NchantdCape.initView() STARTING")
        logma.critical(f"cfg passed: {cfg}")
        logma.critical("="*60)

        if cfg is None:
            cfg = {}
        
        # Force print
        print(f"cfg after None check: {cfg}")
        
        # DEBUG: Log the cfg at start of initView
        logma.critical(f"NchantdCape.initView - cfg at start: {cfg}")
        
        super().initView()
        self.view.initView()

        # Create central widget for the main window
        print("Creating central widget and main_layout...")
        central_widget = pyqt.QWidget()
        self.main_layout = pyqt.QVBoxLayout()
        central_widget.setLayout(self.main_layout)
        self.main_widget.setCentralWidget(central_widget)
        print(f"main_layout created: {self.main_layout}")

        # ==== ADD AUTHENTICATION CHECK HERE ====
        # Check if this application requires authentication
        # Always require auth for now - ensure password dialog always shows
        requires_auth = True  # Force authentication for security
        
        # Force print
        print(f"requires_auth: {requires_auth}")
        logma.critical(f"NchantdCape.initView - requires_auth: {requires_auth}")
        
        if requires_auth:
            print("Authentication required - showing password dialog NOW")
            logma.critical("Authentication required - showing password dialog NOW")
            if not self._show_password_dialog():
                print("Authentication cancelled - exiting")
                logma.critical("Authentication cancelled - exiting")
                self.quit()
                return self
            logma.critical("Authentication successful")
        else:
            logma.info("Authentication NOT required - skipping password dialog")
        # =======================================

        # Now add the widget since layout is initialized
        if cfg.get("widget", None):
            logma.info(f"Add Widget {cfg['widget']}")
            self.add_widget(cfg["widget"])

        self.main_widget.MaxRecentFiles = 10
        self.main_widget.windowList = []
        self.main_widget.recentFileActs = []
        self.main_widget.show()

        return self

    def _show_password_dialog(self):
        """Show password dialog for authentication"""
        # FORCE PRINT - to ensure we see this in all cases
        print("="*50)
        print("_show_password_dialog() CALLED - ABOUT TO SHOW DIALOG")
        print("="*50)
        
        logma.critical("="*50)
        logma.critical("_show_password_dialog() CALLED")
        logma.critical("="*50)
        
        dialog = pyqt.QDialog(self.main_widget)
        dialog.setWindowTitle("Nchantrs Authentication")
        dialog.setMinimumWidth(350)
        dialog.setWindowFlags(dialog.windowFlags() | pyqt.Qt.Dialog)

        layout = pyqt.QVBoxLayout(dialog)

        # Icon
        icon_label = pyqt.QLabel("🔐")
        icon_label.setAlignment(pyqt.Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 48px;")
        layout.addWidget(icon_label)

        layout.addWidget(pyqt.QLabel("Enter master passphrase to continue:"))

        passphrase_input = pyqt.QLineEdit()
        passphrase_input.setEchoMode(pyqt.QLineEdit.Password)
        passphrase_input.returnPressed.connect(dialog.accept)
        layout.addWidget(passphrase_input)

        buttons = pyqt.QDialogButtonBox(pyqt.QDialogButtonBox.Ok | pyqt.QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        # Show dialog
        print("About to call dialog.exec()...")
        result = dialog.exec()
        print(f"dialog.exec() returned: {result}")
        
        if result == pyqt.QDialog.Accepted:
            password = passphrase_input.text()
            if password:
                print("Password accepted")
                logma.info("Password accepted")
                return True
            else:
                print("Empty password - rejecting")
                logma.info("Empty password - rejecting")
                return False
        
        print("Dialog cancelled")
        logma.info("Dialog cancelled")
        return False

    def add_widget(self, widget):
        """"""
        logma.info(f"Adding widget: {widget}")
        try:
            widget_instance = widget(self)
            logma.info(f"Widget instance created: {widget_instance}")

            widget_instance.initWidget()
            logma.info(f"Widget initialized: {widget_instance}")

            # DEBUG: Check main_layout
            logma.info(f"main_layout is None: {self.main_layout is None}")
            logma.info(f"widget_instance parent: {widget_instance.parent()}")
            logma.info(f"widget_instance layout: {widget_instance.layout()}")

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
        """"""
        self.initModel()
        self.initView(cfg)

        result = self.exec_()
        logma.info(f"Application exiting with result: {result}")
        return result

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
