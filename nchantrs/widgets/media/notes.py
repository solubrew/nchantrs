from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import dirname, join
from kahndor import kahndor
import logging
from nchantrs.libraries import pyqt
logger = logging.getLogger(__name__)
from nchantrs.widgets.media.editors.editors import NchantdScratchEditor
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.dialogs.dialogs import NchantdSigil
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'notes.yaml')

class NchantdStickyNoteEditor(NchantdSigil):
    """A Draggable always ontop note that can be minimized to a dot or hidden entirely but then turned
    back on with correct on screen placement"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdStickyNoteEditor')
        if self.parent:
            self.config.override(parent.config)
        super().__init__('NchantdStickNote', self, self.config)
        self.config.override(cfg)
        self.is_pinned = False
        self.start_position = None
        self.toolbox_config = None
        self.editor = None

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        cfg = {}
        self.editor = NchantdScratchEditor(self, cfg).initWidget()
        self.editor.setStyleSheet('QTextEdit { background-color: #E5E28A; }')
        self.editor.setWindowTitle('Floating Note')
        self.editor.setWindowFlags(pyqt.Qt.FramelessWindowHint | pyqt.Qt.WindowStaysOnTopHint)
        self.editor.setAttribute(pyqt.Qt.WA_TranslucentBackground)
        self.editor.setWindowOpacity(0.9)
        self.layout.addWidget(self.editor)
        self.setMaximumHeight(250)
        self.setMinimumHeight(100)
        self.setMinimumWidth(100)
        self.setBaseSize(350, 250)
        self.setMaximumWidth(300)
        return self

    def mousePressEvent(self, event) -> None:
        """"""
        if event.button() == pyqt.Qt.LeftButton and (not self.is_pinned):
            self.drag_start_position = event.globalPosition().toPoint()
            self.start_position = self.frameGeometry().topLeft()

class NchantdStickyNoteManager(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('Nchantd')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdStickyNoteManager, self).__init__(self.parent, self.config)

    def initModel(self) -> Any:
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> Any:
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initView {{type(self).__name__}}')
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdRateCard(pyqt.QWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('Nchantd')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdRateCard, self).__init__(self.parent, self.config)

    def initModel(self) -> Any:
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> Any:
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initView {{type(self).__name__}}')
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self