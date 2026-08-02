from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.widgets.widgets import NchantdWidget
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')

class NchantdMinuteCalendar(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('Nchantd'))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
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

class NchantdQuarterHourCalendar(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('Nchantd'))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
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

class NchantdHourCalendar(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('Nchantd'))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
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