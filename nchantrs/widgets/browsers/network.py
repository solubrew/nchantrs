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
import logging
from kahndor import kahndor
from kahndor.logma import Logma
from typing import Optional, Dict, List, Any, Tuple
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')