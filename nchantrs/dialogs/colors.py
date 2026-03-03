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

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from nchantrs.libraries import pyqt

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "colors.yaml")


class NchantdColorSelectSigil(pyqt.QColorDialog):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent.app.main)
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdColorSelectSigil")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self, cfg=None):
        """"""
        return self

    def initView(self, cfg=None):
        """"""
        self.setGeometry(150, 250, 1000, 600)
        # self.hide_title()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        self.color = self.getColor()
        # self.run()
        return self

    def accept(self):
        """"""
        super().accept()
        self.set_ok()
        return self

    def get_color(self):
        """"""
        return self.color

    def set_ok(self):
        """"""
        self.ok = True
        return self

    def reject(self):
        """"""
        super().reject()

    def run(self):
        """"""
        self.exec()


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
