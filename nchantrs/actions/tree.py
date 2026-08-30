"""
---
<(META)>:
        docid: 62ea7f1-d120-4d97-92b4-2ed26d0aee4a
        name:
        description: >
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""
import datetime as dt
import logging
from os.path import abspath, dirname, join
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)
from kahndor import kahndor
from kahndor.logma import Logma

from nchantrs.dialogs.new import NewNchantdNodeSigil

here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'tree.yaml')
