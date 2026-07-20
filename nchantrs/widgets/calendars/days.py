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
from os.path import dirname, join
import datetime as dt

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.widgets.annotations import NchantdLabel, NchantdHighLowLabel
from nchantrs.widgets.managers import NchantdManager
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.widgets.tables.tables import NchantdTable
from kahndor.logma import Logma
from nchantrs.widgets.groups import NchantdVScrollGroupBox
from nchantrs.widgets.controls.toolbars import NchantdButtonBar
from nchantrs.widgets.tabsets import NchantdTab

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "days.yaml")


class NchantdDayCalendar(NchantdTab):
    """Nchantd Day Calendar provides a list of items
    completed or to be completed on that day
    """

    def __init__(self, parent=None, cfg=None):
        """"""
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdDayCalendar").override(cfg))
        self.journal_notes = None
        self.days_table = None

    def initModel(self):
        """"""
        super().initModel()
        self.dttm = self.config.dikt.get("datetime", dt.datetime.now())
        # self.journal_notes = self.app.model.get_journal("DAY", self.dttm)
        return self

    def initView(self, cfg=None):
        """ """
        if cfg is None:
            cfg = {}
        cfg["layout"] = "vertical"
        super().initView(cfg)
        layout = pyqt.QHBoxLayout()
        today = dt.datetime.now()
        cfg = {"text": self.config.dikt.get("datetime", None)}
        layout.addWidget(NchantdLabel(self, cfg).initWidget())
        buttons = {0: "add_task", 4: "hide_self"}
        self.button_bar = NchantdButtonBar(self).initWidget(buttons)
        layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignLeft)

        layout.addStretch(1)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)

        self.layout.addLayout(layout)
        labels = ["Due Date", "Action", "Status", "Notes"]
        cfg = {
            "columns": labels,
            "column_widgets": {"Due Date": "datetime", "Status": "buttonbar"},
            "data": [[self.dttm, None, None]],
        }
        # put the buttons inside the preview pane
        # need a buttonbar inside each row in the Disposition column
        # Split, Push, Close, Tag
        logma.info(f"cfg: {cfg}")
        self.days_table = NchantdTable(self, cfg).initWidget()
        self.days_table.setHorizontalHeaderLabels(labels)
        self.days_table.reset_column_widths()
        self.layout.addWidget(self.days_table)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdDayDashboard(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdDayMiniOverview").override(cfg))
        self.name = None  # TODO get tab name

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        day = None
        group = pyqt.QGroupBox()
        layout = pyqt.QVBoxLayout()
        group.setLayout(layout)
        if day is None:
            day = dt.datetime.now()
        cfg = {
            "title": day.strftime("%A %Y-%m-%d"),
            "humidity": {"high": "80", "low": "50"},
            "temperature": {"high": "80", "low": "50"},
            "rain_chance": {"high": "80", "low": "50"},
        }
        day = self.config.dikt.get("day", {self.name: cfg})
        # data = self.app.model.integration.weather.openWeather(day['date'], day['location'])
        # ideally we get temp high low, humidity high low,
        group.setMinimumWidth(200)
        group.setMaximumHeight(100)
        for key, param in day.items():
            if key == "title":
                group.setTitle(param)
            elif key in ("humidity", "temperature", "rain_chance"):
                cfg = {"text": key, "high": param.get("high", ""), "low": param.get("low", "")}
                label = NchantdHighLowLabel(self, cfg).initWidget()
                layout.addWidget(label)
        self.layout.addWidget(group)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdDayJournal(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdDayJournal").override(cfg))
        self.journal_group = None

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        cfg = {"size": ["auto", "auto"]}
        self.journal_group = NchantdVScrollGroupBox(self, cfg)
        self.journal_group.setTitle("Journal Review")
        self.layout.addLayout(self.journal_group.layout)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdDayManager(NchantdManager):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdDayManager").override(cfg))

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        # self.day
        # self.task_adder = NchantdNewTaskPane().initWidget()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdHourDay(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdHourDay").override(cfg))

    def initModel(self):
        """"""
        super().initModel()
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


class NchantdQuarterHourDay(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdQuarterHourDay").override(cfg))

    def initModel(self):
        """"""
        super().initModel()
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


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
