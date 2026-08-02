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
from typing import Dict, Any, Optional

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
pxcfg = join(here, "_data_", ".yaml")


# class NchantdApplicationSkeleton:
#     """"""
#
#     def __init__(self, path) -> None:
#         """"""
#         self.path = path
#
#     def create_folder_structure(self) -> None:
#         """"""
#         app_name = ""
#         app_name_lower = ""
#         app_code_name = ""
#         cfg = {"<[app_name]>": app_name, "<[app_name_lower]>": app_name_lower, "<[app_code_name]>": app_code_name}
#         for k, v in self.config.dikt.items():
#             if isinstance(v, dict):
#                 if "text" in v.keys():
#                     pass
#                 else:
#                     touch(join(path, k))


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
