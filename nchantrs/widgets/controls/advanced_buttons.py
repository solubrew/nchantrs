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
import datetime as dt
from typing import Any, Dict, Optional
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.controls.checkboxes import NchantdCheckbox
from nchantrs.widgets.media.editors.editors import NchantdEntryBox
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from nchantrs.widgets.controls.buttons import NchantdButton
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
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
pxcfg = join(here, '_data_', 'advanced_buttons.yaml')

class NchantdNumberWheelButton(NchantdWidget):
    valueChanged = pyqt.Signal(int)

    def __init__(self, parent: Optional[Any]=None, cfg: Optional[Dict]=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdNumberWheelButton').override(cfg))
        self.value: int = DEFAULT_INITIAL_VALUE
        self.minimum: int = DEFAULT_MINIMUM
        self.maximum: int = DEFAULT_MAXIMUM
        self.step: int = DEFAULT_STEP
        self.up_button: Optional[Any] = None
        self.down_button: Optional[Any] = None
        self.number_display: Optional[Any] = None
        self.label: Optional[Any] = None
        logma.info(f'NchantdNumberWheelButton initialized')

    def initModel(self) -> 'NchantdNumberWheelButton':
        """"""
        super().initModel()
        self.value = self.config.dikt.get('initial_value', DEFAULT_INITIAL_VALUE) or 0
        self.minimum = self.config.dikt.get('minimum', DEFAULT_MINIMUM) or 0
        self.maximum = self.config.dikt.get('maximum', DEFAULT_MAXIMUM) or 0
        self.step = self.config.dikt.get('step', DEFAULT_STEP) or 0
        self.valueChanged.emit(self.value)
        return self

    def initView(self) -> 'NchantdNumberWheelButton':
        """"""
        super().initView()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(SPACING_DEFAULT)
        cfg = {'label': self.config.dikt.get('label', '')}
        self.label = NchantdLabel(self, cfg).initWidget()
        self.layout.addWidget(self.label)
        self.layout.setAlignment(self.label, pyqt.Qt.AlignCenter)
        layout = pyqt.QHBoxLayout()
        self.up_button = pyqt.QPushButton('▲')
        self.up_button.setFixedSize(BUTTON_SIZE_SMALL, BUTTON_SIZE_SMALL)
        self.up_button.clicked.connect(self.increment_value)
        layout.addWidget(self.up_button, alignment=pyqt.Qt.AlignCenter)
        cfg = {'label': str(self.value)}
        self.number_display = NchantdEntryBox(self, cfg).initWidget()
        self.number_display.setAlignment(pyqt.Qt.AlignCenter)
        self.number_display.setFixedSize(DISPLAY_SIZE, DISPLAY_SIZE)
        layout.addWidget(self.number_display, alignment=pyqt.Qt.AlignCenter)
        self.down_button = pyqt.QPushButton('▼')
        self.down_button.setFixedSize(BUTTON_SIZE_MEDIUM, BUTTON_SIZE_SMALL)
        self.down_button.clicked.connect(self.decrement_value)
        layout.addWidget(self.down_button, alignment=pyqt.Qt.AlignCenter)
        self.layout.addLayout(layout)
        self.update_display()
        return self

    def initWidget(self) -> 'NchantdNumberWheelButton':
        """"""
        self.initModel()
        self.initView()
        return self

    def increment_value(self) -> None:
        if self.value + self.step <= self.maximum:
            self.value += self.step
            self.update_display()

    def decrement_value(self) -> None:
        if self.value - self.step >= self.minimum:
            self.value -= self.step
            self.update_display()

    def update_display(self) -> None:
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

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdLinkIcon')).override(cfg)

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
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initView {{type(self).__name__}}')
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdEnableSpinBox(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdEnableSpinBox').override(cfg))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        if cfg is None:
            cfg = {}
        cfg['layout'] = 'horizontal'
        super().initView(cfg)
        cfg = {'text': self.config.dikt.get('label', ''), 'font': {'size': 8}}
        self.checkbox = NchantdCheckbox(self, cfg).initWidget()
        self.layout.addWidget(self.checkbox)
        self.layout.setSpacing(3)
        cfg = {}
        self.spinbox = NchantdSpinBox(self, cfg).initWidget()
        self.layout.addWidget(self.spinbox)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdEnableSequencer(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdEnableSequencer').override(cfg))
        logma.info(f'NchantdEnableSequencer initialized')

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        self.sequence = {i: None for i in range(len(self.config.dikt.get('items', [])))}
        self.items = {}
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        for i, item in enumerate(self.config.dikt.get('items', [])):
            item['value'] = i
            self.items[i] = NchantdEnableSpinBox(self, item).initWidget()
            self.layout.addWidget(self.items[i])
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def on_spin_box_change(self, signal=None, *args, **kwargs) -> None:
        """"""
        for i, widget in self.items:
            new_value = self.sequence[i]
            if new_value is None:
                continue
            if new_value != widget.value():
                widget.setValue(new_value)
        self.sequence[widget] = new_value

class NchantdSpinBox(NchantdWidgetMixin, pyqt.QSpinBox):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent)
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdSpinBox').override(parent.config).override(cfg)
        self.init_variables()

    def initModel(self) -> Any:
        """"""
        super().initModel()
        self.setRange(int(self.config.get('min_value', 0) or 0), int(self.config.get('max_value', 100) or 0))
        self.setSingleStep(int(self.config.get('step', 1) or 0))
        self.setValue(int(self.config.get('value', 0) or 0))
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdActivateSpinBox(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdActivateSpinBox').override(cfg))

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        if cfg is None:
            cfg = {}
        cfg['layout'] = 'horizontal'
        cfg['size'] = None
        super().initView(cfg)
        cfg = {'text': self.config.dikt.get('label', ''), 'action': self.config.dikt.get('action', None)}
        self.button = NchantdButton(self, cfg).initWidget()
        self.layout.addWidget(self.button)
        range_ = self.config.dikt.get('range', [0, 100])
        cfg = {'range': range_, 'value': 0, 'font': {'size': 8}}
        self.spinbox = NchantdSpinBox(self, cfg).initWidget()
        self.layout.addWidget(self.spinbox)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdLabeledSpinBox(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdLabeledSpinBox').override(cfg))

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        self.has_lock = self.config.get('has_lock', False)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        if cfg is None:
            cfg = {}
        cfg['layout'] = 'horizontal'
        cfg['size'] = None
        super().initView(cfg)
        cfg = {'text': self.config.get('label', '')}
        label = NchantdLabel(self, cfg).initWidget()
        self.layout.addWidget(label)
        range_ = self.config.dikt.get('range', [0, 100])
        cfg = {'range': range_, 'value': self.config.get('value', 0), 'font': {'size': 8}}
        self.spinbox = NchantdSpinBox(self, cfg).initWidget()
        self.layout.addWidget(self.spinbox)
        if self.has_lock:
            self.lock_button = NchantdButton(self, cfg={'text': 'Lock'}).initWidget()
            self.layout.addWidget(self.lock_button)
        self.layout.addStretch(0)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdLabeledDoubleSpinBox(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdLabeledDoubleSpinBox').override(cfg))

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        if cfg is None:
            cfg = {}
        cfg['layout'] = 'horizontal'
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

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdColorSelectButton(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdColorSelectButton').override(cfg))
        self.color = None
        self.button = None
        self.color_sample = None

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        self.color = self.config.dikt.get('color', '#000000')
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        cfg = {}
        self.button = NchantdButton(self, cfg).initWidget()
        self.layout.addWidget(self.button)
        cfg = {'color': self.color}
        self.color_sample = NchantdLabel(self, cfg).initWidget()
        self.layout.addWidget(self.color_sample)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self