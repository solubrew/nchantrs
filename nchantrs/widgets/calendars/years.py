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
import calendar
from calendar import monthrange

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.groups import NchantdVScrollGroupBox
from nchantrs.widgets.tables.tables import NchantdGrid
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.widgets.tabsets import NchantdTab

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "years.yaml")


class NchantdYearCalendar(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdYearCalendar"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.year_overview_group = None
        self.months = []

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """

        1 to 3 major items that happened each week...in the news events or personal life events.
        a highlight of journal entries for the year

        collect goals and create metrics if available in the document.

        show the current week number
        show weekly weather forecast
        have a yearly items tab launch - have this as a special integration in the + tab or an area of the overview tab?
            - yearly goals
            - yearly metrics
            - yearly summary

        :return:
        """
        super().initView()
        self.layout.setContentsMargins(0, 0, 0, 0)
        layout = pyqt.QGridLayout()
        self.month_tables = {}
        row = 0
        col = 0
        year = dt.date.today().year
        for i in range(1, 13):
            cfg = {"rows": 3, "columnts": 10, "number": monthrange(year, i)[1], "start_one": True}
            self.month_tables[i] = NchantdGrid(self, cfg).initWidget()
            # self.month_tables[i].update_number(monthrange(year, i)[1])
            self.month_tables[i].setTitle(calendar.month_name[i])
            logma.info(f"Row {row} Col {col}")
            layout.addWidget(self.month_tables[i], row, col)
            self.months.append(self.month_tables[i])
            col += 1
            if col == 2:
                col = 0
                row += 1
        self.layout.addLayout(layout)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdYearlyJournal(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdYearlyJournal"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
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
        self.journal_group.setTitle("Yearly Journal Review")
        self.layout.addLayout(self.journal_group.layout)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdYearSummaryTab(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdYearSummaryTab"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

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
