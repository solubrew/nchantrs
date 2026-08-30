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

from nchantrs.libraries import pyqt

here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')

class LinkService:
    """
    This will be used to move link data this is specific to affiliates, operations and advertisements from the
    Nchantrs service to the Nchantd Applications
    """

    def __init__(self, parent, cfg: dict=None) -> None:
        """"""
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('').override(cfg)
        self.app = pyqt.QApplication.instance()

    def get_links(self) -> None:
        logma.info('get_links requested')
        return None

    def store_link(self, name: str, path: str, tags: str) -> None:
        """"""
        try:
            self.app.model.store_link(name=name, url=path, tags=tags)
        except TypeError as e:
            if 'tags' in str(e):
                try:
                    self.app.model.store_link(name=name, url=path, tag=tags)
                    return
                except TypeError:
                    pass
            raise
