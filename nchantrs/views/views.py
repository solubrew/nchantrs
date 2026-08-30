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
import logging
from os.path import abspath, dirname, join
from typing import Any, Dict, List, Optional, Tuple

from kahndor import kahndor
from kahndor.logma import Logma

here = join(dirname(__file__), '')
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')
