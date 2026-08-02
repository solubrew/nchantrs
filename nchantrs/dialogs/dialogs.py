from typing import Any
'\n---\n<(META)>:\n    docid: <^(UUID)^>\n    name:\n    description: >\n    expirary: <[expiration]>\n    version: <[version]>\n    authority: document|this\n    security: sec|lvl2\n    <(WT)>: -32\n'
from os.path import abspath, dirname, join
from sys import argv
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.views.applicationviews import NchantdCapeView
from nchantrs.widgets.applications.applications import NchantdPanties
from nchantrs.models.applicationmodels import NchantdCapeModel
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.widgets import NchantdWidgetMixin, loadWidget
from nchantrs.widgets.controls.button_groups import NchantdAcceptButtons, NchantdOkButtons
from nchantrs.themes.themes import NchantdTheme
from nchantrs.widgets.widgets import NchantdWidget
from kahndor.logma import Logma
from nchantrs.dialogs.sigil import NchantdSigilMixin
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
pxcfg = join(abspath(here), '_data_', 'dialogs.yaml')

class NchantdCape(NchantdPanties):
    """Cape is the base class leveraging dialogs to create single pane applications"""

    def __init__(self, name, instance=None, parent=None, cfg=None, args=None, log_file=None) -> None:
        """
        :param name:
        :param cfg:
        """
        self.config = kahndor.Instruct(pxcfg).select('NchantdCape')
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg).addArgs(args)
        logma.info(f'NchantdCape Config: {self.config.dikt}')
        self.application_name = name
        self.name = name
        self.parent = parent
        self.main_widget = pyqt.QMainWindow()
        self.main_widget.setWindowTitle(name)
        self.main_widget.destroyed.connect(self.quit)
        self.model = NchantdCapeModel(self)
        self.view = NchantdCapeView(self)
        self.user = self.model.user
        self.newApplication = True
        self.src = None
        self._init_view_called = False

    @property
    def main(self) -> Any:
        """Expose main_widget as main for compatibility with theme initialization"""
        return self.main_widget

    def initView(self, cfg=None) -> Any:
        """Initialize UI setting the main application layout and building
        landing widgets"""
        if hasattr(self, '_init_view_called') and self._init_view_called:
            import traceback
            logma.critical(f'NchantdCape.initView() called TWICE! Second call blocked.')
            logma.critical(f'Call stack for second call:')
            for line in traceback.format_stack():
                logma.critical(f'  {line.strip()}')
            return self
        self._init_view_called = True
        if cfg is None:
            cfg = {}
        logma.critical(f'NchantdCape.initView() STARTING NOW')
        logma.critical(f'cfg passed: {cfg}')
        central_widget = pyqt.QWidget()
        self.main_layout = pyqt.QVBoxLayout()
        central_widget.setLayout(self.main_layout)
        self.main_widget.setCentralWidget(central_widget)
        if cfg.get('widget', None):
            logma.info(f"Add Widget {cfg['widget']}")
            self.add_widget(cfg['widget'])
        else:
            logma.info('No widget provided - adding welcome placeholder')
            welcome_label = pyqt.QLabel('Welcome to NchantdAXN')
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

    def add_widget(self, widget) -> Any:
        """"""
        logma.info(f'Adding widget: {widget}')
        try:
            widget_instance = widget(self)
            logma.info(f'Widget instance created: {widget_instance}')
            widget_instance.initWidget()
            logma.info(f'Widget initialized: {widget_instance}')
            self.main_layout.addWidget(widget_instance)
            logma.info(f'Widget added to layout')
            widget_instance.show()
            self.main_widget.update()
            logma.info(f'Widget displayed')
        except Exception as e:
            logma.error(f'Error adding widget: {e}')
            import traceback
            traceback.print_exc()
        return self

    def initApp(self, cfg=None) -> int:
        """Initialize and run the application"""
        self.initModel()
        self.initView(cfg)
        logma.critical('Main widget shown - starting Qt event loop')
        pyqt.QApplication.instance().exec()
        logma.info(f'Application exiting')
        return 0

    def closeEvent(self, event) -> Any:
        """Handle application close event"""
        logma.info(f'NchantdCape Close Event')
        event.accept()
        self.quit()
        return self

class NchantdClip(pyqt.QDialog):
    """"""

    def __init__(self, name, args, widget, cfg=None) -> None:
        """ """
        self.app = pyqt.QApplication(args)
        super().__init__()
        self.setWindowTitle(name)
        self.resize(300, 200)
        layout = pyqt.QVBoxLayout()
        logma.info(f'Widget {widget}')
        logma.info(f'Type {type(widget)}')
        layout.addWidget(widget().initWidget())

    def initApp(self) -> None:
        """"""
        self.exec()
        self.app.exec()

class NchantdSigil(NchantdSigilMixin, pyqt.QDialog):
    """Sigil is the base class for individual dialogs used to interact with the
    user these Sigils allow the user to alter their Cloak"""

    def __init__(self, name, parent=None, cfg: dict={}) -> None:
        """
        :param name:
        :param parent:
        :param cfg:
        """
        super().__init__(parent)
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdSigil').override(parent.config).override(cfg)
        if self.layout is None:
            self.layout = pyqt.QVBoxLayout()
            self.setLayout(self.layout)

    def closeEvent(self, event) -> Any:
        """Handle close event and emit finished signal"""
        logma.info(f'NchantdSigil Close Event')
        event.accept()
        self.finished.emit(0)
        return self

    def initModel(self, cfg=None) -> None:
        """"""
        super().initModel(cfg)

    def initView(self, cfg=None) -> Any:
        """Build the dialog from the provided parameters"""
        super().initView(cfg)
        self.show()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        self.run()
        return self

    def exec_(self) -> None:
        """"""
        self.exec()

    def run(self, cfg=None) -> None:
        """"""
        logma.info(f'Run NchantdSigil')
        self.resize(300, 150)
        self.exec_()

class NchantdSplashDialog(NchantdSigil):
    """ """

    def __init__(self) -> None:
        """ """

    def buildDialog(self) -> Any:
        logma.info(f'buildDialog called')
        return self

class NchantdBroach(NchantdWidget):
    """"""

    def __init__(self, name, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdBroach').override(cfg))

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        self.setWindowFlags(pyqt.Qt.Widget)
        self.resize(300, 150)
        self.show()
        self.raise_()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self
'\n\n'