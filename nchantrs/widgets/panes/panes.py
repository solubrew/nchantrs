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
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidget

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "panes.yaml")


class NchantdPane(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdPane").override(cfg))
        self.left_side_layout = None
        self.center_layout = None
        self.right_side_layout = None

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        cfg = cfg or {}
        if cfg.get("layout", None) is None:
            cfg = {"layout": "horizontal"}
        super().initView(cfg)
        if cfg["layout"] == "horizontal":
            logma.info("Initialize Horizontal Layout")
            self.left_side_layout = pyqt.QVBoxLayout()
            self.layout.addLayout(self.left_side_layout)
            self.center_layout = pyqt.QHBoxLayout()
            self.layout.addLayout(self.center_layout)
            self.right_side_layout = pyqt.QVBoxLayout()
            self.layout.addLayout(self.right_side_layout)
        # self.set_size()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def accept(self) -> Any:
        super().accpet()
        return self

    def update_pane(self) -> Any:
        """"""
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
