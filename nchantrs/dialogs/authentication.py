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
from os.path import abspath, dirname, join
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.widgets.widgets import NchantdWidget
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')

class NchantdAuthenticationWindow(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdAuthenticationWindow').override(cfg))

    def initModel(self, cfg=None) -> None:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> None:
        """"""
        super().initView(cfg)
        return self

    def initWidget(self) -> None:
        """"""
        self.initModel()
        self.initView()
        return self