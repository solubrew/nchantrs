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
from os.path import dirname, join
from typing import Optional, Dict, List
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from kahndor.logma import Logma
here = join(dirname(__file__), '')
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'license.yaml')

class Ownership(object):
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select('Ownership').override(cfg)

class TOS:
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select('TOS').override(cfg)