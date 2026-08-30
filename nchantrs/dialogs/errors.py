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
import datetime as dt
import logging
from os.path import abspath, dirname, join
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)
from kahndor import kahndor
from kahndor.logma import Logma

from nchantrs.dialogs.dialogs import NchantdSigil
from nchantrs.widgets.annotations import NchantdLabel

here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'errors.yaml')

class NchantdErrorNotifySigil(NchantdSigil):
    """"""

    def __init__(self, name, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdErrorNotifySigil')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__('error', self.parent, self.config)

    def initModel(self) -> None:
        """"""
        super().initModel()
        return self

    def initView(self) -> None:
        """"""
        super().initView()
        self.config.override({'font': {'size': 20}})
        self.layout.addWidget(NchantdLabel(self, self.config).initWidget())
        self.hide_title()
        self.add_ok_button()
        return self
