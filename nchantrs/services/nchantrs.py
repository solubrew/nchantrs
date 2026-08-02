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
from os.path import dirname, join
from typing import Any, Dict, List, Optional
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from nchantrs.services.services import NchantdService
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')

class NchantdApplicationService(NchantdService):
    """The Nchantrs Service connects to an Nchnatd family of websites and pulls default data needed by the desktop
    applications"""

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select('NchantdApplicationService')
        super().__init__(self)
        self.config.override(cfg)
        logma.info(f'NchantdApplicationService initialized')

    def get_app_updates(self) -> None:
        logma.info(f'get_app_updates requested')
        return None

    def get_app_actions(self) -> Any:
        logma.info(f'get_app_actions requested')
        return None

    def get_app_document_types(self) -> Any:
        logma.info(f'get_app_document_types requested')
        return None

    def get_app_link_affiliate_substitutions(self) -> Any:
        logma.info(f'get_app_link_affiliate_substitutions requested')
        return None

    def get_app_menus(self) -> Any:
        logma.info(f'get_app_menus requested')
        return None

    def get_app_options(self) -> Any:
        logma.info(f'get_app_options requested')
        return None

    def get_app_option_keys(self) -> Any:
        logma.info(f'get_app_option_keys requested')
        return None

    def get_app_policies(self) -> Any:
        logma.info(f'get_app_policies requested')
        return None

    def get_doc_tags(self) -> Any:
        logma.info(f'get_doc_tags requested')
        return None

    def get_doc_tag_groups(self) -> Any:
        logma.info(f'get_doc_tag_groups requested')
        return None