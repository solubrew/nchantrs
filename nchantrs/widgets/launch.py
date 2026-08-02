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
from os.path import dirname, join
from kahndor import kahndor
import logging
logger = logging.getLogger(__name__)
from nchantrs.wizards.accounts import NchantdNewApplicationWizard
from nchantrs.widgets.widgets import NchantdWidget
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')