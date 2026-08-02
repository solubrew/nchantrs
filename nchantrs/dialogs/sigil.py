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
from os.path import abspath, dirname, join
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidgetMixin, loadWidget
from nchantrs.themes.themes import NchantdTheme
HERE = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
if not log:
    logma.off()
PXCFG = join(HERE, '_data_', '.yaml')

class NchantdSigilMixin(NchantdWidgetMixin):
    """"""

    def init_variables(self, name='generic') -> Any:
        """"""
        super().init_variables()
        self.layout = None
        self.pane = None
        self.ok = None
        self.buttons = None
        self.new = True
        self.open = False
        gui = self.config.dikt.get('gui', None)
        if gui is None:
            raise
        self.dtop = gui.get('dialogs', {}).get(name, None)
        if self.dtop is None:
            self.dtop = gui.get('dialogs', {}).get('base', None)
        self.new_form_field = None
        self.new_form_field_style = None
        self.add_field_button = None
        return self

    def validate(self) -> Any:
        logma.info(f'validate called')
        return self

    def accept_(self, *args, **kwargs) -> Any:
        """"""
        logma.info(f'Accept')
        self.validate()
        self.set_ok()
        return self

    def add_field(self, field_wdgt) -> Any:
        """"""
        self.layout.addWidget(field_wdgt)
        return self

    def buildPane(self, style='1pane') -> None:
        """"""
        cnt = 0
        for position in self.config.dikt['styles'][style]['positions']:
            logma.info(f"Load Widget {self.dtop['layout'][position]}")
            self.pane[position] = loadWidget(self, self.dtop['layout'][position], style)
            self.pane[position].initWidget()
            self.model.registerListener(self.pane[position])
            self.layout.addWidget(self.pane[position], cnt)
            cnt += 1

    def getData(self) -> Any:
        if self.records == None:
            return self.defaults
        return self.records

    def hide_title(self) -> None:
        """"""
        self.setWindowFlags(pyqt.Qt.FramelessWindowHint)

    def increase_font_size(self, value) -> None:
        logma.info(f'increase_font_size called')
        return self

    def increase_height(self, value) -> None:
        """"""
        if '%' in value:
            height = self.height() * (1 + int(value.replace('%', '')) / 100)
            self.resize(self.width(), height)
        else:
            height = self.height() + int(value)
            self.resize(self.width(), height)

    def increase_width(self, value) -> None:
        """"""
        if '%' in value:
            width = self.width() * (1 + int(value.replace('%', '')) / 100)
            self.resize(width, self.height())
        else:
            width = self.width() + int(value)
            self.resize(width, self.height())

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """Build the dialog from the provided parameters"""
        super().initView(cfg)
        self.setWindowFlags(self.windowFlags() | pyqt.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(self.dtop.get('title', ''))
        self.pane = {}
        self.setAttribute(pyqt.Qt.WA_DeleteOnClose)
        theme = NchantdTheme(self)
        theme.set_theme('midnight_mist')
        style = self.dtop['layout']['style']
        if style is None:
            style = '1Pane'
        singlepane = False
        if style == '1Pane':
            singlepane = True
        if self.config.dikt.get('build', None):
            self.buildPane(style)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def reject_(self, signal=None, *args, **kwargs) -> Any:
        logma.info(f'reject_ called')
        return self

    def set_ok(self) -> Any:
        """"""
        self.ok = True
        return self

    def setDefaults(self, defaults) -> Any:
        """ """
        self.defaults = defaults
        return self

    def set_font_size(self, size) -> None:
        logma.info(f'set_font_size called')
        return self

    def set_position(self, where='center') -> Tuple[Any, Any]:
        """"""
        match where:
            case 'center':
                x, y = self.set_position_center()
            case 'right':
                x, y = self.set_position_right()
        return (x, y)

    def set_position_center(self) -> Tuple[Any, Any]:
        """"""
        x = self.app.view.gui.geometry().center().x() - self.geometry().width() // 2
        y = self.app.view.gui.geometry().center().y() - self.geometry().height() // 2
        self.move(x, y)
        return (x, y)

    def set_position_right(self) -> Tuple[Any, Any]:
        """"""
        x = self.app.view.gui.geometry().center().x() - self.geometry().width() * 0.8
        y = self.app.view.gui.geometry().center().y() - self.geometry().height() // 2
        self.move(x, y)
        return (x, y)

    def set_size(self, width=400, height=200, left=150, top=250) -> None:
        """"""
        left_ = None
        top_ = None
        width_ = None
        height_ = None
        if 'size' in self.dtop.keys():
            left_ = self.dtop['size'].get('left', left)
            top_ = self.dtop['size'].get('top', top)
            width_ = self.dtop['size'].get('width', width)
            height_ = self.dtop['size'].get('height', height)
        if left_ is not None:
            left = left_
        if top_ is not None:
            top = top_
        if width_ is not None:
            width = width_
        if height_ is not None:
            height = height_
        self.setGeometry(left, top, width, height)

    def setSource(self, src) -> Any:
        self.src = src
        return self