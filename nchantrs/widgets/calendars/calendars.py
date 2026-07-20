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

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from nchantrs.widgets.panes.calendars import NchantdCalendarDetailPane
from kahndor.logma import Logma
from nchantrs.widgets.calendars.hours import NchantdMinuteCalendar, NchantdHourCalendar, NchantdQuarterHourCalendar
from nchantrs.widgets.calendars.days import NchantdDayCalendar
from nchantrs.widgets.calendars.decades import NchantdDecadeCalendar
from nchantrs.widgets.calendars.months import NchantdMonthCalendar, NchantdQuarterYearCalendar
from nchantrs.widgets.calendars.weeks import NchantdWeekCalendar
from nchantrs.widgets.calendars.years import NchantdYearCalendar

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "calendars.yaml")


class NchantdCalendar(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdCalendar").override(cfg))
        self.button_bar = None
        self.detail_pane = None
        self.scope = None
        self.calendar = None

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        self.scope = self.config.dikt.get("scope", "week").lower().replace(" ", "_").replace("-", "_")
        cfg = {"size": ["auto", "auto"], "scope": self.scope}
        match self.scope:
            case "minutely":
                cfg = {}
                self.calendar = NchantdMinuteCalendar(self, cfg).initWidget()
            case "quarter_hourly":
                cfg = {}
                self.calendar = NchantdQuarterHourCalendar(self, cfg).initWidget()
            case "hourly":
                cfg = {}
                self.calendar = NchantdHourCalendar(self, cfg).initWidget()
            case "daily":
                cfg = {}
                self.calendar = NchantdDayCalendar(self, cfg).initWidget()
            case "weekly":
                cfg = {}
                self.calendar = NchantdWeekCalendar(self, cfg).initWidget()
            case "week":
                cfg = {}
                self.calendar = NchantdWeekCalendar(self, cfg).initWidget()
            case "monthly":
                cfg = {}
                self.calendar = NchantdMonthCalendar(self, cfg).initWidget()
            case "quarter_yearly":
                cfg = {}
                self.calendar = NchantdQuarterYearCalendar(self, cfg).initWidget()
            case "yearly":
                cfg = {}
                self.calendar = NchantdYearCalendar(self, cfg).initWidget()
            case "decadely":
                cfg = {}
                self.calendar = NchantdDecadeCalendar(self, cfg).initWidget()
            case _:
                raise Exception(f"Unknown Calendar Scope {self.scope}")
        self.layout.addWidget(self.calendar)
        cfg = {"size": ["auto", 200]}
        self.detail_pane = NchantdCalendarDetailPane(self, cfg).initWidget()
        self.detail_pane.setSizePolicy(pyqt.QSizePolicy.Policy.Expanding, pyqt.QSizePolicy.Policy.Expanding)
        self.layout.addWidget(self.detail_pane, stretch=1)
        self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdDateTimeSelect(NchantdWidgetMixin, pyqt.QDateTimeEdit):
    """"""

    def __init__(self, parent, cfg=None, *args, **kwargs):
        """"""
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).override(cfg)
        super().__init__(*args, **kwargs)

    def initModel(self, objects=None, get_actions=True):
        """"""

    def initView(self):
        """"""

    def initWidget(self, handler=None):
        """

        :param handler:
        :return:
        """
        self.handler = handler
        return self


class NchantdDateTimeGroup(NchantdWidget):
    """"""

    def __init__(self, parent, cfg=None):
        """"""
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdAdvancedCalculator").override(cfg))

    def initView(self):
        """"""
        layout = pyqt.QVBoxLayout()
        gb = pyqt.QGroupBox()
        gb.setMinimumSize(150, 130)
        gb.setMaximumSize(625, 500)
        if "size" in self.config.dikt.keys():
            if self.config.dikt["size"]["width"]:
                gb.setFixedWidth(int(self.config.dikt["size"]["width"] * 1.1))
            if self.config.dikt["size"]["height"]:
                gb.setFixedHeight(int(self.config.dikt["size"]["height"] * 1.35))
        gb.setTitle(self.config.dikt["text"])
        annotate_layout = pyqt.QVBoxLayout()
        time_select = NchantdTimeSelect(self).initWidget()
        annotate_layout.addWidget(time_select)
        date_select = NchantdDateSelect(self).initWidget()
        annotate_layout.addWidget(date_select)
        annotate_layout.setAlignment(self._set_alignment(self.config.dikt["justify"]))
        gb.setLayout(annotate_layout)
        layout.addWidget(gb)
        layout.setAlignment(self._set_alignment(self.config.dikt["justify"]))
        self.setLayout(layout)
        return self

    def initWidget(self, handler=None):
        """

        :param handler:
        :return:
        """
        self.handler = handler
        self.initView()
        return self


class NchantdDateSelect(NchantdWidgetMixin, pyqt.QCalendarWidget):
    """"""

    def __init__(self, parent, cfg=None, *args, **kwargs):
        """"""
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg)
        if self.parent:
            self.config.override(self.parent.config)
        super().__init__(*args, **kwargs)
        self.config.override(cfg)

    def initView(self):
        """"""
        self.set_size()
        # self.setMinimumSize(100, 100)
        # self.setMaximumSize(500, 400)
        return self

    def initWidget(self, handler=None):
        """

        :param handler:
        :return:
        """
        self.initView()
        self.handler = handler
        self.selectionChanged.connect(self.on_date_selected)
        return self

    def on_date_selected(self):
        """"""
        date = self.selectedDate()
        self.handler("date", date)
        return self


class NchantdDateIterate(NchantdWidgetMixin, pyqt.QDateEdit):
    """"""

    def __init__(self, parent, cfg=None):
        """"""
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).override(cfg)
        super().__init__()
        self.setDate(pyqt.QDate.currentDate())


class NchantdEventsList(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("Nchantd")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self.parent, self.config)
        self.config.override(cfg)

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


class NchantdTimeSelect(NchantdWidgetMixin, pyqt.QTimeEdit):
    """"""

    def __init__(self, parent, cfg=None, *args, **kwargs):
        """"""
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdTimeSelect")
        super().__init__(*args, **kwargs)
        self.config.override(cfg)

    def initWidget(self, handler=None):
        """

        :param handler:
        :return:
        """
        self.handler = handler
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
