from typing import Any

"\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n"
from os.path import abspath, dirname, join
import datetime as dt
import logging

logger = logging.getLogger(__name__)
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.themes.themes import NchantdTheme
from kahndor.logma import Logma

here = join(dirname(__file__), "")
log = True
logma = Logma(__name__)
pxcfg = join(here, "_data_", "wizards.yaml")


class NchantdWizard(pyqt.QWizard):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdWizard")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__()
        self.theme = NchantdTheme(self)
        self.set_theme(self.config.dikt["gui"]["desktop"]["theme"])

    def initModel(self, cfg=None) -> Any:
        """Initialize the wizard model."""
        logma.info(f"initModel {type(self).__name__}")
        # MUST BE IMPLEMENTED by subclasses
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        cancel_button = self.button(pyqt.QWizard.CancelButton)
        if cancel_button:
            cancel_button.clicked.connect(self.cmd_on_cancel)
        return self

    def initWizard(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    @pyqt.Slot()
    def cmd_on_cancel(self) -> Any:
        logma.critical("Cancel button clicked!")
        self.reject()
        return self

    def set_theme(self, theme="midnight_mist") -> None:
        """"""
        self.theme.set_theme(theme)
