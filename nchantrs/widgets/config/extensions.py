from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.widgets.groups import NchantdHScrollGroupBox, NchantdVScrollGroupBox
from kahndor.logma import Logma
from nchantrs.widgets.config.settings import NchantdSettingsWidget
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'extensions.yaml')

class NchantdExtensionsSettings(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdExtensionsSettings')
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.primary_settings_group = None

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.primary_settings_group = NchantdVScrollGroupBox()
        self.primary_settings_group.setTitle('Configurations & Permissions')
        self.layout.addLayout(self.primary_settings_group.layout)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdExtensionsCatalog(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdExtensionsCatalog')
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.primary_settings_group = None

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.primary_settings_group = NchantdVScrollGroupBox()
        self.primary_settings_group.setTitle('Available Extensions')
        self.layout.addLayout(self.primary_settings_group.layout)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self