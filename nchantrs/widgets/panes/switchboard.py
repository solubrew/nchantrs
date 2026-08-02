# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
from typing import Any

"""
---
<(META)>:
        docid:
        name:
        description: >
            A NchantdSwitchboard Pane will be a pane that builds gui options for cli tools with a basic widet of what it will
            Do a button to activeate and entry fields for any options
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
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.widgets.widgets import NchantdWidget

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "switchboard.yaml")


class NchantdSwitchBoard(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdSwitchBoard").override(cfg))
        self.commands = None
        self.options = None
        logma.info(f"NchantdSwitchBoard initialized")


    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def add_command(self, command) -> None:
        """"""
        if self.commands is None:
            self.commands = []
        self.commands.append(command)

    def _parse_command(self, command) -> None:
        """"""
        return


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
