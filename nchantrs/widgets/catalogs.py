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
from os import listdir
import json as j

import logging


logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||
from pandas import DataFrame

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.widgets.annotations import NchantdLabel
from typing import Optional, Dict, List, Any, Tuple
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.media.editors.editors import NchantdEntryEditor
from nchantrs.widgets.media.images import NchantdImage
from nchantrs.widgets.groups import NchantdGridScrollGroupBox
from nchantrs.widgets.items.catalogs import NchantdCatalogItem
from nchantrs.widgets.panes.catalogs import NchantdNewNodePane
from nchantrs.widgets.widgets import NchantdWidget
from ogma.logma import Logma
from subtrix.utilities import uuid

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "catalogs.yaml")
pxcfg = {}


class NchantdCatalog(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdCatalog"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.catalog = self
        self.selected_item = None
        self.all_items = None
        self.display = None
        self.display_items = None
        self.item_pane = None
        self.item_pane_layout = None
        self.item_pane_group = None

    def initModel(self, cfg=None) -> None:
        """"""
        super().initModel(cfg)
        self.all_items = DataFrame()
        self.display_items = self.all_items
        return self

    def init_pre_view(self) -> None:
        """"""
        if self.layout is None:
            super().initView()

    def initView(self, item_obj=None, pane_obj=None) -> None:
        """Create a scrollable self building grid"""
        self.init_pre_view()
        if self.display is None:
            cfg = {}
            self.display = NchantdGridScrollGroupBox(self, cfg)
            self.display.set_minimum_height(self.size().height() - 500)  [DONE]
            self.display.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
            self.display.setTitle(self.config.dikt.get("title", "New Item Catalog"))
            self.display.limit_horizontal()
            self.layout.addLayout(self.display.layout)

            row, col = 0, 0
            logma.info(f"Display Items {self.display_items.head()}")
            if self.display_items.empty:
                return self
            df = self.display_items.sort_values(by=["sequence_int"])
            if not df.empty:
                if item_obj is None:
                    item_obj = NchantdCatalogItem
                for i, item in df.iterrows():
                    if col >= 4:
                        row += 1
                        col = 0
                    cfg = {
                        "text": item.get("name_txt", ""),
                        "description": item.get("description_ltxt", ""),
                        "action": item.get("action_txt", "load_catalog_item"),
                        "local_available": item.get("local_available_bit", ""),
                        "file_type": item.get("file_type_txt", ""),
                        "icon_txt": item.get("icon_txt", item.get("name_txt", "")),
                        "handler": self.update_item_pane,
                        # "size": ["auto", "auto"],
                    }
                    item_obj_inst = item_obj(self, cfg).initWidget()
                    self.display.addWidget(item_obj_inst, row, col)
                    if col == 0 and row == 0:
                        self.item_selected(item_obj_inst)
                    col += 1
        if self.item_pane_group is None:
            self.item_pane_group = pyqt.QGroupBox()
            if pane_obj is None:
                pane_obj = NchantdNewNodePane
            logma.info(f"Pane Obj")
            cfg = {"options": self.all_items["name_txt"].values.tolist()}
            logma.info(f"CFG {cfg}")
            self.item_pane = pane_obj(self, cfg).initWidget()
            # logma.info(f"Pane Obj {self.item_pane.config.dikt["action"]}")
            self.item_pane_group.setTitle("New Item Pane")
            self.item_pane_group.setMaximumHeight(250)
            self.item_pane_group.setMinimumHeight(250)
            self.item_pane_layout = pyqt.QHBoxLayout()
            self.item_pane_group.setSizePolicy(pyqt.QSizePolicy.Policy.Expanding, pyqt.QSizePolicy.Policy.Expanding)
            self.item_pane_group.setLayout(self.item_pane_layout)
            self.item_pane_layout.addWidget(self.item_pane)
            self.layout.addWidget(self.item_pane_group)
        return self

    def initWidget(self) -> None:
        """"""
        self.initModel()
        self.initView()
        return self

    def item_selected(self, child) -> None:
        """"""
        self.selected_item = child
        self.update_item_pane()
        return self

    def update_item_pane(self) -> None:
        """"""
        logma.info(f"Selected Item {self.selected_item.action} {self.item_pane}")
        if self.selected_item is None or self.item_pane is None:
            return self
        self.item_pane.update_pane()
        return self


class NchantdImageCatalog(NchantdCatalog):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("Nchantd")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self) -> None:
        """"""
        super().initModel()
        return self

    def initView(self) -> None:
        """"""
        super().initView()
        # directory load widget
        cfg = {"text": "Load Path", "layout": "horizontal", "size": "small"}
        entry = NchantdEntryEditor(self, cfg).initWidget()
        self.layout.addWidget(entry)
        self.loadPath()
        return self

    def loadPath(self) -> None:
        """"""
        # path = '/home/solubrew/_work/collectImages'
        # grid_w = pyqt.QWidget()
        # grid = pyqt.QGridLayout(grid_w)
        # scroll = pyqt.QScrollArea()
        # max_col = 5
        # for i, f_ in enumerate(listdir(path)):
        # 	img = NchantdImage(self).setPath(join(path, f_))
        # 	if img is None:
        # 		continue
        # 	row = int(i / max_col)
        # 	col = int(i % max_col)
        # 	grid.addWidget(img, row, col, 1, 2)
        # scroll.setWidget(grid_w)
        # self.layout.addWidget(scroll)

        path = "/home/solubrew/_work/collectImages"
        grid = NchantdGridScrollGroupBox()
        grid.setTitle("Image Catalog")
        max_col = 5
        for i, f_ in enumerate(listdir(path)):
            cfg = {"path": join(path, f_)}
            img = NchantdImage(self, cfg).initWidget()
            img.setPath(join(path, f_))
            if img is None:
                continue
            row = int(i / max_col)
            col = int(i % max_col)
            grid.addWidget(img, row, col)
        self.layout.addWidget(grid.layout)

    def initWidget(self) -> None:
        """"""
        self.initModel()
        self.initView()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
