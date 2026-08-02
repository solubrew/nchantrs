from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.widgets.tables.tables import NchantdTableWidget
from nchantrs.widgets.widgets import NchantdWidget
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')

class NchantdPaletteTable(NchantdTableWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdPaletteTable').override(cfg))

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

class NchantdPalette(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdPalette')
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.color_picker = None
        self.palette_meta = None
        self.image = None
        self.color_table = None

    def initModel(self) -> Any:
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        cfg = {'size': ['auto', 600]}
        self.image = NchantdImage(self, cfg).initWidget()
        self.layout.addWidget(self.image)
        bottom_layout = pyqt.QHBoxLayout()
        cfg = {'fields': {}}
        cfg['fields'][0] = 'Palette Name'
        cfg['fields'][1] = 'Description'
        cfg['fields'][2] = 'Tags'
        cfg['fields'][3] = 'Lock Palette'
        cfg['fields'][4] = ''
        self.color_picker = NchantdDynamicEntryForm(self, cfg).initWidget()
        bottom_layout.addWidget(self.color_picker, stretch=1)
        cfg = {'num_columns': 3, 'num_rows': 10, 'size': ['auto', 'auto'], 'headers': ['Color Name', 'Hex Color', 'RGB Color', 'Launch Color']}
        self.color_table = NchantdPaletteTable(self, cfg).initWidget()
        bottom_layout.addWidget(self.color_table, stretch=1)
        self.layout.addLayout(bottom_layout)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self