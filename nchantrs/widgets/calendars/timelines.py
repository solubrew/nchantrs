#!/usr/bin/env python3
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
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

# ======================================3rd Party Library Modules=====================================================||


# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma

# ====================================================================================================================||
HERE = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
if not log:
    logma.off()
# ====================================================================================================================||
PXCFG = join(HERE, "_data_", ".yaml")


from typing import Any

from os.path import dirname, join
import datetime as dt
import logging
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.widgets.calendars.calendars import NchantdDateSelect
from nchantrs.widgets.calendars.days import NchantdDayCalendar
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.groups import NchantdVScrollGroupBox
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.widgets.tabsets import NchantdTab
from kahndor.logma import Logma

here = join(dirname(__file__), "")
logma = Logma(__name__)
pxcfg = join(here, "_data_", "timelines.yaml")


class NchantdHistory(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdHistory")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.top_layout = None
        self.start_date_selector = None
        self.end_date_selector = None
        self.populate_history = None
        logma.info(f"NchantdHistory initialized")

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """Show an overview of the history within this Nchantd Fapplication"""
        super().initView()
        cfg = {}
        self.top_layout = pyqt.QHBoxLayout()
        self.start_date_selector = NchantdDateSelect(self, cfg).initWidget()
        self.top_layout.addWidget(self.start_date_selector)
        self.end_date_selector = NchantdDateSelect(self, cfg).initWidget()
        self.top_layout.addWidget(self.end_date_selector)
        self.layout.addLayout(self.top_layout)
        cfg = {"handlers": self.run_populate_history}
        self.populate_history = NchantdButton(self, cfg).initWidget()
        self.layout.addWidget(self.populate_history)
        self.layout.addLayout(self.top_layout)
        self.update_history_table()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def run_populate_history(self) -> Any:
        logma.info(f"run_populate_history called")
        return self

    def update_history_table(self) -> Any:
        logma.info(f"update_history_table called")
        return self

    def on_focus(self) -> Any:
        """"""
        self.editor.setText(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return self

    def store_journal(self) -> Any:
        """"""
        return self
        today = dt.datetime.now().strftime("%Y%m%d")
        file_name = f"{today}-journal"
        page = 0
        notes = self.get_journal_notes(file_name)
        if notes is None:
            update = False
            entry = 0
        else:
            entry = len(notes)
        if update is False:
            payload = [
                [
                    uuid(),
                    "journal",
                    file_name,
                    "doc_media|doc_media_content",
                    "internal",
                    "clear|text|utf-8",
                    f"journal|day|entry|{today}",
                    0,
                ]
            ]
        self._store_media(payload, page, entry, content)


class NchantdRecentChanges(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdRecentChanges")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.change_group = None

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.change_group = NchantdVScrollGroupBox()
        self.change_group.setTitle("Recent Changes")
        self.layout.addLayout(self.change_group.layout)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdTodayOverview(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdTodayOverviewTab").override(cfg))
        self.tasks = None

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdTODOCalendar(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("Nchantd")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.day_calendar = NchantdDayCalendar().initWidget()
        self.layout.addWidget(self.day_calendar)
        self.task_entry = NchantdTODOEntryPane().initWidget()
        self.layout.addWidget(self.task_entry)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdTimeTrackerForm(NchantdWidget):
    """ """

    def __init__(self, parent=None, cfg={}, panestyle=None) -> None:
        """ """
        self.parent = parent
        logma.info("CFG", cfg)
        self.config = kahndor.Instruct(pxcfg).select("tabsets.NchantdTab")
        self.config.override(cfg)
        if parent:
            self.config.override(parent.config)
        logma.info(f"Config {self.config.dikt}")
        super(NchantdTimeTrackerForm, self).__init__(parent, self.config, panestyle)

    def initModel(self) -> Any:
        """ """
        logma.info(f"CONFIG {self.config.dikt}")
        return self

    def initView(self) -> Any:
        """ """
        self.buildPane()
        return self

    def buildPane(self, minutes=5, hour_inc=1, start_tm="08:00", sections=10) -> Any:
        """ """
        start_tm = time.strptime(start_tm, "%H:%M")
        logma.info(f"Start TM {start_tm} {type(start_tm)}")
        minutes = [str(x) if len(str(x)) == 2 else f"0{x}" for x in range(0, 60, minutes)]
        start_tm = time.strptime("08:00", "%H:%M")
        logma.info(f"Start TM {start_tm} {type(start_tm)}")
        windows, hour = (24 * len(minutes), 8)
        layout = pyqt.QVBoxLayout()
        l = pyqt.QHBoxLayout()
        for section in range(sections):
            gb = pyqt.QGroupBox()
            logma.info(f"Section {section}")
            l0 = pyqt.QVBoxLayout()
            cnt = 1
            rows = int(windows / sections)
            logma.info(f"Rows {rows}")
            for i in range(0, rows, hour_inc):
                logma.info(f"I {i}")
                thour = str(hour)
                if len(str(hour)) == 1:
                    thour = f"0{hour}"
                j = i % len(minutes)
                logma.info(f"J {j}")
                minute = minutes[j]
                logma.info(f"Minute {minute}")
                l1 = pyqt.QHBoxLayout()
                cfg = {"label": f"{thour}:{minute}", "layout": "horizontal"}
                l1.addWidget(editors.NchantdEntryEditor(self, cfg).initWidget(None))
                l0.addLayout(l1)
                if cnt == len(minutes):
                    hour += hour_inc
                    if hour == 24:
                        hour = 0
                    cnt = 0
                cnt += 1
                gb.setLayout(l0)
            l.addWidget(gb)
        layout.addLayout(l)
        gb = pyqt.QGroupBox("Tasks")
        scroll = pyqt.QScrollArea()
        scroll.setWidgetResizable(True)
        cfg = {"label": "Select Task", "size": [500, 25]}
        l0 = pyqt.QVBoxLayout()
        l0.addWidget(editors.NchantdEntryEditor(self, cfg).initWidget(None))
        gb.setLayout(l0)
        layout.addWidget(gb)
        layout.addWidget(scroll)
        self.setLayout(layout)
        return self

    def onEnterEvent(self) -> None:
        logma.info(f"onEnterEvent called")
        return self

    def mousePressEvent(self, event) -> Any:
        """ """
        editor.mousePressEventLog(event)
        super().mousePressEvent(event)
        return self


class NchantdTimeTrackerFormFast(NchantdWidget):
    """ """

    def __init__(self, parent=None, cfg={}, panestyle=None) -> None:
        """ """
        super().__init__(parent, cfg, panestyle)
        self.parent = parent
        logma.info("CFG", cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdTimeTrackerFormFast"))
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        logma.info(f"Config {self.config.dikt}")

    def initModel(self) -> Any:
        """ """
        logma.info(f"CONFIG {self.config.dikt}")
        return self

    def initView(self) -> Any:
        """ """
        self.buildPane()
        return self

    def addTimeBox(self, hour, minute) -> Any:
        """"""
        hour = str(hour)
        if len(str(hour)) == 1:
            hour = f"0{hour}"
        l1 = pyqt.QHBoxLayout()
        l1.addWidget(annotations.NchantdLabel().initWidget({"text": f"{hour}:{minute}"}))
        l1.addWidget(editors.NchantdEntryBox(self).initWidget(None))
        return l1

    def calculateTime(self, section, rows, hour_inc) -> Any:
        """"""
        return tm

    def buildPane(self, minutes=5, hour_inc=1, start_tm="08:00", sections=10) -> Any:
        """ """
        start_tm = time.strptime(start_tm, "%H:%M")
        logma.info(f"Start TM {start_tm} {type(start_tm)}")
        minutes_ls = [str(x) if len(str(x)) == 2 else f"0{x}" for x in range(0, 60, minutes)]
        start_tm = time.strptime("08:00", "%H:%M")
        logma.info(f"Start TM {start_tm} {type(start_tm)}")
        windows, hour = (24 * len(minutes_ls), 8)
        layout = pyqt.QVBoxLayout()
        rows = int(windows / sections)
        logma.info(f"Rows {rows}")
        gb, l0 = ({}, {})
        for section in range(sections):
            gb[section] = pyqt.QGroupBox()
            l0[section] = pyqt.QVBoxLayout()
        l = pyqt.QHBoxLayout()
        cnt = 1
        for i in range(0, rows, hour_inc):
            section = 0
            l0[section].addLayout(self.addTimeBox(hour, minutes_ls[i % len(minutes_ls)]))
            gb[section].setLayout(l0[section])
            if cnt == len(minutes_ls):
                hour += hour_inc
                if hour == 24:
                    hour = 0
                cnt = 0
            l.addWidget(gb[section])
            cnt += 1
        layout.addLayout(l)
        gb = pyqt.QGroupBox("Tasks")
        scroll = pyqt.QScrollArea()
        scroll.setWidgetResizable(True)
        cfg = {"label": "Select Task", "size": [500, 25]}
        l0 = pyqt.QVBoxLayout()
        l0.addWidget(editors.NchantdEntryEditor(self, cfg).initWidget(None))
        gb.setLayout(l0)
        layout.addWidget(gb)
        layout.addWidget(scroll)
        self.setLayout(layout)
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
