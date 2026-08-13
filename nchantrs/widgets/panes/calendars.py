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
from typing import Any
from os.path import abspath, dirname, join
import datetime as dt
import calendar
from calendar import monthrange

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.widgets.panes.panes import NchantdPane
from nchantrs.libraries import pyqt
from nchantrs.widgets.media.editors.selectors import NchantdDropDown
from nchantrs.widgets.tables.tables import NchantdGrid

# ====================================================================================================================||
HERE = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
if not log:
    logma.off()
# ====================================================================================================================||
PXCFG = join(HERE, "_data_", "calendars.yaml")


class NchantdCalendarDetailPane(NchantdPane):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(PXCFG).select("NchantdCalendarDetailPane").override(cfg))

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        group = pyqt.QGroupBox("Calendar Details")
        self.group_layout = pyqt.QVBoxLayout()
        group.setLayout(self.group_layout)
        self.group_layout.addStretch()
        self.layout.addWidget(group, stretch=1)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdMonthCalendarPane(NchantdPane):
    """The Month Calendar will be a fixed window for a multiweek calendar with fixed end points"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(PXCFG).select("NchantdMonthCalendarPane").override(cfg))
        self.month_type = None
        self.journal_notes = None

    def initModel(self) -> Any:
        """"""
        super().initModel()
        datetime = self.config.dikt.get("datetime", dt.datetime.now())
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        cfg = cfg or {}
        cfg["layout"] = "vertical"
        super().initView(cfg)
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
        controlsLayout = pyqt.QHBoxLayout()
        self.layout.addLayout(controlsLayout)
        # controlsLayout.addWidget(self.month_select)
        # controlsLayout.addWidget(self.year_select)
        # controlsLayout.addSpacing(24)
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
            # controlsLayout.addWidget(self.fontSizeLabel)
            # controlsLayout.addWidget(self.fontSizeSpinBox)
        else:
            self.insertCalendarWidget()
        # controlsLayout.addStretch(1)
        self.month_select.combobox.activated.connect(self.setMonth)
        self.year_select.dateChanged.connect(self.setYear)
        if self.month_type == "text":
            self.fontSizeSpinBox.valueChanged.connect(self.setfontSize)
        # self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop | pyqt.Qt.AlignmentFlag.AlignLeft)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initView()
        self.initModel()
        return self

    def insertCalendarWidget(self) -> None:
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

    def insertCalendarText(self) -> None:
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

    def setfontSize(self, size) -> None:
        self.fontSize = size
        self.insertCalendar()

    def setMonth(self, month) -> None:
        self.selectedDate = pyqt.QDate(self.selectedDate.year(), month + 1, self.selectedDate.day())
        self.insertCalendar()

    def setYear(self, date) -> None:
        self.selectedDate = pyqt.QDate(date.year(), self.selectedDate.month(), self.selectedDate.day())
        self.insertCalendar()


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
