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
from os.path import dirname, join

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.dialogs.sigil import NchantdSigilMixin
# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "colors.yaml")


class NchantdColorSelectSigil(NchantdSigilMixin, pyqt.QColorDialog):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent.app.main)
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdColorSelectSigil").override(parent.config).override(cfg)
        self.init_variables()
        logma.info(f"NchantdColorSelectSigil initialized")


    def initModel(self, cfg=None) -> None:
        """"""
        return self

    def initView(self, cfg=None) -> None:
        """"""
        self.setGeometry(150, 250, 1000, 600)
        # self.hide_title()
        return self

    def initWidget(self) -> None:
        """"""
        self.initModel()
        self.initView()
        self.color = self.getColor()
        # self.run()
        return self

    def accept(self) -> None:
        """"""
        super().accept()
        self.set_ok()
        return self

    def get_color(self) -> None:
        """"""
        return self.color

    def set_ok(self) -> None:
        """"""
        self.ok = True
        return self

    def reject(self) -> None:
        """"""
        super().reject()

    def run(self) -> None:
        """"""
        self.exec()


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
