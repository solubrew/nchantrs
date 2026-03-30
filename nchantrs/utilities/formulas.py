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
from typing import Any, Dict, Optional, Any

import logging

# ======================================3rd Party Library Modules=====================================================||

logger = logging.getLogger(__name__)

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "formulas.yaml")


class NchantdFormula(object):
    """"""

    def __init__(self, formula: str, cfg: Optional[Dict[str, Any]] = None) -> None:
        """"""
        self.config = condor.Instruct(pxcfg).override(cfg)
        self.formula = formula
        self.parsed_formula = self.parse()
        self.value: Optional[Any] = None

    def parse(self) -> "NchantdFormula":
        """
        need to parse and search out the base formulas used
        :return:
        """
        return self

    def compute(self, arguments: Optional[Dict[str, Any]] = None) -> Any:
        """"""
        return self

    def get_value(self, refresh: bool = False) -> Optional[Any]:
        """"""
        if self.value is None or refresh:
            self.compute()
        return self.value


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
