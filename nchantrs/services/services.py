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
from typing import Optional, Dict, List
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
RETURN_NONE = None
pxcfg = join(here, '_data_', 'services.yaml')

class NchantdServiceManager(object):
    """"""

    def __init__(self, parent, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select('NchantdServiceManager').override(cfg)
        self.app = parent
        self.is_update_available = False
        self.services = {}

    def add_service(self, service_name) -> None:
        """"""
        self.services[service_name] = NchantdService(service_name)

    def check_for_updates(self) -> None:
        """"""
        if 'nchantrs' in self.services.keys():
            self.services['nchantrs'].check_for_updates(self.services)
        else:
            for service in self.services.keys():
                self.services[service].check_for_updates()
        self.is_update_available = False

class NchantdService(object):
    """"""

    def __init__(self, service_name, cfg=None) -> None:
        """"""
        self.service_name = service_name
        self.config = kahndor.Instruct(pxcfg).select('NchantdService').override(cfg)
        self.service = None
        self.is_update_available = False

    def set_api_key(self, api_key) -> 'NchantdService':
        logma.info(f'set_api_key called')
        if hasattr(self, 'api_key'):
            logma.info(f'  has api_key attr')
        return self

    def set_service_object(self, service) -> 'NchantdService':
        """"""
        self.service = service
        return self

    def check_for_updates(self) -> 'NchantdService':
        """"""
        self.is_update_available = False
        return self

class NchantrsService(NchantdService):
    """Custom Service for Nchantrs Paid Users"""

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select('NchantrsService').override(cfg)

    def check_for_updates(self) -> 'NchantrsService':
        """"""
        super().check_for_updates()
        return self