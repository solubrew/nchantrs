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
from os.path import abspath, dirname, join
import datetime as dt
from typing import Optional, Dict, List, Any, Tuple
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from nchantrs.dialogs.new import NewNchantdNodeSigil
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'tree.yaml')