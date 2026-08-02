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

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.widgets.groups import NchantdVScrollGroupBox, NchantdHGroupBox, NchantdHScrollGroupBox
from nchantrs.widgets.media.editors.editors import NchantdEntryEditor
from nchantrs.widgets.media.images import NchantdImage
from nchantrs.widgets.widgets import NchantdWidget
from kahndor.logma import Logma
from nchantrs.widgets.tabsets import NchantdTab
from nchantrs.widgets.trees import NchantdTree
# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "help.yaml")


class NchantdFAQs(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdFAQs").override(parent.config).override(cfg))
        self.primary_settings_group = None
        self.faqs = None

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        self.faqs = self.app.model.get_view_options_faqs()
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        cfg = {"size": ["auto", "auto"]}
        self.primary_settings_group = NchantdVScrollGroupBox(self, cfg)
        self.primary_settings_group.setTitle("Frequently Asked Questions")
        # NOTE build out a list of FAQs using a simple Q/A tree widget pulling data from a datatable updated from the service
        #
        cfg = {}
        faqtree = NchantdTree(self, cfg)
        for faq in self.faqs:
            faqtree.add_item(faq)
        self.primary_settings_group.addWidget(faqtree)
        self.layout.addLayout(self.primary_settings_group.layout)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdHelpChatDex(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdHelpChatDex").override(parent.config).override(cfg))

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        cfg = {"size": ["auto", "auto"]}
        self.model_view = NchantdHScrollGroupBox(self, cfg)
        self.layout.addLayout(self.model_view.layout)
        layout = pyqt.QHBoxLayout()

        #cfg = {"size": ["auto", "auto"], "text": "Index"}
        #index_group = NchantdVScrollGroupBox(self, cfg)
        #layout.addLayout(index_group.layout)

        cfg = {"size": ["auto", "auto"], "text": "Chat"}
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

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdHelpDocs(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdHelpDocs").override(parent.config).override(cfg))

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        cfg = cfg or {}
        super().initView(cfg)
        cfg = {"size": ["auto", "auto"]}
        # self.primary_settings_group = NchantdVScrollGroupBox(self, cfg)
        # self.primary_settings_group.setTitle("Documentation")
        # self.layout.addLayout(self.primary_settings_group.layout)

        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
