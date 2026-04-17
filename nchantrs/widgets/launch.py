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
from kahndor import kahndor

import logging

logger = logging.getLogger(__name__)
from nchantrs.wizards.accounts import NchantdNewApplicationWizard
from nchantrs.widgets.widgets import NchantdWidget
from kahndor.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


# class NchantdLaunch(NchantdWidget):
#     """"""
#
#     def __init__(self, application, parent=None, cfg=None):
#         """ """
#         self.parent = parent
#         self.config = kahndor.Instruct(pxcfg).select("NchantdLaunch")
#         if self.parent:
#             self.config.override(parent.config)
#         self.config.override(cfg)
#         super(NchantdLaunch, self).__init__(self.parent, self.config)
#         self.application = application(self, self.config)
#         self.setup_wizard = NchantdNewApplicationWizard(self.parent, self.config)
#
#     def initModel(self):
#         """"""
#         super().initModel()
#         return self
#
#     def initView(self):
#         """"""
#         super().initView()
#         self.setup_wizard.finished.connect(self.launch_application)
#         self.setup_wizard.initWidget()
#         return self
#
#     def initWidget(self):
#         """"""
#         self.initModel()
#         self.initView()
#         return self
#
#     def launch_application(self):
#         """"""
#         self.application.initApp()


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
