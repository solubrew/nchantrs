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
from condor import condor
from nchantrs.dialogs.dialogs import NchantdCape
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class NewPasswordDialog(NchantdCape):
    """"""

    def __init__(self, parent, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg)
        if parent is not None:
            self.config.override(parent.config)
        self.parent = parent
        self.config.override(cfg)
        super(NchantdCape, self).__init__(parent, self.config)


class ChangePasswordDialog(NchantdCape):
    """"""

    def __init__(self, parent, cfg=None):
        """"""
        self.config = condor.Instruct(parent)
        if parent is not None:
            self.config.override(parent.config)
        self.parent = parent
        self.config.override(cfg)

    def _check_current_password(self):
        """"""

    def _set_new_password(self):
        """"""


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
