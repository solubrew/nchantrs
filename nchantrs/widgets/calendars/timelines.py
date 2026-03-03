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

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.widgets.calendars.calendars import NchantdDateSelect
from nchantrs.widgets.calendars.days import NchantdDayCalendar
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.groups import NchantdHScrollGroupBox, NchantdVScrollGroupBox
from nchantrs.widgets.media.editors.selectors import NchantdComboBox, NchantdDropDown
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.widgets.tabsets import NchantdTab
from nchantrs.widgets.media.media import NchantdNEWSLSummary

from nchantrs.widgets.calendars.days import NchantdDayDashboard
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "timelines.yaml")
pxcfg = {}


class NchantdHistory(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdHistory")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.top_layout = None
        self.start_date_selector = None
        self.end_date_selector = None
        self.populate_history = None

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
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

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def run_populate_history(self):
        """"""
        return self

    def update_history_table(self):
        """"""
        return self

    def on_focus(self):
        """"""
        # add a datetime stamp
        self.editor.setText(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return self

    # def check_rotation_time(self):
    #     """Check the set time for rotating the journal"""
    #     if self.running_log:
    #         pass  # TODO check entries by time and rotate out ones older than 24 hours
    #     else:
    #         if self.current_time > self.rotate_time:
    #             self.rotate_journal()
    #
    # def rotate_journal(self):
    #     """"""
    #     self.set_rotate_time(hour=24)
    #
    # def rotate_entry(self):
    #     """"""
    #     self.set_rotate_time(min=30, hour=24)
    #
    # def update_widget(self):
    #     """"""
    #     self.check_rotation_time()
    #
    # def get_journal_notes(self, threshold, datetime=None, rolling=False):
    #     """"""
    #     table = "vw_journal_notes"
    #     data = self.app.model.store.get_table(table)
    #     if threshold == "TODAY":
    #         if rolling:
    #             pass  # need to calculate back 24 hours
    #         datetime = datetime.now()
    #         notes = data[data["file_name_txt"] == f"{datetime.strftime('%Y%m%d')}-journal"]
    #     elif threshold == "YEAR":
    #         notes = data[data["file_name_txt"].str.contains(f"{datetime.strptime('%Y')}*-journal", regex=True)]
    #     elif threshold == "MONTH":
    #         if rolling:
    #             pass  # need to calculate back 1 month
    #         notes = data[data["file_name_txt"].str.contains(f"{datetime.strptime('%Y%m')}*-journal", regex=True)]
    #     elif threshold == "DAY":
    #         notes = data[data["file_name_txt"] == f"{datetime.strptime('%Y%m%d')}-journal"]
    #     return notes
    #
    def store_journal(self):
        """"""
        return self
        today = dt.datetime.now().strftime("%Y%m%d")
        file_name = f"{today}-journal"
        page = 0  # journals always have 1 page for the current day
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
        # payload = {"file_name_txt": file_name}

    # def update_journal(self):
    #     """"""


class NchantdRecentChanges(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdRecentChanges")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.change_group = None

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        self.change_group = NchantdVScrollGroupBox()
        self.change_group.setTitle("Recent Changes")
        self.layout.addLayout(self.change_group.layout)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdTodayOverview(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdTodayOverviewTab"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.tasks = None

    def initModel(self):
        """"""
        super().initModel()
        # self.tasks = self.app.model.store.get_tasks("TODAY")
        return self

    def initView(self):
        """"""
        super().initView()
        logma.info(f"initView")
        scroll = NchantdHScrollGroupBox()
        scroll.setTitle("Daily Weather")
        today = dt.datetime.now()
        days = [today + dt.timedelta(days=x) for x in range(-3, 4)]
        logma.info(f"Days {days}")
        for day in days:
            cfg = {
                "title": day.strftime("%A %Y-%m-%d"),
                "humidity": {"high": "80", "low": "50"},
                "temperature": {"high": "80", "low": "50"},
                "rain_chance": {"high": "80", "low": "50"},
            }
            logma.info(f"Day {day}")
            cfg = {"day": cfg}
            if day.strftime("%Y-%m-%d") == today.strftime("%Y-%m-%d"):
                cfg["font_zoom"] = 1.2  # TODO: make the today mini widget slightly larger in text etc?
            scroll.addWidget(NchantdDayDashboard(self, cfg).initWidget())
            # scrollbar = scroll.scroll.horizontalScrollBar()
            # scrollbar = scroll.scroll.horizontalScrollBar()
            # scrollbar.setSliderPosition(int((scrollbar.maximum() + scrollbar.minimum())/2))
        scroll.set_scroll_bar_position("center")
        self.layout.addLayout(scroll.layout)
        logma.info(f"initView END")
        # put in a tabset here
        if self.tasks is None:
            self.tasks = []
        # if len(self.tasks) > 0:

        self.selected_day = NchantdDayCalendar(self, self.config).initWidget()
        if len(self.tasks) == 0:
            self.selected_day.setFixedHeight(75)
        self.layout.addWidget(self.selected_day)

        # have another tab that is most recent comms table
        # instead of a tabset could have the system auto create tasks to read emails for any important emails
        # these would then show in the todo tasks

        layout = pyqt.QHBoxLayout()
        cfg = {"filters": {}}
        # self.news = NchantdNEWSLSummary(self, cfg).initWidget()
        # layout.addWidget(self.news)
        cfg = {"size": ["auto", "auto"]}
        self.viewer = NchantdVScrollGroupBox(self, cfg)
        self.viewer.setTitle("Quick View")
        layout.addLayout(self.viewer.layout)
        self.layout.addLayout(layout)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdTODOCalendar(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("Nchantd")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        self.day_calendar = NchantdDayCalendar().initWidget()
        self.layout.addWidget(self.day_calendar)
        self.task_entry = NchantdTODOEntryPane().initWidget()
        self.layout.addWidget(self.task_entry)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdTimeTrackerForm(NchantdWidget):
    """ """

    def __init__(self, parent=None, cfg={}, panestyle=None):
        """ """
        self.parent = parent
        logma.info("CFG", cfg)
        self.config = condor.Instruct(pxcfg).select("tabsets.NchantdTab")
        self.config.override(cfg)
        if parent:
            self.config.override(parent.config)
        logma.info(f"Config {self.config.dikt}")
        super(NchantdTimeTrackerForm, self).__init__(parent, self.config, panestyle)

    def initModel(self):
        """ """
        logma.info(f"CONFIG {self.config.dikt}")
        # self.name = self.config.dikt['tab']['name']
        # self.data = j.loads(self.config.dikt['tab']['widgdata'])
        return self

    def initView(self):
        """ """
        self.buildPane()
        # self.setText(self.data['text'])
        return self

    def buildPane(self, minutes=5, hour_inc=1, start_tm="08:00", sections=10):
        """ """
        start_tm = time.strptime(start_tm, "%H:%M")
        logma.info(f"Start TM {start_tm} {type(start_tm)}")
        minutes = [str(x) if len(str(x)) == 2 else f"0{x}" for x in range(0, 60, minutes)]
        start_tm = time.strptime("08:00", "%H:%M")
        logma.info(f"Start TM {start_tm} {type(start_tm)}")
        windows, hour = 24 * len(minutes), 8
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
                # if log: print('TODO Action', self.config.dikt)
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

    def onEnterEvent(self):
        """Run a save of the doc editor data to the database"""

    def mousePressEvent(self, event):
        """ """
        editor.mousePressEventLog(event)
        super().mousePressEvent(event)
        return self


class NchantdTimeTrackerFormFast(NchantdWidget):
    """ """

    def __init__(self, parent=None, cfg={}, panestyle=None):
        """ """
        super().__init__(parent, cfg, panestyle)
        self.parent = parent
        logma.info("CFG", cfg)
        self.config.override(condor.Instruct(pxcfg).select("NchantdTimeTrackerFormFast"))
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        logma.info(f"Config {self.config.dikt}")

    def initModel(self):
        """ """
        logma.info(f"CONFIG {self.config.dikt}")
        # self.name = self.config.dikt['tab']['name']
        # self.data = j.loads(self.config.dikt['tab']['widgdata'])
        return self

    def initView(self):
        """ """
        self.buildPane()
        # self.setText(self.data['text'])
        return self

    def addTimeBox(self, hour, minute):
        """"""
        hour = str(hour)
        if len(str(hour)) == 1:
            hour = f"0{hour}"
        l1 = pyqt.QHBoxLayout()
        l1.addWidget(annotations.NchantdLabel().initWidget({"text": f"{hour}:{minute}"}))
        l1.addWidget(editors.NchantdEntryBox(self).initWidget(None))
        return l1

    def calculateTime(self, section, rows, hour_inc):
        """"""

        return tm

    def buildPane(self, minutes=5, hour_inc=1, start_tm="08:00", sections=10):
        """ """
        start_tm = time.strptime(start_tm, "%H:%M")
        logma.info(f"Start TM {start_tm} {type(start_tm)}")
        minutes_ls = [str(x) if len(str(x)) == 2 else f"0{x}" for x in range(0, 60, minutes)]
        start_tm = time.strptime("08:00", "%H:%M")
        logma.info(f"Start TM {start_tm} {type(start_tm)}")
        windows, hour = 24 * len(minutes_ls), 8
        layout = pyqt.QVBoxLayout()
        # Rewrite for each section to build in the same loop
        rows = int(windows / sections)
        logma.info(f"Rows {rows}")
        gb, l0 = {}, {}
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
