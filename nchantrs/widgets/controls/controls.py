# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""  #																			||
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
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.groups import NchantdVScrollGroupBox
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from ogma.logma import Logma

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
log = False

# ===============================================================================||
pxcfg = join(abspath(here), "_data_", "controls.yaml")


class NchantdIncrementbox(pyqt.QSpinBox):
    """ """

    def __init__(self, app, cfg, parent=None):
        """https://www.tutorialspoint.com/pyqt/pyqt_qspinbox_self.htm"""
        if parent:
            cfg = parent.config
        self.config = condor.Instruct(pxcfg).override(cfg)
        super(NchantdIncrementbox, self).__init__(cfg["name"], parent)
        self.setMinimum(cfg["min"])
        self.setMaximum(cfg["max"])
        self.setRange(cfg["range"])
        self.setValue(cfg["default_value"])
        self.valueChanged.connect(getattr(app, cfg["handlers"]["value_changed_handler"]))


class NchantdSelectionWidget(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("Nchantd")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.checkable_button = None
        self.label = None
        self.description = None

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
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

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdWidgetSelector(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("Nchantd")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.widgets = {}

    def initModel(self):
        """"""
        super().initModel()
        [self.add_widget(sequence, widget) for sequence, widget in self.config.dikt.get("selector", {}).items()]
        return self

    def initView(self):
        """"""
        super().initView()
        group = NchantdVScrollGroupBox()
        for sequence, widget in dict(sorted(self.widgets.items())):
            group.addWidget(widget.initWidget())
        self.layout.addLayout(group.layout)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def add_widget(self, sequence, widget):
        """"""
        self.widgets[sequence] = widget
        return self


# ===========================Code Source Examples================================||
"""
new_cmd =
submit_cmd = "INSERT INTO {table} () VALUES ()"
delete_cmd = "UPDATE {db}.{table} SET DELETE_BIT = 1, MODON_DTTM = '{now}' WHERE {table}_PK = {table_pk}"
next_cmd = "SELECT * FROM {db}.{table} WHERE {table}_PK = {table_pk}" #how to know next by what filter
jump_cmd = "SELECT * FROM {db}.{table} WHERE {table}_PK = {table_pk}"
prev_cmd = "SELECT * FROM {db}.{table} WHERE {table}_PK = {table_pk}"
"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
