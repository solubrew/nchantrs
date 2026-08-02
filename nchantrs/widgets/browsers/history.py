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
pxcfg = join(here, '_data_', 'history.yaml')

class NchantdWebHistory(object):
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select('').override(cfg)

    def add_page(self) -> None:
        logma.info(f'add_page called')
        return self

    def back(self) -> None:
        logma.info(f'back called')
        return self

    def forward(self) -> None:
        logma.info(f'forward called')
        return self