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

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.controls.checkboxes import NchantdCheckbox
from nchantrs.widgets.media.editors.editors import NchantdEntryBox
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from nchantrs.widgets.controls.buttons import NchantdButton

# ====================================================================================================================||
here = join(dirname(__file__), "")
log = True
logma = Logma(__name__)


# ====================================================================================================================||
# Constants to avoid magic numbers
DEFAULT_INITIAL_VALUE: int = 16
DEFAULT_MINIMUM: int = 0
DEFAULT_MAXIMUM: int = 100
DEFAULT_STEP: int = 1
BUTTON_SIZE_SMALL: int = 30
BUTTON_SIZE_MEDIUM: int = 40
DISPLAY_SIZE: int = 30
SPACING_DEFAULT: int = 5
SPINBOX_LAYOUT_SPACING: int = 3
FONT_SIZE_SMALL: int = 8


# ====================================================================================================================||
pxcfg = join(here, "_data_", "advanced_buttons.yaml")


class NchantdNumberWheelButton(NchantdWidget):
    # Signal to emit the current value whenever it changes
    valueChanged = pyqt.Signal(int)

    def __init__(self, parent: Optional[Any] = None, cfg: Optional[Dict] = None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdNumberWheelButton")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.value: int = DEFAULT_INITIAL_VALUE
        self.minimum: int = DEFAULT_MINIMUM
        self.maximum: int = DEFAULT_MAXIMUM
        self.step: int = DEFAULT_STEP
        self.up_button: Optional[Any] = None
        self.down_button: Optional[Any] = None
        self.number_display: Optional[Any] = None
        self.label: Optional[Any] = None

    def initModel(self) -> "NchantdNumberWheelButton":
        """"""
        super().initModel()
        self.value = self.config.dikt.get("initial_value", DEFAULT_INITIAL_VALUE)
        self.minimum = self.config.dikt.get("minimum", DEFAULT_MINIMUM)
        self.maximum = self.config.dikt.get("maximum", DEFAULT_MAXIMUM)
        self.step = self.config.dikt.get("step", DEFAULT_STEP)
        self.valueChanged.emit(self.value)
        return self

    def initView(self) -> "NchantdNumberWheelButton":
        """"""
        super().initView()
        # Vertical layout for Up Button, Display, Down Button
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(SPACING_DEFAULT)

        cfg = {"label": self.config.dikt.get("label", "")}
        self.label = NchantdLabel(self, cfg).initWidget()
        self.layout.addWidget(self.label)
        self.layout.setAlignment(self.label, pyqt.Qt.AlignCenter)
        layout = pyqt.QHBoxLayout()
        # Up button
        self.up_button = pyqt.QPushButton("▲")
        self.up_button.setFixedSize(BUTTON_SIZE_SMALL, BUTTON_SIZE_SMALL)
        self.up_button.clicked.connect(self.increment_value)
        layout.addWidget(self.up_button, alignment=pyqt.Qt.AlignCenter)

        # Display label
        cfg = {"label": str(self.value)}
        self.number_display = NchantdEntryBox(self, cfg).initWidget()
        self.number_display.setAlignment(pyqt.Qt.AlignCenter)
        self.number_display.setFixedSize(DISPLAY_SIZE, DISPLAY_SIZE)
        layout.addWidget(self.number_display, alignment=pyqt.Qt.AlignCenter)

        # Down button
        self.down_button = pyqt.QPushButton("▼")
        self.down_button.setFixedSize(BUTTON_SIZE_MEDIUM, BUTTON_SIZE_SMALL)
        self.down_button.clicked.connect(self.decrement_value)
        layout.addWidget(self.down_button, alignment=pyqt.Qt.AlignCenter)
        self.layout.addLayout(layout)
        self.update_display()
        return self

    def initWidget(self) -> "NchantdNumberWheelButton":
        """"""
        self.initModel()
        self.initView()
        return self

    def increment_value(self) -> None:
        # Increment the value while respecting the maximum
        if self.value + self.step <= self.maximum:
            self.value += self.step
            self.update_display()

    def decrement_value(self) -> None:
        # Decrement the value while respecting the minimum
        if self.value - self.step >= self.minimum:
            self.value -= self.step
            self.update_display()

    def update_display(self) -> None:
        # Update the label to display the current value
        self.number_display.setText(str(self.value))
        self.valueChanged.emit(self.value)

    def set_value(self, value: int) -> None:
        """
        Set the current value explicitly (e.g., from external code).
        """
        if self.minimum <= value <= self.maximum:
            self.value = value
            self.update_label()

    def set_range(self, minimum: int, maximum: int) -> None:
        """
        Set the range of the number wheel (minimum and maximum values).
        """
        self.minimum = minimum
        self.maximum = maximum

    def set_step(self, step: int) -> None:
        """
        Set the step size for the number wheel.
        """
        self.step = step


class NchantdShareButton(NchantdWidgetMixin, pyqt.QPushButton):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdLinkIcon")).override(cfg)

    def initModel(self):
        """"""
        return self

    def initView(self):
        """"""
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdEnableSpinBox(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent)
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdSpinBox")
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
        cfg = {"text": self.config.dikt.get("label", ""), "font": {"size": 8}}
        self.checkbox = NchantdCheckbox(self, cfg).initWidget()
        self.layout.addWidget(self.checkbox)
        self.layout.setSpacing(3)
        cfg = {}
        self.spinbox = NchantdSpinBox(self, cfg).initWidget()
        self.layout.addWidget(self.spinbox)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdEnableSequencer(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdEnableSequencer"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        self.sequence = {i: None for i in range(len(self.config.dikt.get("items", [])))}
        self.items = {}
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        for i, item in enumerate(self.config.dikt.get("items", [])):
            item["value"] = i
            self.items[i] = NchantdEnableSpinBox(self, item).initWidget()
            self.layout.addWidget(self.items[i])
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def on_spin_box_change(self, signal=None, *args, **kwargs):
        """"""
        # update each page below that is set to enabled
        for i, widget in self.items:
            new_value = self.sequence[i]
            if new_value is None:
                continue
            if new_value != widget.value():
                widget.setValue(new_value)
        self.sequence[widget] = new_value


class NchantdSpinBox(NchantdWidgetMixin, pyqt.QSpinBox):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent)
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdSpinBox").override(parent.config).override(cfg)
        self.init_variables()

    def initModel(self):
        """"""
        super().initModel()
        self.setRange(self.config.get("min_value", 0), self.config.get("max_value", 100))  # Set the range for the spin box
        self.setSingleStep(self.config.get("step", 1))
        self.setValue(self.config.get("value", 0))
        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    # def validate(self, text, pos):
    # 	 """Override the validate method to ensure only even numbers are valid."""
    # 	 if text.isdigit() and int(text) % 2 == 0:
    # 		 return pyqt.QSpinBox.Acceptable, text, pos
    # 	 return pyqt.QSpinBox.Intermediate, text, pos
    #
    # def valueFromText(self, text):
    # 	 """Convert input text to an integer."""
    # 	 return int(text)
    #
    # def textFromValue(self, value):
    # 	 """Convert the value into a string."""
    # 	 return str(value)


class NchantdActivateSpinBox(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdLabeledSpinBox"))
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
        cfg["size"] = None
        super().initView(cfg)
        cfg = {"text": self.config.dikt.get("label", ""), "action": self.config.dikt.get("action", None)}
        self.button = NchantdButton(self, cfg).initWidget()
        self.layout.addWidget(self.button)
        # self.layout.addStretch(0)
        range_ = self.config.dikt.get("range", [0, 100])
        cfg = {"range": range_, "value": 0, "font": {"size": 8}}
        self.spinbox = NchantdSpinBox(self, cfg).initWidget()
        self.layout.addWidget(self.spinbox)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdLabeledSpinBox(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdLabeledSpinBox").override(cfg))

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        self.has_lock = self.config.get("has_lock", False)
        return self

    def initView(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {}
        cfg["layout"] = "horizontal"
        cfg["size"] = None
        super().initView(cfg)
        cfg = {"text": self.config.get("label", "")}
        label = NchantdLabel(self, cfg).initWidget()
        self.layout.addWidget(label)
        # self.layout.addStretch(0)
        range_ = self.config.dikt.get("range", [0, 100])
        cfg = {"range": range_, "value": self.config.get("value", 0), "font": {"size": 8}}
        self.spinbox = NchantdSpinBox(self, cfg).initWidget()
        self.layout.addWidget(self.spinbox)
        if self.has_lock:
            self.lock_button = NchantdButton(self, cfg={"text": "Lock"}).initWidget()
            self.layout.addWidget(self.lock_button)
        self.layout.addStretch(0)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdLabeledDoubleSpinBox(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(self)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdLabeledDoubleSpinBox"))
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
        self.label = NchantdLabel(self, cfg).initWidget()
        self.layout.addWidget(self.label)
        cfg = {}
        self.left_spinbox = NchantdSpinBox(self, cfg).initWidget()
        self.layout.addWidget(self.left_spinbox)
        cfg = {}
        self.right_spinbox = NchantdSpinBox(self, cfg).initWidget()
        self.layout.addWidget(self.right_spinbox)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdColorSelectButton(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(self)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdSelectButton"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.color = None
        self.button = None
        self.color_sample = None

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        self.color = self.config.dikt.get("color", "#000000")
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        cfg = {}
        self.button = NchantdButton(self, cfg).initWidget()
        self.layout.addWidget(self.button)
        cfg = {"color": self.color}
        self.color_sample = NchantdLabel(self, cfg).initWidget()
        self.layout.addWidget(self.color_sample)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
