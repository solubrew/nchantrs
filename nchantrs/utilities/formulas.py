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
from os.path import abspath, dirname, join
import datetime as dt
from typing import Any, Dict, Optional, Any
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'formulas.yaml')

class NchantdFormula(object):
    """"""

    def __init__(self, formula: str, cfg: Optional[Dict[str, Any]]=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).override(cfg)
        self.formula = formula
        self.parsed_formula = self.parse()
        self.value: Optional[Any] = None

    def parse(self) -> 'NchantdFormula':
        logma.info(f'parse called')
        return self

    def compute(self, arguments: Optional[Dict[str, Any]]=None) -> Any:
        logma.info(f'compute called')
        return self

    def get_value(self, refresh: bool=False) -> Optional[Any]:
        """"""
        if self.value is None or refresh:
            self.compute()
        return self.value