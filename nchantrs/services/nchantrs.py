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
from typing import Optional, Dict, List

import logging


logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.services.services import NchantdService
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class NchantdApplicationService(NchantdService):
    """The Nchantrs Service connects to an Nchnatd family of websites and pulls default data needed by the desktop
    applications"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("NchantdApplicationService")
        super().__init__(self)
        self.config.override(cfg)

    def get_app_updates(self):
        """"""

        return

    def get_app_actions(self):
        """"""
        return self

    def get_app_document_types(self):
        """"""
        return self

    def get_app_link_affiliate_substitutions(self):
        """"""
        return self

    def get_app_menus(self):
        """"""
        return self

    def get_app_options(self):
        """"""
        return self

    def get_app_option_keys(self):
        """"""
        return self

    def get_app_policies(self):
        """"""
        return self

    def get_doc_tags(self):
        """"""
        return self

    def get_doc_tag_groups(self):
        """"""
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
