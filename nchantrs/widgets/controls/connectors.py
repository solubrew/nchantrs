from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import dirname, join
from kahndor import kahndor
import logging
from nchantrs.widgets.tabsets import NchantdTab
logger = logging.getLogger(__name__)
from nchantrs.widgets.browsers.browsers import NchantdWebBrowser
from kahndor.logma import Logma
here = join(dirname(__file__), '')
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')

class NchantdCalendlyConnectTab:
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        self.confg = kahndor.Instruct(pxcfg).select('NchantdCalendlyConnectTab')
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        super(NchantdCalendlyConnectTab, self).__init__()

    def initModel(self) -> None:
        """"""
        pass

    def initView(self) -> None:
        """"""
        pass

    def initWidget(self) -> None:
        """"""
        pass

class NchantdConnectTab(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        self.confg = kahndor.Instruct(pxcfg).select('NchantdConnectTab')
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        super(NchantdConnectTab, self).__init__()

    def initModel(self) -> None:
        """"""
        pass

    def initView(self) -> None:
        """"""
        pass

    def initWidget(self) -> None:
        """"""
        pass

class NchantdFacebookConnectTab:
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        self.confg = kahndor.Instruct(pxcfg).select('NchantdFacebookConnectTab')
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        super(NchantdFacebookConnectTab, self).__init__()

    def initModel(self) -> None:
        """"""
        pass

    def initView(self) -> None:
        """"""
        pass

    def initWidget(self) -> None:
        """"""
        pass

class NchantdGoogleConnectTab(NchantdConnectTab):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        self.confg = kahndor.Instruct(pxcfg).select('NchantdGoogleConnectTab')
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        super(NchantdGoogleConnectTab, self).__init__()

    def initModel(self) -> None:
        """"""
        pass

    def initView(self) -> None:
        """"""
        self.layout = pyqt.VBoxLayout()

    def initWidget(self) -> Any:
        """"""
        self.state_details = ''
        self.browser = NchantdWebBrowser(self).initWidget()
        return self

class NchantdOutlookConnectTab:
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        self.confg = kahndor.Instruct(pxcfg).select('NchantdOutlookConnectTab')
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        super(NchantdOutlookConnectTab, self).__init__()

    def initModel(self) -> None:
        """"""
        pass

    def initView(self) -> None:
        """"""
        pass

    def initWidget(self) -> None:
        """"""
        pass

class NchantdXConnectTab:
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        self.confg = kahndor.Instruct(pxcfg).select('NchantdCalendlyConnectTab')
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        super(NchantdXConnectTab, self).__init__()

    def initModel(self) -> None:
        """"""
        pass

    def initView(self) -> None:
        """"""
        pass

    def initWidget(self) -> None:
        """"""
        pass