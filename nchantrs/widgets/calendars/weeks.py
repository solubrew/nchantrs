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

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.widgets.calendars.days import NchantdDayCalendar
from nchantrs.widgets.widgets import NchantdWidget
from ogma.logma import Logma
from nchantrs.widgets.tabsets import NchantdTab

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "week.yaml")


class NchantdWeekCalendar(NchantdTab):
    """ """

    def __init__(self, parent=None, cfg=None):
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdWeekCalendar"))
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self, cfg=None):
        """ """
        if cfg is None:
            cfg = {}
        cfg["layout"] = "grid"
        super().initView(cfg)
        today = dt.date.today()
        cfg = {"datetime": f"{today.strftime('%A - %B %d, %Y')}"}
        self.layout.addWidget(NchantdDayCalendar(self, cfg).initWidget(), 0, 0, 2, 1)
        today_1 = today + dt.timedelta(days=1)
        cfg = {"datetime": f"{today_1.strftime('%A - %B %d, %Y')}"}
        self.layout.addWidget(NchantdDayCalendar(self, cfg).initWidget(), 2, 0, 1, 1)
        today_2 = today + dt.timedelta(days=2)
        cfg = {"datetime": f"{today_2.strftime('%A - %B %d, %Y')}"}
        self.layout.addWidget(NchantdDayCalendar(self, cfg).initWidget(), 3, 0, 1, 1)
        today_3 = today + dt.timedelta(days=3)
        cfg = {"datetime": f"{today_3.strftime('%A - %B %d, %Y')}"}
        self.layout.addWidget(NchantdDayCalendar(self, cfg).initWidget(), 0, 1, 1, 1)
        today_4 = today + dt.timedelta(days=4)
        cfg = {"datetime": f"{today_4.strftime('%A - %B %d, %Y')}"}
        self.layout.addWidget(NchantdDayCalendar(self, cfg).initWidget(), 1, 1, 1, 1)
        today_5 = today + dt.timedelta(days=5)
        cfg = {"datetime": f"{today_5.strftime('%A - %B %d, %Y')}"}
        self.layout.addWidget(NchantdDayCalendar(self, cfg).initWidget(), 2, 1, 1, 1)
        today_6 = today + dt.timedelta(days=6)
        cfg = {"datetime": f"{today_6.strftime('%A - %B %d, %Y')}"}
        self.layout.addWidget(NchantdDayCalendar(self, cfg).initWidget(), 3, 1, 1, 1)

        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
