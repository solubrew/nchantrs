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
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.widgets.groups import NchantdGridScrollGroupBox
from nchantrs.widgets.tabsets import NchantdTab
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.libraries import pyqt

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
log = False
if not log:
    logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "toolboxes.yaml")


class NchantdDrawer(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdDrawer").override(cfg))
        self.group = None
        self.items = None

    def initModel(self):
        """"""
        super().initModel()
        self.items = {}
        return self

    def initView(self):
        """"""
        super().initView()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        drawer_group = NchantdGridScrollGroupBox(self)
        drawer_group.limit_horizontal()
        row, col = 0, 0
        self.config.dikt["rows"] = 0
        items = self.config.dikt.get("items", {})
        if items is None:
            items = {}
        logma.info(f"Drawer Items: {items}")
        logma.info(f"Number of items: {len(items)}")
        for i, item in items.items():
            logma.info(f"Processing item {i}: {item}")
            self.items[i] = item
            widget = self.items[i].get("widget", None)
            logma.info(f"Widget for item {i}: {widget}")
            if widget is None:
                logma.warning(f"Item {i} has no widget, skipping")
                continue
            widget.initWidget()
            self.items[i]["widget"] = widget
            drawer_group.addWidget(widget, row, col)
            logma.info(f"Added widget for item {i} at row {row}")
            row += 1

        logma.info(f"Total widgets added to drawer: {row}")
        self.layout.addLayout(drawer_group.layout)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdToolBox(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdToolBox").override(cfg))
        self.box = None
        self.drawers = None
        self.name = "ToolBox"
        self.position = None
        self.toolbox_config = None
        self.current_document = None

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        self.build_toolbox(cfg)
        self.box.layout().update()
        self.box.currentChanged.connect(self.on_drawer_changed)
        return self

    def initWidget(self, cfg=None):
        """"""
        self.initModel(cfg)
        self.initView(cfg)
        return self

    def add_drawer(self, drawer, items=None):
        """"""
        cfg = {"items": items.get("items", {})}
        # self.drawers[drawer] = NchantdDrawer(self, cfg).initWidget()
        self.box.addItem(NchantdDrawer(self, cfg).initWidget(), items.get("title", "Mystery Drawer"))
        return self

    def add_drawer_lazy(self, drawer, items=None):
        """"""
        if items is None:
            items = {}
        self.drawers[drawer] = {"widget": self.add_dummy_widget(), "loaded": False}
        logma.info(f"Add Drawer {drawer}")
        idx = self.box.addItem(self.drawers[drawer]["widget"], items.get("title", "Mystery Drawer"))
        logma.info(f"Index {idx}")
        self.drawers[drawer]["idx"] = idx
        self.drawers[drawer]["cfg"] = {"items": items.get("items", {})}
        return self

    def add_dummy_widget(self):
        """"""
        widget = pyqt.QWidget()
        layout = pyqt.QVBoxLayout()
        layout.addWidget(pyqt.QLabel("Dummy Widget"))
        widget.setLayout(layout)
        return widget

    def build_toolbox(self, cfg=None):
        """"""
        # logma.inspect_caller()
        current_document = self.app.view.panes["center"].currentWidget()
        self.box = pyqt.QToolBox()
        self.box.currentChanged.connect(self.on_drawer_changed)
        if current_document is not None:
            logma.info(f"Config Toolbox {self.config.dikt.get("toolbox", {})}")  # [0]["items"]}")
            try:
                cfg = {"toolbox": current_document.toolbox_config}
                cfg = kahndor.Instruct(cfg).override(cfg).override(self.config.dikt).get("toolbox", {})
            except Exception as e:
                logma.warning(e)
                cfg = {}
            default_cfg = self.config.dikt.get("default", {})
            cfg = cfg or default_cfg
            cfg = dict(sorted(cfg.items()))
            self.drawers = {}
            for drawer, items in cfg.items():
                logma.info(f"Add Drawer {drawer} {items}")
                if drawer == 0:
                    self.add_drawer(drawer, items)
                else:
                    self.add_drawer_lazy(drawer, items)
            self.layout.addWidget(self.box)
        return self

    def clear(self):
        """Manually remove all items in the QToolBox."""
        if self.drawers is not None:
            logma.info(f"Clear Toolbox {self.drawers.keys()}")
            for index in range(len(self.drawers) - 1, -1, -1):  # Loop in reverse
                logma.info(f"Remove Drawer {index}")
                widget = self.box.widget(index)
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
                self.box.removeItem(index)
            self.layout.removeWidget(self.box)

    def init_toolbox(self):
        """"""
        return self

    @pyqt.Slot(int)
    def load_drawer(self, idx: int):
        """"""
        logma.info(f"load_drawer called for index {idx}")
        # Find drawer key by matching index
        drawer_key = None
        drawer_data = None
        for key, data in self.drawers.items():
            logma.info(f"Checking drawer key={key}, data idx={data.get('idx')}, loaded={data.get('loaded')}")
            if data.get("idx") == idx:
                drawer_key = key
                drawer_data = data
                break

        # If not found, nothing to do
        if drawer_key is None:
            logma.info(f"Drawer at index {idx} not found in drawers dict")
            return self

        # If already loaded, nothing to do
        if drawer_data.get("loaded", False):
            logma.info(f"Drawer at index {idx} already loaded")
            return self

        logma.info(f"Building drawer {drawer_key} at index {idx}")
        try:
            drawer = NchantdDrawer(self, drawer_data.get("cfg", {})).initWidget()
            drawer_data["widget"] = drawer
            drawer_data["loaded"] = True
            logma.info(f"Successfully built drawer {drawer_key}")
        except Exception as e:
            logma.error(f"Failed to build drawer {drawer_key}: {e}")
            # If building fails, show a simple error page, but keep toolbox functional
            drawer = pyqt.QWidget()
            lay = pyqt.QVBoxLayout(drawer)
            msg = pyqt.QLabel(f"Failed to load drawer content:\n{e}")
            msg.setStyleSheet("color: #b00;")
            lay.addWidget(msg)
            drawer_data["widget"] = drawer
            drawer_data["loaded"] = True

        # Preserve title and icon, replace at the same index
        title = self.box.itemText(idx)
        icon = self.box.itemIcon(idx)

        # Get old widget and prepare to delete it
        old_widget = self.box.widget(idx)

        self.box.blockSignals(True)
        try:
            self.box.removeItem(idx)
            if icon.isNull():
                self.box.insertItem(idx, drawer, title)
            else:
                self.box.insertItem(idx, drawer, icon, title)
            self.box.setCurrentIndex(idx)
            # Delete old dummy widget
            if old_widget is not None:
                old_widget.deleteLater()
            logma.info(f"Replaced dummy widget with real drawer at index {idx}")
        finally:
            self.box.blockSignals(False)
        return self

    def on_drawer_changed(self, index):
        """"""
        # self.drawers[list(self.drawers.keys())[index]].initWidget()
        logma.info(f"Current Drawer {index}")
        self.load_drawer(index)
        # self.box.layout().update()
        return self

    def on_drawer_selected(self, index):
        """
        Handle drawer selection and lazily load its contents when accessed.
        """
        # # Connect currentChanged signal to lazy loading function
        # self.toolbox.currentChanged.connect(self.on_drawer_selected)
        # if index < 0:
        #     return  # Invalid index, nothing to do
        # # Check if the drawer is already loaded
        # if index in self.loaded_drawers:
        #     print(f"Drawer {index + 1} is already loaded. Skipping.")
        #     return
        # # Mark this drawer as loaded
        # self.loaded_drawers.add(index)
        # print(f"Loading content for Drawer {index + 1}...")
        # # Create content (e.g., labels, widgets) dynamically for the selected drawer
        # drawer_widget = QWidget()
        # drawer_layout = QVBoxLayout()
        # # Simulate the dynamic content (you can replace this with actual logic)
        # for i in range(5):
        #     drawer_layout.addWidget(QLabel(f"Item {i + 1} in Drawer {index + 1}"))
        # drawer_widget.setLayout(drawer_layout)
        # # Replace the placeholder widget with the loaded content
        # self.toolbox.setItem(index, drawer_widget)
        # print(f"Content for Drawer {index + 1} loaded successfully.")

    def setItem(self, index, widget):
        """
        Replace a drawer's placeholder widget with its actual content.
        """
        existing_widget = self.toolbox.widget(index)
        self.toolbox.removeItem(index)
        existing_widget.deleteLater()
        self.toolbox.insertItem(index, widget, f"Drawer {index + 1}")


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
