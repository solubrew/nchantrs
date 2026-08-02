from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.panes.panes import NchantdPane
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'calendars.yaml')

class NchantdCalendarDetailPane(NchantdPane):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdCalendarDetailPane')
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self.parent, self.config)
        self.config.override(cfg)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        group = pyqt.QGroupBox('Calendar Details')
        self.group_layout = pyqt.QVBoxLayout()
        group.setLayout(self.group_layout)
        self.group_layout.addStretch()
        self.layout.addWidget(group, stretch=1)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self