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

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "search.yaml")


class Search:
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select("").override(cfg)


class TreeSearch(Search):
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select("").override(cfg)
        super().__init__(cfg)


class LocalFileSystemSearch(Search):
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select("").override(cfg)
        super().__init__(cfg)


class RemoteFileSystemSearch(Search):
    """Search all Connected Cloud File Systems"""

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select("").override(cfg)
        super().__init__(cfg)


class InternetSearch(Search):
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select("").override(cfg)
        super().__init__(cfg)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
