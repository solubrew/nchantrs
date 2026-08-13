# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""#                                          ||
---  #                                          ||
<(META)>:  #                                          ||
    docid:   #                                          ||
    name:   #                                          ||
    description: >  #                                          ||
        Extendes the basic_js Item widget into the Nchantd Framework for cells
        with in a table...this will need to account for both data and metadata
        for the cell
    expirary: <[expiration]>  #                                          ||
    version: <[version]>  #                                          ||
    path: <[LEXIvrs]>  #                                          ||
    outline: <[outline]>  #                                          ||
    authority: document|this  #                                          ||
    security: sec|lvl2  #                                          ||
    <(WT)>: -32  #                                          ||
"""  # ||

# -*- coding: utf-8 -*-#                                          ||
# ================================Core Modules===================================||
from os.path import abspath, dirname, join
from typing import Optional, Dict, List, Any, Tuple

import logging

logger = logging.getLogger(__name__)
# ===============================================================================||

# ===============================================================================||
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.widgets import NchantdWidgetMixin

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ===============================================================================||
pxcfg = join(here, "_data_", "cells.yaml")


class NchantdCell(NchantdWidgetMixin, pyqt.QTableWidgetItem):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__()
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdCell").override(parent.config).override(cfg)
        self.auto_calculate = None
        self.label = None
        self.formula = None
        self.is_formula = False
        self.is_active = False
        default_color = "transparent"
        active_color = "#191cc2"
        self.row = self.config.dikt.get("row", None)
        self.column = self.config.dikt.get("column", None)
        self.default_color = default_color
        self.document = None
        self.active_color = active_color
        self.is_active = False
        logma.info(f"NchantdCell initialized")

    def initModel(self) -> None:
        """"""
        super().initModel()
        self.auto_calculate = self.config.dikt.get("auto_calculate", True)
        return self

    def initView(self) -> None:
        """"""
        cfg = {"text": self.config.dikt.get("text", ""), "size": self.config.dikt.get("size", 10)}
        self.setText(str(cfg.get("text", "")))
        return self

    def initWidget(self) -> None:
        """"""
        self.initModel()
        self.initView()
        return self

    def cmd_on_cell_edit(self) -> None:
        logma.info(f"cmd_on_cell_edit invoked")
        return self

    def cmd_on_cell_select(self) -> None:
        logma.info(f"cmd_on_cell_select invoked")
        return self

    def get_cell_address(self) -> None:
        logma.info(f"get_cell_address requested")
        return None

    def hide(self) -> None:
        """"""
        if self.label is not None:
            self.layout.removeWidget(self.label)
        return self

    def mousePressEvent(self, event: pyqt.QMouseEvent) -> None:
        """
        Override mousePressEvent to toggle the background color on click.
        """
        self.toggle_cell()

    def set_content_format(self, text) -> None:
        logma.info(f"set_content_format called")
        return self

    def toggle_cell(self) -> None:
        """
        Toggle the cell's background color between active and default.
        """
        self.is_active = not self.is_active
        color = self.active_color if self.is_active else self.default_color
        self.setStyleSheet(f"""
            background-color: {color};
            border: 1px solid black;
            min-width: 40px;
            min-height: 40px;
        """)

    def toggle_border(self) -> None:
        """"""
        self.is_active = not self.is_active
        color = self.active_color if self.is_active else self.default_color
        self.setStyleSheet(f"""
            background-color: {color};
            border: 1px solid white;
            min-width: 40px;
            min-height: 40px;
        """)


class NchantdTableCell(NchantdWidgetMixin, pyqt.QTableWidgetItem):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__()
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdCell")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.auto_calculate = None
        self.label = None
        self.formula = None
        self.is_formula = False
        self.is_active = False
        default_color = "transparent"
        active_color = "#191cc2"
        self.row = self.config.dikt.get("row", None)
        self.column = self.config.dikt.get("column", None)
        self.default_color = default_color
        self.active_color = active_color
        self.is_active = False
        logma.info(f"NchantdTableCell initialized")

    def initModel(self) -> None:
        """"""
        super().initModel()
        self.auto_calculate = self.config.dikt.get("auto_calculate", True)
        return self

    def initView(self) -> None:
        """"""
        cfg = {"text": self.config.dikt.get("text", ""), "size": self.config.dikt.get("size", 10)}
        self.setText(str(cfg.get("text", "")))
        return self

    def initWidget(self) -> None:
        """"""
        self.initModel()
        self.initView()
        return self

    def cmd_on_cell_edit(self) -> None:
        logma.info(f"cmd_on_cell_edit invoked")
        return self

    def cmd_on_cell_select(self) -> None:
        logma.info(f"cmd_on_cell_select invoked")
        return self

    def get_cell_address(self) -> None:
        logma.info(f"get_cell_address requested")
        return None

    def hide(self) -> None:
        """"""
        if self.label is not None:
            self.layout.removeWidget(self.label)
        return self

    def mousePressEvent(self, event: pyqt.QMouseEvent) -> None:
        """
        Override mousePressEvent to toggle the background color on click.
        """
        self.toggle_cell()

    def set_content_format(self, text) -> None:
        logma.info(f"set_content_format called")
        return self

    def toggle_cell(self) -> None:
        """
        Toggle the cell's background color between active and default.
        """
        self.is_active = not self.is_active
        color = self.active_color if self.is_active else self.default_color
        self.setStyleSheet(f"""
            background-color: {color};
            border: 1px solid black;
            min-width: 40px;
            min-height: 40px;
        """)

    def toggle_border(self) -> None:
        """"""
        self.is_active = not self.is_active
        color = self.active_color if self.is_active else self.default_color
        self.setStyleSheet(f"""
            background-color: {color};
            border: 1px solid white;
            min-width: 40px;
            min-height: 40px;
        """)
