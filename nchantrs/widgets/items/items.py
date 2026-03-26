# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""#																			||
---  #																			||
<(META)>:  #																	||
        docid:   #																	||
        name:	#																	||
        description: >  #															||

        expirary: <[expiration]>  #													||
        version: <[version]>  #														||
        path: <[LEXIvrs]>  #														||
        outline: <[outline]>  #														||
        authority: document|this  #													||
        security: sec|lvl2  #														||
        <(WT)>: -32  #																||
"""  # ||

# -*- coding: utf-8 -*-#														||
# ================================Core Modules===================================||
from os.path import dirname, join

# ===============================================================================||
# ===============================================================================||
from condor import condor

import logging
from nchantrs.libraries import pyqt

logger = logging.getLogger(__name__)
from nchantrs.widgets.widgets import NchantdWidgetMixin
from typing import Optional, Dict, List, Any, Tuple
from ogma.logma import Logma

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
log = False
logma = Logma(__name__)

# ===============================================================================||
pxcfg = join(here, "_data_", "items.yaml")
pxcfg = {}


class NchantdItem(NchantdWidgetMixin, pyqt.QStandardItem):
    """ """

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdItem")
        self.catalog = parent.catalog
        NchantdWidgetMixin.__init__(self)
        pyqt.QStandardItem.__init__(self, parent)
        self.config.override(cfg)
        self.tree = None

    def initModel(self) -> None:
        """ """
        self.init_variables()
        super().initModel()
        return self

    def initView(self) -> None:
        """ """
        super().initView()
        self.setModel(self.parent.model)
        self.initUI()
        self.initContextMenu()
        self.initTriggers()
        self.setLayout(self.view.layout)
        return self

    def initWidget(self) -> None:
        """ """
        self.model()
        self.view()
        return self

    def initContextMenu(self) -> None:
        """ """
        self.setContextMenuPolicy(pyqt.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onRightClick)
        return self

    def initTriggers(self) -> None:
        """ """
        logma.info(f"Init Triggers")
        self.doubleClicked.connect(self.onLeftDoubleClick)
        self.expanded.connect(self.onExpand)
        self.clicked.connect(self.onLeftClick)
        return self

    def onExpand(self) -> None:
        """ """
        return self

    def onRightClick(self, signal=None) -> None:
        """ """
        logma.info(f"Right Click")
        return self

    def onLeftDoubleClick(self, signal) -> None:
        logma.info(f"Left Double Click")
        return self

    def onLeftClick(self, signal) -> None:
        """"""
        return self

    def onMiddleClick(self) -> None:
        """ """
        logma.info(f"Middle Click")
        return self

    def onSelection(self, fx, mod=None) -> None:
        """On selection of tree node load data for tabs in center widget"""
        event.on_clickleft_press(fx)

        return

    def onDeselection(self, fx, mod=None) -> None:
        """On deslection of tree node save any changes to node options"""
        event.on_clickleft_release(fx)
        return

    def onEnter(self, fx, mod=None) -> None:
        """Need to build if a node was selected an enter create a new sibling
        node. shift-enter creates a new child node, ctrl-enter creates
        a new tab in the node"""
        event.on_enter_kp(fx, mod)
        return

    def onDelete(self, fx, mod=None) -> None:
        """Launch Dialog to confirm deletion of node, which marks as deleted in database
        and is not removed until a database cleanup is run"""


# expand this to allow for multiple connections to content and only delete
# connections until no connections are left then remove content...this requires
# the knowledge of parents by their children


class NchantdTreeItem(NchantdWidgetMixin, pyqt.QTreeWidgetItem):
    """ """

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        NchantdWidgetMixin.__init__(self)
        pyqt.QTreeWidgetItem.__init__(self, parent)
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdTreeItem").override(cfg)
        self.app = self.parent.app

    def initModel(self, cfg) -> None:
        """ """
        super().initModel(cfg)
        return self

    def initView(self, cfg) -> None:
        """ """
        super().initView(cfg)
        return self

    def initWidget(self) -> None:
        """ """
        self.model()
        self.view()
        return self


# ===========================Code Source Examples================================||
"""
"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
