from typing import Any
'#\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n---  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n<(META)>:  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        docid:   #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        name:\t#\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        description: >  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n\n        expirary: <[expiration]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        version: <[version]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        path: <[LEXIvrs]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        outline: <[outline]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        authority: document|this  #\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        security: sec|lvl2  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        <(WT)>: -32  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n'
from os.path import abspath, dirname, join
from kahndor import kahndor
import logging
from kahndor.logma import Logma
logger = logging.getLogger(__name__)
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'maps.yaml')

class NchantdMap:
    """ """

    def __init__(self, item, nid, df=DataFrame(), parent=None) -> None:
        """ """
        self.parent = parent
        if parent:
            cfg = self.parent.config
        self.config = kahndor.Instruct(pxcfg).select('NchantdItem')
        self.config.override(cfg)
        super(NchantdItem, self).__init__(parent)
        self.model = NchantdMapModel(self)
        self.view = NchantdMapView(self)

    def initModel(self) -> Any:
        super().initModel()
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> Any:
        """ """
        self.view.initView(self)
        self.setLayout(self.view.layout)
        return self

    def initWidget(self) -> Any:
        """ """
        self.model()
        self.view()
        return self

class NchantdMindMap:
    """Provide a Canvas area to place and arrange nodes for defining a mind map"""

    def __init__(self, item, nid, df=DataFrame(), parent=None) -> None:
        """ """
        self.parent = parent
        if parent:
            cfg = self.parent.config
        self.config = kahndor.Instruct(pxcfg).select('NchantdItem')
        self.config.override(cfg)
        super(NchantdItem, self).__init__(parent)
        self.model = NchantdMapModel(self)
        self.view = NchantdMapView(self)

    def initModel(self) -> Any:
        super().initModel()
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> Any:
        """ """
        self.view.initView(self)
        self.setLayout(self.view.layout)
        return self

    def initWidget(self) -> Any:
        """ """
        self.model()
        self.view()
        return self
'\n'