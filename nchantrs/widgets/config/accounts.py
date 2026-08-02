from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import dirname, join
from kahndor import kahndor
from nchantrs.utilities.users import NchantdUser
from kahndor.logma import Logma
from nchantrs.widgets.config.settings import NchantdSettingsWidget
from nchantrs.widgets.tabsets import NchantdTab
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'accounts.yaml')

class NchantdAccountOverview(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdAccountOverview').override(cfg))
        self.user = NchantdUser(self, self.config)
        self.address = None
        self.description = None
        self.email = None
        self.icon = None
        self.name = None
        self.username = None
        self.uuid = None

    def initModel(self) -> Any:
        """"""
        self.user.select_user()
        return self

    def initView(self) -> Any:
        super().initView()
        logma.info(f'initView {{type(self).__name__}}')
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdAccountSettings(NchantdSettingsWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdAccountSettings').override(parent.config).override(cfg))

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self