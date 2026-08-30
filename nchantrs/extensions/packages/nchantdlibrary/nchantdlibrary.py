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
from kahndor import kahndor
from kahndor.logma import Logma

here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'nchantdlibrary.yaml')

class NchantdLibraryManager(object):
    """"""

    def __init__(self, parent, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select('NchantdLibraryManager').override(cfg)
