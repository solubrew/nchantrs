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
from os.path import dirname, join
import json as j
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.utilities.utils import lookup
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.items.items import NchantdItem
from typing import Optional, Dict, List, Any, Tuple
from kahndor.logma import Logma
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.widgets.media.images import NchantdImage
here = join(dirname(__file__), '')
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'catalogs.yaml')

class NchantdCatalogItem(NchantdWidget):
    """"""
    clicked = pyqt.Signal()

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdCatalogItem').override(cfg))
        self.catalog = self.parent.catalog
        self.title_txt = None
        self.subtitle_txt = None
        self.description_txt = None
        self.slug = None
        self.width = None
        self.height = None
        self.has_options = False
        self.clicked.connect(self.onLeftClick)

    def initModel(self, item_data=None) -> None:
        """ """
        self.icon_txt = self.config.dikt.get('icon_txt', 'dot-circle')
        super().initModel()
        item_cfg = self.action.action
        self.title_txt = self.config.dikt.get('text', 'Missing Title')
        if self.title_txt is None:
            self.title_txt = 'Missing Title'
        self.slug = self.title_txt.replace(' ', '').lower().strip()
        self.subtitle_txt = self.config.dikt.get('sub_text', None)
        self.description_txt = self.config.dikt.get('description', 'Missing Description')
        self.set_size()
        if item_cfg.get('icon_txt', None) is None or item_cfg.get('icon_txt', '') == '':
            item_cfg['icon_txt'] = self.icon_txt
        item_cfg['link'] = item_cfg.get('link', '')
        item_cfg['path'] = self.app.view.theme.get_icon_path(item_cfg['icon_txt'], 'base')
        item_cfg['size'] = item_cfg.get('size', [self.height, self.width])
        item_cfg['parameters_dict'] = j.dumps(item_cfg.get('parameters_dict', '{}').replace("'", '"'))
        self.item_cfg = item_cfg
        return self

    def initView(self, cfg=None) -> None:
        """ """
        if cfg is None:
            cfg = {}
        cfg['layout'] = cfg.get('layout', 'horizontal')
        super().initView(cfg)
        group = pyqt.QGroupBox()
        if self.width is not None:
            group.setMinimumSize(self.width * 1.4, self.width * 1.4)
        group.setFlat(True)
        group.setCheckable(False)
        group.setChecked(False)
        group.setCursor(pyqt.Qt.CursorShape.PointingHandCursor)
        if self.width is not None:
            group.setMaximumSize(self.width * 1.4, self.width * 1.4)
        group.setTitle(f'{self.title_txt}')
        font_size = 18
        if len(self.title_txt) > 8 and self.width is not None:
            font = group.font()
            font_size = 12
            font.setPointSize(font_size)
            group.setFont(font)
        group.setStyleSheet('\n                    QGroupBox {\n                        font: bold {font_size}px Arial;\n                    }\n                    QGroupBox::title {\n                        subcontrol-origin: margin;\n                        subcontrol-position: top center; /* Position at the top center */\n                        padding: 10 0px;\n                    }\n                '.replace('{font_size}', str(font_size)))
        group_layout = pyqt.QHBoxLayout()
        self.item_cfg['size'] = [128, 128]
        self.item_cfg['icon'] = self.item_cfg['path']
        logma.info(f'Item Config: {self.item_cfg}')
        image = NchantdImage(self, self.item_cfg).initWidget()
        image.setMinimumHeight(128)
        image.onLeftClick = self.onLeftClick
        group_layout.addWidget(image)
        group.setLayout(group_layout)
        if self.config.dikt.get('size_policy', None) == 'fixed':
            group.setSizePolicy(pyqt.QSizePolicy.Policy.Fixed, pyqt.QSizePolicy.Policy.Fixed)
        self.layout.addWidget(group)
        self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignLeft | pyqt.Qt.AlignmentFlag.AlignTop)
        self.setSizePolicy(pyqt.QSizePolicy.Policy.MinimumExpanding, pyqt.QSizePolicy.Policy.MinimumExpanding)
        return self

    def initWidget(self) -> None:
        """ """
        self.initModel()
        self.initView()
        return self

    def onLeftClick(self, signal=None) -> None:
        """"""
        logma.info(f'Catalog Left Click {signal}')
        super().onLeftClick(signal)
        logma.info(f'Left Click')
        self.catalog.item_selected(self)
        logma.info(f'Selected Item')
        return self

    def set_size(self) -> None:
        """"""
        self.width = self.config.dikt.get('width', None)
        self.height = self.config.dikt.get('height', None)
        return self

class NchantdAccountCatalogItem(NchantdCatalogItem):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select('NchantdAccountCatalogItem')
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        super().__init__(self)
        self.config.override(cfg)

    def initModel(self) -> None:
        """ """
        super().initModel()
        return self

    def initView(self) -> None:
        """ """
        super().initView()
        return self

    def initWidget(self) -> None:
        """ """
        self.initModel()
        self.initView()
        return self

class NchantdExtensionCatalogItem(NchantdCatalogItem):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select('NchantdExtensionCatalogItem')
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        super(NchantdExtensionCatalogItem, self).__init__()

    def initModel(self) -> None:
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> None:
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initView {{type(self).__name__}}')
        return self

    def initWidget(self) -> None:
        """ """
        self.initModel()
        self.initView()
        return self

class NchantdThemeCatalogItem(NchantdCatalogItem):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select('NchantdThemeCatalogItem')
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        super(NchantdThemeCatalogItem, self).__init__()

    def initModel(self) -> None:
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> None:
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initView {{type(self).__name__}}')
        return self

    def initWidget(self) -> None:
        """ """
        self.initModel()
        self.initView()
        return self