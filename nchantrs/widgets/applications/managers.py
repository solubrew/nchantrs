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

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma

from nchantrs.widgets.browsers.profiles import NchantdWebProfile
from nchantrs.widgets.widgets import NchantdWidget
from typing import Optional, Dict, List, Any, Tuple
from subtrix.subtrix import uuid

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "managers.yaml")


class NchantdProfileManager(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdProfileManager")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)
        self.profiles = {}
        logma.info(f"NchantdProfileManager initialized")


    def create_new_profile(self, name=None, profile_type=None) -> None:
        """"""
        if name is None:
            name = uuid()
        if profile_type == "web":
            browser = None
            self.profiles[name] = NchantdWebProfile(name, browser, self, self.config)
        else:
            self.profiles[name] = NchantdProfile()
        return self

    def initModel(self) -> None:
        """"""
        super().initModel()
        return self

    def initView(self) -> None:
        """"""
        super().initView()
        return self

    def initWidget(self) -> None:
        """"""
        self.initModel()
        self.initView()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
