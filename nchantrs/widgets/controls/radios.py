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
from typing import Any, Optional, Dict

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")
log = True
logma = Logma(__name__)


# ====================================================================================================================||
pxcfg = join(here, "_data_", "radios.yaml")


class NchantdRadioButton(NchantdWidgetMixin, pyqt.QRadioButton):
    def __init__(self, parent: Any, cfg: Optional[Dict] = None) -> None:
        """https://www.tutorialspoint.com/pyqt/pyqt_qradiobutton_self.htm"""
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdRadioButton")
        if parent:
            self.config.override(parent.config)
        super().__init__(self.parent)
        self.config.override(cfg)
        self.init_variables()

    def initModel(self) -> "NchantdRadioButton":
        """"""
        return self

    def initView(self) -> "NchantdRadioButton":
        """"""
        self.setChecked(self.config.dikt.get("checked", False))
        self.setText(self.config.dikt.get("text", ""))
        return self

    def initWidget(self) -> "NchantdRadioButton":
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdRadioButtonGroup(NchantdWidget):
    """"""

    def __init__(self, parent: Optional[Any] = None, cfg: Optional[Dict] = None) -> None:
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdRadioButtonGroup")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self.parent, self.config)
        self.radios: Dict[int, Any] = {}
        self.label: Optional[Any] = None

    def initModel(self) -> "NchantdRadioButtonGroup":
        """"""
        super().initModel()
        return self

    def initView(self) -> "NchantdRadioButtonGroup":
        """"""
        super().initView({"layout": self.config.dikt.get("layout", "vertical")})
        cfg = {"text": self.config.dikt.get("text", "")}
        self.label = NchantdLabel(self, cfg).initWidget()
        self.layout.addWidget(self.label)
        cnt = 0
        checked = False
        for option in self.config.dikt.get("unique_options", []):
            if cnt == 0:
                checked = True
            cfg = {"text": option, "checked": checked}
            self.radios[cnt] = NchantdRadioButton(self, cfg).initWidget()
            self.layout.addWidget(self.radios[cnt])
            cnt += 1
        return self

    def initWidget(self) -> "NchantdRadioButtonGroup":
        """"""
        self.initModel()
        self.initView()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
