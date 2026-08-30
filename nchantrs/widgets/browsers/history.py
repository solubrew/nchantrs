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
import datetime as dt
import logging
from os.path import abspath, dirname, join

logger = logging.getLogger(__name__)
from typing import Any, Dict, List, Optional, Tuple

from kahndor import kahndor
from kahndor.logma import Logma

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
        logma.info('add_page called')
        return self

    def back(self) -> None:
        logma.info('back called')
        return self

    def forward(self) -> None:
        logma.info('forward called')
        return self
