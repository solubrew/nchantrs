# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""  #																			||
---  #																			||
<(META)>:  #																	||
    docid:   #																	||
    name:	#																	||
    description: >  #															||
        Extendes the basic_js Item widget into the Nchantd Framework for cells
        with in a table...this will need to account for both data and metadata
        for the cell
    expirary: <[expiration]>  #													||
    version: <[version]>  #														||
    path: <[LEXIvrs]>  #														||
    outline: <[outline]>  #														||
    authority: document|this  #													||
    security: sec|lvl2  #														||
    <(WT)>: -32  #																||
"""  # ||
# -*- coding: utf-8 -*-#														||
# ================================Core Modules===================================||
from os.path import abspath, dirname, join

# ===============================================================================||

# ===============================================================================||
from condor import condor
from ogma.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.widgets import NchantdWidgetMixin
from pyffice.items.cells import PyfficeCell
from pyffice.workflows.formulas import PyfficeFormula

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ===============================================================================||
pxcfg = join(here, "_data_", "cells.yaml")
pxcfg = {}


class NchantdCell(NchantdWidgetMixin, pyqt.QWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__()
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdCell")
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
        self.document = None
        self.active_color = active_color
        self.is_active = False

    def initModel(self):
        """"""
        super().initModel()
        self.auto_calculate = self.config.dikt.get("auto_calculate", True)
        logma.info(f"Pyffice Cell Init:")
        cfg = {}
        self.document = PyfficeCell(cfg)
        return self

    def initView(self):
        """"""
        cfg = {"text": self.config.dikt.get("text", ""), "size": self.config.dikt.get("size", 10)}
        # self.setText(str(cfg.get("text", "")))
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def calculate_formula(self, text):
        """"""
        cfg = {"text": text}
        self.formula = PyfficeFormula(cfg)

        return self

    def cmd_on_cell_edit(self):
        """"""
        return self

    def cmd_on_cell_select(self):
        """"""
        return self

    def get_cell_address(self):
        """"""
        return self

    def hide(self):
        """"""
        if self.label is not None:
            self.layout.removeWidget(self.label)
        return self

    def mousePressEvent(self, event: pyqt.QMouseEvent):
        """
        Override mousePressEvent to toggle the background color on click.
        """
        self.toggle_cell()

    def parse_cell(self):
        """"""
        if "=" == self.text[0]:
            self.is_formula = True
            if self.auto_calculate:
                text = self.text[1:]
                self.text = self.calculate_formula(text)
        else:
            self.is_formula = False
        self.text = self.set_content_format(self.text)
        return self

    def set_content_format(self, text):
        """"""

    def toggle_cell(self):
        """
        Toggle the cell's background color between active and default.
        """
        self.is_active = not self.is_active
        color = self.active_color if self.is_active else self.default_color
        self.setStyleSheet(
            f"""
            background-color: {color};
            border: 1px solid black;
            min-width: 40px;
            min-height: 40px;
        """
        )

    def toggle_border(self):
        """"""
        self.is_active = not self.is_active
        color = self.active_color if self.is_active else self.default_color
        self.setStyleSheet(
            f"""
            background-color: {color};
            border: 1px solid white;
            min-width: 40px;
            min-height: 40px;
        """
        )


class NchantdTableCell(NchantdWidgetMixin, pyqt.QTableWidgetItem):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__()
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdCell")
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

    def initModel(self):
        """"""
        super().initModel()
        self.auto_calculate = self.config.dikt.get("auto_calculate", True)
        logma.info(f"Pyffice Cell Init:")
        cfg = {}
        self.document = PyfficeCell(cfg)
        return self

    def initView(self):
        """"""
        cfg = {"text": self.config.dikt.get("text", ""), "size": self.config.dikt.get("size", 10)}
        self.setText(str(cfg.get("text", "")))
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def calculate_formula(self, text):
        """"""
        cfg = {"text": text}
        self.formula = PyfficeFormula(cfg)

        return self

    def cmd_on_cell_edit(self):
        """"""
        return self

    def cmd_on_cell_select(self):
        """"""
        return self

    def get_cell_address(self):
        """"""
        return self

    def hide(self):
        """"""
        if self.label is not None:
            self.layout.removeWidget(self.label)
        return self

    def mousePressEvent(self, event: pyqt.QMouseEvent):
        """
        Override mousePressEvent to toggle the background color on click.
        """
        self.toggle_cell()

    def parse_cell(self):
        """"""
        if "=" == self.text[0]:
            self.is_formula = True
            if self.auto_calculate:
                text = self.text[1:]
                self.text = self.calculate_formula(text)
        else:
            self.is_formula = False
        self.text = self.set_content_format(self.text)
        return self

    def set_content_format(self, text):
        """"""

    def toggle_cell(self):
        """
        Toggle the cell's background color between active and default.
        """
        self.is_active = not self.is_active
        color = self.active_color if self.is_active else self.default_color
        self.setStyleSheet(
            f"""
            background-color: {color};
            border: 1px solid black;
            min-width: 40px;
            min-height: 40px;
        """
        )

    def toggle_border(self):
        """"""
        self.is_active = not self.is_active
        color = self.active_color if self.is_active else self.default_color
        self.setStyleSheet(
            f"""
            background-color: {color};
            border: 1px solid white;
            min-width: 40px;
            min-height: 40px;
        """
        )
