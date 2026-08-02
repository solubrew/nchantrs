# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
from typing import Any

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

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from nchantrs.widgets.widgets import NchantdWidget
from kahndor.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "managers.yaml")


class NchantdManager(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(self)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdManager"))
        # if self.parent:
        #     self.config.override(parent.config)
        self.config.override(cfg)

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
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdBasket")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)

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


class NchantdBasketManager(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdBasketManager")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdBasketManager, self).__init__(self.parent, self.config)
        self.baskets = ["Memes", "InfoGraphics", "Photos"]

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
            cfg = {"text": "Drop File Here"}
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
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdExtensionManager")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdExtensionManager, self).__init__(self.parent, self.config)
        logma.info(f"NchantdExtensionManager initialized")


    def initModel(self) -> Any:
        """"""
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
        """
        need a method for injecting tabs into tabsets for specific nodes
        those nodes could be

        singlely identified or
        pattern identified or
        a mapping

        :return:
        """

    def remove_extension(self) -> None:
        """"""


class NchantdFileSystemsManager(NchantdManager):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdFileSystemsManager")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdFileSystemsManager, self).__init__(self.parent, self.config)

    def initModel(self) -> Any:
        """"""
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


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
