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
import math

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")
log = True
logma = Logma(__name__)
logma.off()


# ====================================================================================================================||
# Constants to avoid magic numbers
DEFAULT_FONT_SIZE: int = 10
DEFAULT_MIN_DIMENSION: int = 10
DEFAULT_GRID_COLUMNS: int = 2


# ====================================================================================================================||
pxcfg = join(here, "_data_", "checkboxes.yaml")


class NchantdCheckbox(NchantdWidgetMixin, pyqt.QCheckBox):
    def __init__(self, parent: Any, cfg: Optional[Dict] = None) -> None:
        """https://www.tutorialspoint.com/pyqt/pyqt_qcheckbox_self.htm"""
        super().__init__("", parent)
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdCheckbox")
        if self.parent:
            self.config.override(self.parent.config.dikt)
        self.config.override(cfg)
        self.init_variables()

    def initModel(self) -> "NchantdCheckbox":
        """"""
        super().initModel()
        return self

    def initView(self) -> "NchantdCheckbox":
        """"""
        super().initView()
        self.setText(self.config.dikt.get("text", "Missing Text"))
        self.setChecked(self.config.dikt.get("checked", False))
        if self.config.dikt.get("font", None):
            font = pyqt.QFont()
            font.setPointSize(self.config.dikt["font"].get("size", DEFAULT_FONT_SIZE))
            font.setFamily(self.config.dikt["font"].get("family", "Arial"))
            self.setFont(font)
        self.set_size()
        return self

    def initWidget(self) -> "NchantdCheckbox":
        """"""
        self.initModel()
        self.initView()
        return self

    def set_size(
        self,
        set_width: Optional[int] = None,
        set_height: Optional[int] = None,
        min_width: int = DEFAULT_MIN_DIMENSION,
        min_height: int = DEFAULT_MIN_DIMENSION,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
    ) -> None:
        """"""
        text_width, text_height = self._get_text_size(self.text)
        logma.info(f"Text Size {text_width} {text_height}")
        width = text_width
        height = text_height
        size = self.config.dikt.get("size", None)
        logma.info(f"Size {size}")
        if isinstance(size, list):
            width = size[0]
            height = size[1]
        logma.info(f"Size {width} {height}")
        size_width = None
        size_height = None
        if width != "auto":
            if size is None or len(size) != 2:
                size = [0, 0]
            size_width, size_height = size
            if set_width is None:
                set_width = max(text_width, size_width)
        if height != "auto":
            if size is None or len(size) != 2:
                size = [0, 0]
            size_width, size_height = size
            if set_height is None:
                set_height = max(text_height, size_height)
        logma.info(f"Size {size_width} {size_height}")
        logma.info(f"Text Size {set_width} {set_height}")
        super().set_size(set_width, set_height, min_width, min_height, max_width, max_height)


class NchantdCheckboxGroup(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdCheckboxGroup"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.checks = {}

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView({"layout": "grid"})
        cnt = 0
        checked = False
        col = 0
        row = 0
        max_rows = int(math.ceil(len(self.config.dikt.get("multi_options", [])) / 2))
        if max_rows == 0:
            max_rows = 1
        max_cols = int(math.ceil(len(self.config.dikt.get("multi_options", [])) / max_rows))
        for option in self.config.dikt.get("multi_options", []):
            cfg = {"text": option, "checked": checked}
            self.checks[cnt] = NchantdCheckbox(self, cfg).initWidget()
            self.layout.addWidget(self.checks[cnt], row, col)
            col += 1
            if col % max_cols == 0:
                row += 1
                col = 0
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdCheckboxCombo(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdCheckboxCombo"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {}
        cfg["layout"] = "horizontal"
        super().initView(cfg)
        self.checkbox = NchantdCheckbox(self, cfg).initWidget()
        self.layout.addWidget(self.checkbox)
        cfg = {}
        self.combo = NchantdComboBox(self, cfg).initWidget()
        self.layout.addWidget(self.combo)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
