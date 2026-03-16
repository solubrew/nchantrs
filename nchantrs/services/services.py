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

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "services.yaml")


class NchantdServiceManager(object):
    """"""

    def __init__(self, parent, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("NchantdServiceManager").override(cfg)
        self.app = parent
        self.is_update_available = False
        self.services = {}

    def add_service(self, service_name):
        """"""
        self.services[service_name] = NchantdService(service_name)

    def check_for_updates(self):
        """"""
        # if the user is paying for bundled nchantrs service then all updates are handled by the single service
        if "nchantrs" in self.services.keys():
            self.services["nchantrs"].check_for_updates(self.services)
        else:
            # otherwise the user will have to run updates individual against each service
            for service in self.services.keys():
                self.services[service].check_for_updates()
        self.is_update_available = False


class NchantdService(object):
    """"""

    def __init__(self, service_name, cfg=None):
        """"""
        self.service_name = service_name
        self.config = condor.Instruct(pxcfg).select("NchantdService").override(cfg)
        self.service = None
        self.is_update_available = False

    def set_api_key(self, api_key):
        """"""
        return self

    def set_service_object(self, service):
        """"""
        self.service = service
        return self

    def check_for_updates(self):
        """"""
        self.is_update_available = False
        return self


class NchantrsService(NchantdService):
    """Custom Service for Nchantrs Paid Users"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("NchantrsService").override(cfg)

    def check_for_updates(self):
        """"""
        super().check_for_updates()
        return self

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
