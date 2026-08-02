from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from nchantrs.widgets.widgets import NchantdWidget
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'managers.yaml')

class NchantdManager(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdManager').override(cfg))

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdBasket(NchantdWidget):
    """A Group with configuration drop in actions like moving, or copying a file, exporting, importing, tagging
    etc"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdBasket').override(cfg))

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdBasketManager(NchantdManager):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdBasketManager').override(cfg))
        super(NchantdBasketManager, self).__init__(self.parent, self.config)
        self.baskets = ['Memes', 'InfoGraphics', 'Photos']

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        for basket in self.baskets:
            group = pyqt.QGroupBox()
            group.setTitle(basket)
            layout = pyqt.QVBoxLayout()
            group.setLayout(layout)
            cfg = {'text': 'Drop File Here'}
            label = NchantdLabel(self, cfg).initWidget()
            layout.addWidget(label)
            self.layout.addWidget(group)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdExtensionManager(NchantdManager):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdExtensionManager').override(cfg))
        logma.info(f'NchantdExtensionManager initialized')

    def initModel(self) -> Any:
        super().initModel()
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> Any:
        """"""
        header_layout = pyqt.QVBoxLayout()
        cfg = {}
        self.header = NchantdLabel(self, cfg).initWidget()
        header_layout.addWidget(self.header)
        self.layout.addLayout(header_layout)
        self.extension_catalog = NchantdCatalog(self, cfg).initWidget()
        self.layout.addWidget(self.extension_catalog)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def add_extension(self) -> None:
        logma.info(f'add_extension called')
        return self

    def remove_extension(self) -> None:
        logma.info(f'remove_extension called')
        return self

class NchantdFileSystemsManager(NchantdManager):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdFileSystemsManager').override(cfg))

    def initModel(self) -> Any:
        super().initModel()
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> Any:
        """"""
        layout = pyqt.QHBoxLayout()
        cfg = {}
        table = NchantdFileSystemsTable(self, cfg).initWidget()
        layout.addWidget(table)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdSecurityManager(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdSecurityManager').override(cfg))

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self