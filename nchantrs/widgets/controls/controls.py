# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
from typing import Any

"""#																			||
---  #																			||
<(META)>:  #																	||
    docid:   #																	||
    name:   #																	||
    description: >  #															||
          #			||
    expirary: <[expiration]>  #													||
    version: <[version]>  #														||
    path: <[LEXIvrs]>  #														||
    outline: <[outline]>  #														||
    authority: document|this  #													||
    security: sec|lvl2  #														||
    <(WT)>: -32  #																||
"""  # ||

# -*- coding: utf-8 -*-#														||
# ===============================Core Modules====================================||
from os.path import abspath, dirname, join

# ===============================================================================||
from kahndor import kahndor

import logging
from nchantrs.libraries import pyqt

logger = logging.getLogger(__name__)
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.groups import NchantdVScrollGroupBox
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from kahndor.logma import Logma

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
logma.off()
log = False

# ===============================================================================||
pxcfg = join(abspath(here), "_data_", "controls.yaml")


class NchantdIncrementbox(NchantdWidgetMixin, pyqt.QSpinBox):
    """ """

    def __init__(self, parent=None, cfg=None) -> None:
        """https://www.tutorialspoint.com/pyqt/pyqt_qspinbox_self.htm"""
        super().__init__(cfg["name"])
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdIncrementbox").override(cfg))
        self.setMinimum(cfg["min"])
        self.setMaximum(cfg["max"])
        self.setRange(cfg["range"])
        self.setValue(cfg["default_value"])
        #self.valueChanged.connect(getattr(app, cfg["handlers"]["value_changed_handler"]))
        self.init_variables()


class NchantdSelectionWidget(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdSelectionWidget").override(cfg))
        self.checkable_button = None
        self.label = None
        self.description = None

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        cfg = {}
        self.checkable_button = NchantdButton(self, cfg).initWidget()
        self.layout.addWidget(self.checkable_button)
        cfg = {}
        self.label = NchantdLabel(self, cfg).initWidget()
        self.layout.addWidget(self.label)
        cfg = {}
        self.description = NchantdLabel(self, cfg).initWidget()
        self.layout.addWidget(self.description)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdWidgetSelector(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdWidgetSelector").override(cfg))
        self.widgets = {}
        logma.info(f"NchantdWidgetSelector initialized")


    def initModel(self) -> Any:
        """"""
        super().initModel()
        [self.add_widget(sequence, widget) for sequence, widget in self.config.dikt.get("selector", {}).items()]
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        group = NchantdVScrollGroupBox()
        for sequence, widget in dict(sorted(self.widgets.items())):
            group.addWidget(widget.initWidget())
        self.layout.addLayout(group.layout)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def add_widget(self, sequence, widget) -> Any:
        """"""
        self.widgets[sequence] = widget
        return self


# ===========================Code Source Examples================================||
"""
"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
