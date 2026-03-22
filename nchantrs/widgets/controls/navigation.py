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

import logging


logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import pyqt
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")
pxcfg = {}


class NchantdNavigationButtons(pyqt.QWidget):
    """ """

    def __init__(self, parent=None, cfg={}):
        """ """
        self.config = condor.Instruct(pxcfg).override(cfg)
        self.config.select("NchantdNavigationButtons")
        if parent:
            self.config.override(parent.config)
        self.parent = parent
        pyqt.QWidget.__init__(self)
        self.layout = pyqt.QHBoxLayout()
        if log:
            logma.info(f"Nchantd Submission Buttons {self.config.dikt}")
        self.config.dikt["buttons"]["next"]["text"] = "Next"
        self.prevbutton = NchantdButton(self, self.config.dikt["buttons"]["prev"])
        self.prevbutton.initWidget()
        self.layout.addWidget(self.prevbutton)
        self.config.dikt["buttons"]["jump"]["input"] = ""
        self.jumpinput = editors.NchantdEntryEditor(self, self.config.dikt["buttons"]["input"])
        self.jumpinput.initWidget()
        self.layout.addWidget(self.jumpinput)
        self.config.dikt["buttons"]["jump"]["text"] = "Jump"
        self.jumpbutton = NchantdButton(self, self.config.dikt["buttons"]["jump"])
        self.jumpbutton.initWidget()
        self.layout.addWidget(self.jumpbutton)
        self.config.dikt["buttons"]["prev"]["text"] = "Prev"
        self.nextbutton = NchantdButton(self, self.config.dikt["buttons"]["next"])
        self.nextbutton.initWidget()
        self.layout.addWidget(self.nextbutton)
        self.setLayout(self.layout)

    def initWidget(self):
        """ """
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
