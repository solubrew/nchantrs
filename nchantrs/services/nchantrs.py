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
from typing import Any, Dict, List, Optional

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from nchantrs.services.services import NchantdService
from kahndor.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class NchantdApplicationService(NchantdService):
    """The Nchantrs Service connects to an Nchnatd family of websites and pulls default data needed by the desktop
    applications"""

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select("NchantdApplicationService")
        super().__init__(self)
        self.config.override(cfg)
        logma.info(f"NchantdApplicationService initialized")


    def get_app_updates(self) -> None:
        """"""

        return

    def get_app_actions(self) -> Any:
        """"""
        return self

    def get_app_document_types(self) -> Any:
        """"""
        return self

    def get_app_link_affiliate_substitutions(self) -> Any:
        """"""
        return self

    def get_app_menus(self) -> Any:
        """"""
        return self

    def get_app_options(self) -> Any:
        """"""
        return self

    def get_app_option_keys(self) -> Any:
        """"""
        return self

    def get_app_policies(self) -> Any:
        """"""
        return self

    def get_doc_tags(self) -> Any:
        """"""
        return self

    def get_doc_tag_groups(self) -> Any:
        """"""
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
