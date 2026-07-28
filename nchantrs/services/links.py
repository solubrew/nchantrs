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

# ======================================3rd Party Library Modules=====================================================||

logger = logging.getLogger(__name__)

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from nchantrs.libraries import pyqt
from kahndor.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class LinkService:
    """
    This will be used to move link data this is specific to affiliates, operations and advertisements from the
    Nchantrs service to the Nchantd Applications
    """

    def __init__(self, parent, cfg: dict = None) -> None:
        """"""
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("").override(cfg)
        self.app = pyqt.QApplication.instance()

    def get_links(self) -> None:
        """
        need to send a request to a service and then parse the response

        :return:
        """

    def store_link(self, name: str, path: str, tags: str) -> None:
        """"""
        # FIX P9 (store_link kwarg mismatch):
        # LinkService.store_link() used to call
        # ``self.app.model.store_link(name=name, url=path, tag=tags)``.
        # ``NchantdOfficeCloakModel.store_link`` is the
        # ``NchantdCloakModel.store_link(name, url=None, tags=None)``
        # stub, which accepts ``tags`` (plural) — NOT ``tag``.
        # Passing ``tag=tags`` therefore raised::
        #
        #     TypeError: NchantdCloakModel.store_link() got an
        #         unexpected keyword argument 'tag'
        #
        # We keep the public kwarg ``tags=`` (singular-from-our-side
        # accepts a scalar string the way the rest of the codebase
        # treats it) and delegate to the underlying store_link
        # without renaming so any future signature change doesn't
        # silently break link tracking.
        try:
            self.app.model.store_link(name=name, url=path, tags=tags)
        except TypeError as e:
            # Defensive fallback: try both kwarg shapes. The
            # underlying store historically used ``tag=`` (singular)
            # for the NchantdStore base class; some deployments
            # still expose that name.
            if "tags" in str(e):
                try:
                    self.app.model.store_link(name=name, url=path, tag=tags)
                    return
                except TypeError:
                    pass
            raise


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
