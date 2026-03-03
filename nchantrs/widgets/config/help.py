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
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.widgets.groups import NchantdVScrollGroupBox, NchantdHGroupBox, NchantdHScrollGroupBox
from nchantrs.widgets.media.editors.editors import NchantdEntryEditor
from nchantrs.widgets.media.images import NchantdImage
from nchantrs.widgets.widgets import NchantdWidget
from ogma.logma import Logma
from nchantrs.widgets.tabsets import NchantdTab

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "help.yaml")


class NchantdFAQs(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdFAQs"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.primary_settings_group = None

    def initModel(self):
        """"""
        return self

    def initView(self):
        """"""
        super().initView()
        cfg = {"size": ["auto", "auto"]}
        self.primary_settings_group = NchantdVScrollGroupBox(self, cfg)
        self.primary_settings_group.setTitle("Frequently Asked Questions")
        self.layout.addLayout(self.primary_settings_group.layout)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdHelpChatDex(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdHelpChatDex"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        cfg = {"size": ["auto", "auto"]}
        self.model_view = NchantdHScrollGroupBox(self, cfg)
        self.layout.addLayout(self.model_view.layout)
        layout = pyqt.QHBoxLayout()
        cfg = {"size": ["auto", "auto"]}
        index_group = NchantdVScrollGroupBox(self, cfg)
        layout.addLayout(index_group.layout)
        cfg = {"size": ["auto", "auto"]}
        chat_group = NchantdVScrollGroupBox(self, cfg)

        layout.addLayout(chat_group.layout)
        self.layout.addLayout(layout)

        cfg = {"size": ["auto", "auto"]}
        chat_entry_group = NchantdHGroupBox(self, cfg).initWidget()
        cfg = {"path": "Blubert.png", "size": [100, 100]}
        bot_image = NchantdImage(self, cfg).initWidget()
        chat_entry_group.addWidget(bot_image)
        cfg = {"text": "Chat with the Nchantd", "layout": "horizontal"}
        chat_entry = NchantdEntryEditor(self, cfg).initWidget()
        chat_entry_group.addWidget(chat_entry)
        self.layout.addWidget(chat_entry_group)

        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdHelpDocs(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdHelpDocs"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        cfg = {"size": ["auto", "auto"]}
        self.primary_settings_group = NchantdVScrollGroupBox(self, cfg)
        self.primary_settings_group.setTitle("Documentation")
        self.layout.addLayout(self.primary_settings_group.layout)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
