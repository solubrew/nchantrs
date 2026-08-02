from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.widgets.groups import NchantdGridScrollGroupBox
from nchantrs.widgets.tabsets import NchantdTab
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.libraries import pyqt
here = join(dirname(__file__), '')
logma = Logma(__name__)
log = False
if not log:
    logma.off()
pxcfg = join(here, '_data_', 'toolboxes.yaml')

class NchantdDrawer(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdDrawer').override(cfg))
        self.group = None
        self.items = None

    def initModel(self) -> Any:
        """"""
        super().initModel()
        self.items = {}
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        drawer_group = NchantdGridScrollGroupBox(self)
        drawer_group.limit_horizontal()
        row, col = (0, 0)
        self.config.dikt['rows'] = 0
        items = self.config.dikt.get('items', {})
        if items is None:
            items = {}
        logma.info(f'Drawer Items: {items}')
        logma.info(f'Number of items: {len(items)}')
        for i, item in items.items():
            logma.info(f'Processing item {i}: {item}')
            self.items[i] = item
            widget = self.items[i].get('widget', None)
            logma.info(f'Widget for item {i}: {widget}')
            if widget is None:
                logma.warning(f'Item {i} has no widget, skipping')
                continue
            widget.initWidget()
            self.items[i]['widget'] = widget
            drawer_group.addWidget(widget, row, col)
            logma.info(f'Added widget for item {i} at row {row}')
            row += 1
        logma.info(f'Total widgets added to drawer: {row}')
        self.layout.addLayout(drawer_group.layout)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdToolBox(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdToolBox').override(cfg))
        self.box = None
        self.drawers = None
        self.name = 'ToolBox'
        self.position = None
        self.toolbox_config = None
        self.current_document = None

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        self.build_toolbox(cfg)
        self.box.layout().update()
        self.box.currentChanged.connect(self.on_drawer_changed)
        return self

    def initWidget(self, cfg=None) -> Any:
        """"""
        self.initModel(cfg)
        self.initView(cfg)
        return self

    def add_drawer(self, drawer, items=None) -> Any:
        """"""
        cfg = {'items': items.get('items', {})}
        self.box.addItem(NchantdDrawer(self, cfg).initWidget(), items.get('title', 'Mystery Drawer'))
        return self

    def add_drawer_lazy(self, drawer, items=None) -> Any:
        """"""
        if items is None:
            items = {}
        self.drawers[drawer] = {'widget': self.add_dummy_widget(), 'loaded': False}
        logma.info(f'Add Drawer {drawer}')
        idx = self.box.addItem(self.drawers[drawer]['widget'], items.get('title', 'Mystery Drawer'))
        logma.info(f'Index {idx}')
        self.drawers[drawer]['idx'] = idx
        self.drawers[drawer]['cfg'] = {'items': items.get('items', {})}
        return self

    def add_dummy_widget(self) -> Any:
        """"""
        widget = pyqt.QWidget()
        layout = pyqt.QVBoxLayout()
        layout.addWidget(pyqt.QLabel('Dummy Widget'))
        widget.setLayout(layout)
        return widget

    def build_toolbox(self, cfg=None) -> Any:
        """"""
        current_document = self.app.view.panes['center'].currentWidget()
        self.box = pyqt.QToolBox()
        self.box.currentChanged.connect(self.on_drawer_changed)
        if current_document is not None:
            logma.info(f"Config Toolbox {self.config.dikt.get('toolbox', {})}")
            try:
                cfg = {'toolbox': current_document.toolbox_config}
                cfg = kahndor.Instruct(cfg).override(cfg).override(self.config.dikt).get('toolbox', {})
            except Exception as e:
                logma.warning(e)
                cfg = {}
            default_cfg = self.config.dikt.get('default', {})
            cfg = cfg or default_cfg
            cfg = dict(sorted(cfg.items()))
            self.drawers = {}
            for drawer, items in cfg.items():
                logma.info(f'Add Drawer {drawer} {items}')
                if drawer == 0:
                    self.add_drawer(drawer, items)
                else:
                    self.add_drawer_lazy(drawer, items)
            self.layout.addWidget(self.box)
        return self

    def clear(self) -> None:
        """Manually remove all items in the QToolBox."""
        if self.drawers is not None:
            logma.info(f'Clear Toolbox {self.drawers.keys()}')
            for index in range(len(self.drawers) - 1, -1, -1):
                logma.info(f'Remove Drawer {index}')
                widget = self.box.widget(index)
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
                self.box.removeItem(index)
            self.layout.removeWidget(self.box)

    def init_toolbox(self) -> Any:
        logma.info(f'init_toolbox called')
        return self

    @pyqt.Slot(int)
    def load_drawer(self, idx: int) -> Any:
        """"""
        logma.info(f'load_drawer called for index {idx}')
        drawer_key = None
        drawer_data = None
        for key, data in self.drawers.items():
            logma.info(f"Checking drawer key={key}, data idx={data.get('idx')}, loaded={data.get('loaded')}")
            if data.get('idx') == idx:
                drawer_key = key
                drawer_data = data
                break
        if drawer_key is None:
            logma.info(f'Drawer at index {idx} not found in drawers dict')
            return self
        if drawer_data.get('loaded', False):
            logma.info(f'Drawer at index {idx} already loaded')
            return self
        logma.info(f'Building drawer {drawer_key} at index {idx}')
        try:
            drawer = NchantdDrawer(self, drawer_data.get('cfg', {})).initWidget()
            drawer_data['widget'] = drawer
            drawer_data['loaded'] = True
            logma.info(f'Successfully built drawer {drawer_key}')
        except Exception as e:
            logma.error(f'Failed to build drawer {drawer_key}: {e}')
            drawer = pyqt.QWidget()
            lay = pyqt.QVBoxLayout(drawer)
            msg = pyqt.QLabel(f'Failed to load drawer content:\n{e}')
            msg.setStyleSheet('color: #b00;')
            lay.addWidget(msg)
            drawer_data['widget'] = drawer
            drawer_data['loaded'] = True
        title = self.box.itemText(idx)
        icon = self.box.itemIcon(idx)
        old_widget = self.box.widget(idx)
        self.box.blockSignals(True)
        try:
            self.box.removeItem(idx)
            if icon.isNull():
                self.box.insertItem(idx, drawer, title)
            else:
                self.box.insertItem(idx, drawer, icon, title)
            self.box.setCurrentIndex(idx)
            if old_widget is not None:
                old_widget.deleteLater()
            logma.info(f'Replaced dummy widget with real drawer at index {idx}')
        finally:
            self.box.blockSignals(False)
        return self

    def on_drawer_changed(self, index) -> Any:
        """"""
        logma.info(f'Current Drawer {index}')
        self.load_drawer(index)
        return self

    def on_drawer_selected(self, index) -> None:
        logma.info(f'on_drawer_selected event received')
        if getattr(self, 'app', None) is not None and hasattr(self.app, 'model'):
            self.app.model.has_changed = True
        return self

    def setItem(self, index, widget) -> None:
        """
        Replace a drawer's placeholder widget with its actual content.
        """
        existing_widget = self.toolbox.widget(index)
        self.toolbox.removeItem(index)
        existing_widget.deleteLater()
        self.toolbox.insertItem(index, widget, f'Drawer {index + 1}')