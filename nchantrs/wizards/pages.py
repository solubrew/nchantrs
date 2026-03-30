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
from os.path import abspath, dirname, join

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor

import logging
from nchantrs.libraries import pyqt

logger = logging.getLogger(__name__)
from nchantrs.widgets import controls
from ogma.logma import Logma
from nchantrs.widgets.controls.radios import NchantdRadioButtonGroup

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class NchantdWizardPage(pyqt.QWizardPage):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__()
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdFundAccountsTab")
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.app = self.parent.app

    def initModel(self):
        """"""

    def initView(self):
        """
        A stackable page of widgets with a bottom configured navigation buttons

        """
        self.layout = pyqt.QVBoxLayout()
        self.setLayout(self.layout)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdSelectInstancePage(NchantdWizardPage):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdSelectInstancePage")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self.parent)
        self.config.override(cfg)
        self.app = self.parent.app

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        if self.app.recent_documents:
            cfg = {"text": "Select Recent Document", "options": self.parent.recent_documents}
            self.select_document = NchantdRadioButtonGroup(self, cfg)
            self.layout.addWidget(self.select_document)
            self.registerField("select_document", self.select_document)
        cfg = {
            "text": "Select Area of Focus:",
            "options": {
                "Finance": ["Personal Budgeting", "Business Accounting", "Investing"],
                "Task Management": [],
                "Graphic Design": [],
            },
        }
        # 'Social Media': [],
        # 'Document Management': [],
        # 'Business': ['Business Management', 'Project Management', 'Financial Management'],
        #
        # 'Games': [],
        #
        #
        # 'Audio': [],
        # 'Assistant': [],
        # 'Robotitics': [],
        # 'Analytics': [],
        self.checks = NchantdRadioButtonGroup(self, cfg).initWidget()
        self.layout.addWidget(self.checks)
        self.registerField("focus_check", self.checks)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    # def nextId(self):
    # 	""""""
    # 	pass
    # 	#if self.field():


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
