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
from typing import Optional, Dict, List, Any, Tuple

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma

from nchantrs.dialogs.dialogs import NchantdSigil
from nchantrs.widgets.controls.checkboxes import NchantdCheckboxGroup

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class NchantdSettingsSigil(NchantdSigil):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdSettingsSigil").override(cfg))
        logma.info(f"NchantdSettingsSigil initialized")


    def initModel(self) -> None:
        """"""
        super().initModel()
        return self

    def initView(self) -> None:
        """"""
        super().initView()
        cfg = {}
        self.main_settings = NchantdCheckboxGroup(self, cfg).initWidget()
        return self

    def initWidget(self) -> None:
        """"""
        self.initModel()
        self.initView()
        return self

    def on_save(self) -> None:
        """"""


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
