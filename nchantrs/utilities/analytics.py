"""
---
<(META)>:
        docid:
        name:
        description: >
            internal analytics to be used for development, vector search, etc.
            allow internal access for simple demonstrations of graphical analytics/analysis within the Nchantrs Application
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""
from os.path import abspath, dirname, join
import datetime as dt
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from kahndor.logma import Logma
from typing import Optional, Dict, List, Any, Tuple
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')

class NchantdAnalytics:
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('Nchantd'))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

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