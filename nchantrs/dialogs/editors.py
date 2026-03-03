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
from nchantrs.dialogs.settings import NchantdSettingsSigil
from nchantrs.widgets.controls.checkboxes import NchantdCheckbox

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "editors.yaml")


class NchantdJournalSettingsSigil(NchantdSettingsSigil):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdJournalSettingsSigil")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.append_only = True
        self.running_log = False
        self.main_settings = None

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        checkboxes = []
        for checkbox in self.config.dikt["checkboxes"]:
            checkbox_widget = NchantdCheckbox(self, checkbox)
            checkboxes.append(checkbox_widget)
        self.config.dikt["checkboxes"] = checkboxes
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def set_append_only(self, append_only):
        """"""
        self.append_only = append_only
        return self

    def set_rotate_time(self):
        """"""
        self.rotate_time = self.current_time + 24 * 60 * 60
        return self

    def set_running_log(self, running_log):
        """"""
        self.running_log = running_log
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
