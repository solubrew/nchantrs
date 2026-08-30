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
from os.path import dirname, join

from kahndor import kahndor

logger = logging.getLogger(__name__)
from kahndor.logma import Logma

from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.wizards.accounts import NchantdNewApplicationWizard

here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')
