# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
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
from os.path import dirname, join

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.widgets.tabsets import NchantdTab
from nchantrs.widgets.browsers.browsers import NchantdWebBrowser
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")
pxcfg = {}


class NchantdCalendlyConnectTab:
    """"""

    def __init__(self, parent=None, cfg=None):
        """"""
        self.confg = condor.Instruct(pxcfg).select("NchantdCalendlyConnectTab")
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        super(NchantdCalendlyConnectTab, self).__init__()

    def initModel(self):
        """"""
        pass

    def initView(self):
        """"""
        pass

    def initWidget(self):
        """"""
        pass


class NchantdConnectTab(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None):
        """"""
        self.confg = condor.Instruct(pxcfg).select("NchantdConnectTab")
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        super(NchantdConnectTab, self).__init__()

    def initModel(self):
        """"""
        pass

    def initView(self):
        """"""
        pass

    def initWidget(self):
        """"""
        pass


class NchantdFacebookConnectTab:
    """"""

    def __init__(self, parent=None, cfg=None):
        """"""
        self.confg = condor.Instruct(pxcfg).select("NchantdFacebookConnectTab")
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        super(NchantdFacebookConnectTab, self).__init__()

    def initModel(self):
        """"""
        pass

    def initView(self):
        """"""
        pass

    def initWidget(self):
        """"""
        pass


[DONE]
# Connect to the google calendar api integrate a browser into this tab
# Leverage Google Stone
#
class NchantdGoogleConnectTab(NchantdConnectTab):
    """"""

    def __init__(self, parent=None, cfg=None):
        """"""
        self.confg = condor.Instruct(pxcfg).select("NchantdGoogleConnectTab")
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        super(NchantdGoogleConnectTab, self).__init__()

    def initModel(self):
        """"""
        [DONE]
        pass

    def initView(self):
        """"""
        self.layout = pyqt.VBoxLayout()

    def initWidget(self):
        """"""
        self.state_details = ""  # Show connected status, when connected, when authenticated?
        self.browser = NchantdWebBrowser(self).initWidget()
        return self


class NchantdOutlookConnectTab:
    """"""

    def __init__(self, parent=None, cfg=None):
        """"""
        self.confg = condor.Instruct(pxcfg).select("NchantdOutlookConnectTab")
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        super(NchantdOutlookConnectTab, self).__init__()

    def initModel(self):
        """"""
        pass

    def initView(self):
        """"""
        pass

    def initWidget(self):
        """"""
        pass


class NchantdXConnectTab:
    """"""

    def __init__(self, parent=None, cfg=None):
        """"""
        self.confg = condor.Instruct(pxcfg).select("NchantdCalendlyConnectTab")
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        super(NchantdXConnectTab, self).__init__()

    def initModel(self):
        """"""
        pass

    def initView(self):
        """"""
        pass

    def initWidget(self):
        """"""
        pass


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
