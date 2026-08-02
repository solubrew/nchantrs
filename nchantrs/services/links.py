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
from nchantrs.libraries import pyqt
from kahndor.logma import Logma
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
        logma.info(f'get_links requested')
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