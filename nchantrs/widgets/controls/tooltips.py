from typing import Any

'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
import datetime as dt
import logging
from os.path import abspath, dirname, join

logger = logging.getLogger(__name__)
from kahndor import kahndor
from kahndor.logma import Logma

from nchantrs.libraries import pyqt

here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')

class NchantdToolTip(pyqt.QWidget):
    """Create a tooltip popup that can have embeded widgets"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdToolTip')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdToolTip, self).__init__(self.parent)

    def initModel(self) -> Any:
        super().initModel()
        logma.info('initModel {type(self).__name__}')
        return self

    def initView(self) -> Any:
        super().initView()
        logma.info('initView {type(self).__name__}')
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self
