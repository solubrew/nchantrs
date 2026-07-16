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
from typing import Optional, Dict, List, Any, Tuple

import logging
from nchantrs.dialogs.dialogs import NchantdCape

logger = logging.getLogger(__name__)
from kahndor.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class NewPasswordDialog(NchantdCape):
    """"""

    def __init__(self, parent, cfg=None) -> None:
        """"""
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NewPasswordDialog").override(cfg))


class ChangePasswordDialog(NchantdCape):
    """"""

    def __init__(self, parent, cfg=None) -> None:
        """"""
        super()._init(parent, cfg)
        self.config.override(kahndor.Instruct(parent).select("ChangePasswordDialog").override(cfg))

    def _check_current_password(self) -> None:
        """"""

    def _set_new_password(self) -> None:
        """"""


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
