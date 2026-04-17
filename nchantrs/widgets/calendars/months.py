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
import calendar

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||
from calendar import monthrange

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.widgets.groups import NchantdVScrollGroupBox
from nchantrs.widgets.media.editors.selectors import NchantdDropDown
from nchantrs.widgets.tables.tables import NchantdGrid
from nchantrs.widgets.tabsets import NchantdTab
from kahndor.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "month.yaml")


class NchantdMonthCalendar(NchantdTab):
    """The Month Calendar will be a fixed window for a multiweek calendar with fixed end points"""

    def __init__(self, parent=None, cfg=None):
        """"""
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdMonthCalendar"))
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.month_type = None
        self.journal_notes = None

    def initModel(self):
        """"""
        super().initModel()
        datetime = self.config.dikt.get("datetime", dt.datetime.now())
        # self.journal_notes = self.app.model.store.get_journal_notes("MONTH", date=datetime)
        return self

    def initView(self):
        """"""
        super().initView()
        self.month_type = self.config.dikt.get("month_type", "widget")
        self.selectedDate = pyqt.QDate.currentDate()
        self.month_options = []
        for month in range(1, 13):
            self.month_options.append(calendar.month_name[month])
        cfg = {"label": "Date: ", "layout": "horizontal", "combobox": {"options": self.month_options}}
        self.month_select = NchantdDropDown(self, cfg).initWidget()

        self.year_select = pyqt.QDateTimeEdit()
        self.year_select.setDisplayFormat("yyyy")
        self.year_select.setDateRange(pyqt.QDate(1753, 1, 1), pyqt.QDate(8000, 1, 1))

        self.month_select.combobox.setCurrentIndex(self.selectedDate.month() - 1)
        self.year_select.setDate(self.selectedDate)
        # self.layout.addStretch()

        controlsLayout = pyqt.QHBoxLayout()
        self.layout.addLayout(controlsLayout)
        controlsLayout.addWidget(self.month_select)
        controlsLayout.addWidget(self.year_select)
        controlsLayout.addSpacing(24)
        if self.month_type == "text":
            self.fontSizeLabel = pyqt.QLabel("Font size:")
            self.fontSizeSpinBox = pyqt.QSpinBox()
            self.fontSizeSpinBox.setRange(1, 64)
            self.fontSizeSpinBox.setValue(10)
            size = self.get_viewport_size()
            logma.info(f"size: {size}")
            self.fontSize = int(size / 7)
            logma.info(f"self.fontSize: {self.fontSize}")
            self.insertCalendarText()
            controlsLayout.addWidget(self.fontSizeLabel)
            controlsLayout.addWidget(self.fontSizeSpinBox)
        else:
            self.insertCalendarWidget()
        controlsLayout.addStretch(1)
        self.month_select.combobox.activated.connect(self.setMonth)
        self.year_select.dateChanged.connect(self.setYear)
        if self.month_type == "text":
            self.fontSizeSpinBox.valueChanged.connect(self.setfontSize)
        self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop | pyqt.Qt.AlignmentFlag.AlignLeft)
        return self

    def initWidget(self):
        """"""
        self.initView()
        self.initModel()
        return self

    def insertCalendarWidget(self):
        """"""
        year = self.selectedDate.year()
        cfg = {
            "rows": 6,
            "columns": 7,
            "number": monthrange(self.selectedDate.year(), self.selectedDate.month())[1],
            "start_one": True,
        }
        grid = NchantdGrid(self, cfg).initWidget()
        self.layout.addWidget(grid)

    def insertCalendarText(self):
        self.editor.clear()
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()

        date = pyqt.QDate(self.selectedDate.year(), self.selectedDate.month(), 1)

        tableFormat = pyqt.QTextTableFormat()
        tableFormat.setAlignment(pyqt.Qt.AlignHCenter)
        tableFormat.setBackground(pyqt.QColor("#e0e0e0"))
        tableFormat.setCellPadding(2)
        tableFormat.setCellSpacing(4)
        constraints = [
            pyqt.QTextLength(pyqt.QTextLength.PercentageLength, 14),
            pyqt.QTextLength(pyqt.QTextLength.PercentageLength, 14),
            pyqt.QTextLength(pyqt.QTextLength.PercentageLength, 14),
            pyqt.QTextLength(pyqt.QTextLength.PercentageLength, 14),
            pyqt.QTextLength(pyqt.QTextLength.PercentageLength, 14),
            pyqt.QTextLength(pyqt.QTextLength.PercentageLength, 14),
            pyqt.QTextLength(pyqt.QTextLength.PercentageLength, 14),
        ]

        tableFormat.setColumnWidthConstraints(constraints)

        table = cursor.insertTable(1, 7, tableFormat)

        frame = cursor.currentFrame()
        frameFormat = frame.frameFormat()
        frameFormat.setBorder(1)
        frame.setFrameFormat(frameFormat)

        format = cursor.charFormat()
        format.setFontPointSize(self.fontSize)

        boldFormat = pyqt.QTextCharFormat(format)
        boldFormat.setFontWeight(pyqt.QFont.Bold)

        highlightedFormat = pyqt.QTextCharFormat(boldFormat)
        highlightedFormat.setBackground(pyqt.Qt.yellow)

        for weekDay in range(1, 8):
            cell = table.cellAt(0, weekDay - 1)
            cellCursor = cell.firstCursorPosition()
            weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            cellCursor.insertText(weekday_names[weekDay - 1], boldFormat)

        table.insertRows(table.rows(), 1)

        while date.month() == self.selectedDate.month():
            weekDay = date.dayOfWeek()
            cell = table.cellAt(table.rows() - 1, weekDay - 1)
            cellCursor = cell.firstCursorPosition()

            if date == pyqt.QDate.currentDate():
                cellCursor.insertText(str(date.day()), highlightedFormat)
            else:
                cellCursor.insertText(str(date.day()), format)

            date = date.addDays(1)

            if weekDay == 7 and date.month() == self.selectedDate.month():
                table.insertRows(table.rows(), 1)

        cursor.endEditBlock()
        months_name = calendar.month_name[self.selectedDate.month()]
        self.setWindowTitle("Calendar for %s %d" % (months_name, self.selectedDate.year()))

    def setfontSize(self, size):
        self.fontSize = size
        self.insertCalendar()

    def setMonth(self, month):
        self.selectedDate = pyqt.QDate(self.selectedDate.year(), month + 1, self.selectedDate.day())
        self.insertCalendar()

    def setYear(self, date):
        self.selectedDate = pyqt.QDate(date.year(), self.selectedDate.month(), self.selectedDate.day())
        self.insertCalendar()


class NchantdQuarterYearCalendar(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdQuarterYearCalendar").override(cfg))

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdMonthlyJournal(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdMonthlyJournal"))
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
        self.journal_group.setTitle("Monthly Journal Review")
        self.layout.addLayout(self.journal_group.layout)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdMonthDashboard(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdMonthDashboard"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.calendar = None
        self.month_overview_group = None

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """

        Show an overview of a schedule for the month
        show a summary of the journal for the month
        show budget information if fund is being used

        :return:
        """
        super().initView()
        cfg = {}
        self.month_overview_group = NchantdVScrollGroupBox(self, cfg)
        self.month_overview_group.setTitle("Monthly Overview")
        self.layout.addLayout(self.month_overview_group.layout)
        cfg = {}
        self.calendar = NchantdMonthCalendar(self, cfg).initWidget()
        self.month_overview_group.addWidget(self.calendar)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
