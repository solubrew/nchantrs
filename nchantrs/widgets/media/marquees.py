from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidget
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'marquees.yaml')

class NchantdTextMarquee(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdTextMarquee'))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.text = ''
        self.offset = 0
        self.timer = pyqt.QTimer(self)
        self.timer.timeout.connect(self.advance_offset)
        self.timer.start(1000 / 30)
        logma.info(f'NchantdTextMarquee initialized')

    def advance_offset(self) -> None:
        self.offset += 1
        self.update()

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def setText(self, text) -> Any:
        self.text = text
        return self

    def paintEvent(self, event) -> None:
        painter = pyqt.QPainter(self)
        painter.setFont(pyqt.QFont('Arial', 30))
        width = painter.fontMetrics().width(self.text)
        if width < self.offset:
            self.offset = 0
        painter.drawText(-self.offset, self.height() / 2, self.text)

class NchantdImageMarquee(NchantdTextMarquee):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdImageMarquee'))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self