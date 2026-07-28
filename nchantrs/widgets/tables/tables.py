# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
    docid:
    name: Nchantrs Widgets Tables Python Excecution Document  #	||
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

# ======================================3rd Party Library Modules=====================================================||
from pandas import DataFrame

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from nchantrs.libraries import pyqt, qpandas
from nchantrs.widgets.items.cells import NchantdCell, NchantdTableCell
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from kahndor.logma import Logma
from thingery.numbers.numerals import calcExtendedRomanNumerals, calcArabicNumerals

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
debug = True
logma = Logma(__name__)
log = True
if not log:
    logma.off()
# ====================================================================================================================||
pxcfg = join(abspath(here), "_data_", "tables.yaml")


class NchantdTable(NchantdWidgetMixin, pyqt.QTableWidget):
    """ """

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(10, 10, parent)
        self.parent = parent
        self.setParent(parent)
        self.config = kahndor.Instruct(pxcfg).select("NchantdTable").override(parent.config).override(cfg)
        self.current_cell = "I|1"
        self.cell_handlers = {}
        self.columns = None
        self.column_handlers = {}
        self.rows = None
        self.row_handlers = {}

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        return self

    def initView(self, initialize_rows=False):
        """ """
        super().initView()
        self.set_handler_cell(self.config.dikt.get("cell_handler", None))
        self.set_handler_column(self.config.dikt.get("column_handler", None))
        self.set_handler_row(self.config.dikt.get("row_handler", None))
        self.set_columns(self.config.dikt.get("columns", None))
        self.set_column_widths()
        # self.setSelectionBehavior(pyqt.QTableWidget.SelectionBehavior.SelectRows)
        # self.setSelectionMode(pyqt.QTableWidget.SelectionMode.SingleSelection)
        # self.setSelectionBehavior(pyqt.QTableWidget.SelectionBehavior.SelectColumns)
        # self.setSelectionBehavior(pyqt.QTableWidget.SelectionBehavior.SelectItems)
        # self.horizontalHeader().sectionDoubleClicked
        # self.horizontalHeader().sectionResized.connect(self.on_column_changed)
        # self.horizontalHeader().sectionEntered
        # self.horizontalHeader().sectionHandleDoubleClicked
        self.horizontalHeader().sectionPressed.connect(self.on_column_selected)
        self.horizontalHeader().sectionClicked.connect(self.on_column_clicked)
        self.verticalHeader().sectionClicked.connect(self.on_row_clicked)
        self.verticalHeader().sectionPressed.connect(self.on_row_selected)
        # self.verticalHeader().sectionDoubleClicked
        # self.verticalHeader().sectionResized.connect(self.on_column_changed)
        # self.verticalHeader().sectionEntered
        # self.verticalHeader().sectionHandleDoubleClicked
        self.cellActivated.connect(self.on_cell_activated)
        self.cellChanged.connect(self.on_cell_changed)
        self.cellClicked.connect(self.on_cell_clicked)
        self.cellDoubleClicked.connect(self.on_cell_clicked_double)
        self.cellEntered.connect(self.on_cell_entered)
        self.cellPressed.connect(self.on_cell_pressed)
        self.itemActivated.connect(self.on_item_activated)
        self.itemChanged.connect(self.on_item_changed)
        self.itemClicked.connect(self.on_item_clicked)
        self.itemDoubleClicked.connect(self.on_item_clicked_double)
        self.itemEntered.connect(self.on_item_entered)
        self.itemPressed.connect(self.on_item_pressed)
        self.itemSelectionChanged.connect(self.on_item_selection_changed)
        self.setHorizontalHeaderLabels(self.get_roman_numeral_headers() if self.columns is None else self.columns)
        self.set_data(self.config.dikt.get("data", []))
        self.setSizePolicy(pyqt.QSizePolicy.Policy.Expanding, pyqt.QSizePolicy.Policy.Expanding)
        return self

    def initWidget(self, initialize_rows=False):
        """ """
        self.initModel()
        self.initView(initialize_rows)
        return self

    def get_cell(self, row=None, column=None):
        """"""
        if row is None or column is None:
            row, column = self.get_current_cell()
        logma.info(f"Cell Value {row} {column}")
        return self.item(int(row), int(column))

    def get_cell_value(self, row=None, column=None):
        """"""
        if row is None or column is None:
            row, column = self.get_current_cell()
        logma.info(f"Cell Value {row} {column}")
        return self.item(int(row), int(column)).text()

    def get_current_cell(self):
        """"""
        column, row = self.current_cell.split("|")
        return int(row), int(self.lookup_column(column))

    def get_roman_numeral_headers(self):
        """"""
        logma.warning(f"calc roman numerals")
        return [calcExtendedRomanNumerals(x) for x in range(1, self.columnCount() + 1)]

    def lookup_column(self, column):
        """"""
        column = calcArabicNumerals(column)
        return column

    def on_cell_changed(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Cell Changed {event} {row} {column}")
        return self

    def on_cell_activated(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Cell Activated {event} {row} {column}")
        return self

    def on_cell_clicked(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Cell Clicked {event} {row} {column}")

        return self

    def on_cell_clicked_double(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Cell Clicked Double {event} {row} {column}")
        return self

    def on_cell_clicked_right(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Cell Clicked Right {event} {row} {column}")
        self.set_current_cell(row, column)
        return self

    def on_cell_entered(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Cell Entered {event} {row} {column}")
        return self

    def on_cell_pressed(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Cell Pressed {event} {row} {column}")
        self.set_current_cell(row, column)
        #logma.info(f"Column Handlers {self.column_handlers}")
        if column in self.column_handlers.keys():
            if self.column_handlers[column] is not None:
                if callable(self.column_handlers[column]):
                    self.column_handlers[column]()
        # get cell column
        # check all handlers for that column
        # get cell row
        # check all handlers for that row
        return self

    def on_column_activated(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Column Activated {event} {row} {column}")
        return self

    def on_column_changed(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Column Changed {event} {row} {column}")
        return self

    def on_column_clicked(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Column Clicked {event} {row} {column}")
        return self

    def on_column_selected(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Column Selected {event} {row} {column}")
        return self

    def on_item_activated(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Item Activated {event} {row} {column}")
        return self

    def on_item_changed(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Item Changed {event} {row} {column}")
        return self

    def on_item_clicked(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Item Clicked {event} {row} {column}")

        return self

    def on_item_clicked_double(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Item Clicked Double {event} {row} {column}")
        return self

    def on_item_clicked_left(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Item Clicked Left {event} {row} {column}")
        return self

    def on_item_clicked_middle(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Item Clicked Middle {event} {row} {column}")
        return self

    def on_item_clicked_right(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Item Clicked Right {event} {row} {column}")
        return self

    def on_item_entered(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Item Entered {event} {row} {column}")
        return self

    def on_item_pressed(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Item Pressed {event} {row} {column}")
        return self

    def on_item_selection_changed(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Item Selection Changed {event} {row} {column}")
        return self

    def on_row_activated(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Row Activated {event} {row} {column}")
        return self

    def on_row_clicked(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Row Clicked {event} {row} {column}")
        return self

    def on_row_selected(self, row=None, column=None, event=None, *args, **kwargs):
        """"""
        #logma.info(f"Row Selected {event} {row} {column}")
        return self

    def reset_column_widths(self):
        """"""
        self.horizontalHeader().setSectionResizeMode(pyqt.QHeaderView.Stretch)

    def set_columns(self, columns):
        """"""
        if isinstance(columns, dict):
            for column, details in columns.items():
                column_idx = list(self.config.dikt.get("columns", {}).keys()).index(column)
                if "handler" in details:
                    logma.info(f"Handler {details['handler']} {column_idx}")
                    self.set_handler_column(details["handler"], column_idx)
            columns = list(columns.keys())
        self.columns = columns
        return self

    def set_column_numbers(self, data=None):
        """"""
        num_columns = self.config.dikt.get("num_columns", 3)
        if self.columns is not None:
            num_columns = len(self.columns) if len(self.columns) > 0 else self.config.dikt.get("num_columns", 3)
        if isinstance(data, DataFrame):
            self.columns = data.columns.tolist()
            num_columns = len(self.columns) if len(self.columns) > 0 else self.config.dikt.get("num_columns", 3)
        elif isinstance(data, list):
            num_columns = len(data[0]) if len(data) > 0 else self.config.dikt.get("num_columns", 3)
        logma.info(f"Num Columns {num_columns}")
        self.setColumnCount(num_columns)
        logma.info(f"Columns {self.columns}")
        self.setHorizontalHeaderLabels(self.get_roman_numeral_headers() if self.columns is None else self.columns)

    def set_column_widths(self):
        """"""
        self.default_column_width = self.config.dikt.get("column_width", None)
        self.max_column_width = self.config.dikt.get("max_column_width", None)
        self.min_column_width = self.config.dikt.get("min_column_width", None)
        if self.max_column_width is None:
            self.max_column_width = 300
        if self.min_column_width is None:
            self.min_column_width = 20
        return self

    def set_current_cell(self, row, column):
        """"""
        logma.info(f"Set Current Cell {row} {column}")
        logma.info(f"calc roman numerals")
        column = calcExtendedRomanNumerals(column)
        self.current_cell = f"{column}|{row}"
        return self

    def set_row_numbers(self, data=None):
        """"""
        num_rows = self.config.dikt.get("num_rows", 3)
        self.rows = self.config.dikt.get("rows", [])
        if self.rows is not None:
            num_rows = len(self.rows) if len(self.rows) > 0 else self.config.dikt.get("num_rows", 3)
        if isinstance(data, DataFrame):
            self.rows = data.index.tolist()
        elif isinstance(data, list):
            num_rows = len(data) if len(data) > 0 else self.config.dikt.get("num_rows", 3)
            self.rows = data
        num_rows = len(self.rows) if len(self.rows) > 0 else num_rows
        logma.info(f"Num Rows {num_rows}")
        self.setRowCount(num_rows)

    def set_data(self, data):
        """"""
        self.setRowCount(self.config.dikt.get("num_rows", 3))
        self.set_column_numbers(self.config.dikt.get("num_columns", 3))
        logma.info(f"Data {data}")
        #for sheet in data:
        #
        if data is None or data == []:
            return self
        self.setRowCount(len(data) if len(data) > 0 else self.config.dikt.get("num_rows", 3))
        
        self.set_column_numbers(len(data[0]) if data else self.config.dikt.get("num_columns", 3))
        x = 0
        width = {}
        for col in range(self.columnCount()):
            column_widget = None
            column_name = None
            if self.columns:
                column_name = self.columns[col]
            if column_name in self.config.dikt.get("column_widgets", {}):
                column_widget = self.config.dikt["column_widgets"][column_name]
            #logma.info(f"Column Widget {column_widget}")
            y = 0
            width[col] = self.min_column_width
            for row in range(self.rowCount()):
                d = ""
                if row >= len(data):
                    continue
                if col >= len(data[row]):
                    continue
                try:
                    d = data[row][col]
                    if d == "":
                        continue
                    #logma.info(f"Row {row} Col {col} {d}")
                except Exception as e:
                    if debug:
                        logma.warning(e)
                        raise e
                if column_widget is None:
                    #logma.info(f"Col {col} {d}")
                    cfg = {"text": d}
                    #need to hold data in a dictionary?
                    self.setItem(y, x, NchantdTableCell(self, cfg).initWidget())
                    self.set_font()
                    # d_width = self._check_text_length_size(str(d))
                    # if self.config.dikt["column_widths"] is None:
                    #     width[col] = d_width if width[col] < d_width <= self.max_column_width else width[col]
                else:
                    self.assign_widget(column_name, x, y, d)
                y += 1
            x += 1
        self.set_column_numbers()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        # if self.config.dikt["column_widths"]:
        #     for col in range(self.columnCount()):
        #         self.setColumnWidth(col, self.config.dikt["column_widths"][col])
        # else:
        #     for col in range(self.columnCount()):
        #         # logma.info(f"Col {col} {width[col]}")
        #         self.setColumnWidth(col, width[col])
        return self

    def assign_widget(self, column_name, x, y, d=None):
        """Override in subclasses to render a non-text cell (buttonbar, datetime, etc.).

        ``d`` is the cell's data value (kept for subclass overrides that
        need it). The base class returns ``NotImplemented`` so the
        caller can fall through to a text-cell render.
        """
        return NotImplemented

    def set_font(self):
        """"""
        self.font = pyqt.QFont("Arial", 10)
        return self

    def set_font_size(self):
        """"""
        return self

    def set_handler_cell(self, handler):
        """"""
        return self

    def set_handler_row(self, handler):
        """"""
        return self

    def set_handler_column(self, handler, column=0):
        """"""
        logma.info(f"Set Handler Column {handler} {column}")
        self.column_handlers[column] = handler
        logma.info(f"Column Handlers {self.column_handlers}")
        return self

    def setHorizontalHeaderLabels(self, labels):
        super().setHorizontalHeaderLabels(labels)
        for col in range(self.columnCount()):
            if len(labels) > col:
                header_length = self._check_text_length_size(labels[col])
                if self.columnWidth(col) < header_length * 1.1:
                    self.setColumnWidth(col, int(header_length * 1.1))

    def set_row_select(self):
        """"""
        self.setSelectionBehavior(pyqt.QAbstractItemView.SelectRows)
        return self

    def setSelectionBehavior(self, behavior):
        """"""

    def update_data(self, data):
        """"""
        self.clear()
        self.clearContents()
        self.setRowCount(0)
        if isinstance(data, DataFrame):
            data_ = [data.columns.tolist()]
            data_ += data.values.tolist()
            data = data_
        self.set_data(data)
        self.repaint()

        # self.table.clearContents()
        # with open(file_path, "r", encoding="utf-8") as f:
        #     reader = csv.reader(f)
    #     for row_idx, row in enumerate(reader):
    #         for col_idx, value in enumerate(row):
    #             if col_idx >= self.table.columnCount():
    #                 self.table.insertColumn(col_idx)
    #                 self.table.setHorizontalHeaderItem(col_idx, pyqt.QTableWidgetItem(chr(65 + col_idx)))
    #             item = pyqt.QTableWidgetItem(value)
    #             self.table.setItem(row_idx, col_idx, item)
    #         if row_idx >= self.table.rowCount() - 1:
    #             self.table.insertRow(row_idx + 1)

        return self

    def _check_text_length_size(self, text):
        """"""
        # TODO need to find any \n values and split to check the longest section of text
        self.set_font()
        # logma.info(f"Font {self.font}")
        if self.font is not None:
            metrics = pyqt.QFontMetrics(self.font)
            return metrics.horizontalAdvance(text)


class NchantdDataFrameTable(NchantdWidgetMixin, qpandas.DataTableWidget):
    """ """

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__()
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdDataFrameTable").override(parent.config).override(cfg)
        self.model = qpandas.DataFrameModel()

    def initModel(self, df=None):
        """ """
        super().initModel()
        if df is None:
            df = DataFrame()
        self.model.setDataFrame(df)
        return self

    def initView(self):
        """ """
        super().initView()
        self.setFrameShape(pyqt.QTableWidget.NoFrame)
        self.setFrameShadow(pyqt.QTableWidget.Plain)
        self.setViewModel(self.model)
        return self

    def initWidget(self):
        """ """
        self.initModel()
        self.initView()
        return self

    def set_dataframe(self, df, copy=False):
        """"""
        self.model.setDataFrame(df, copy)
        return self


class NchantdTableWidget(NchantdWidget):
    """"""
    def __init__(self, parent=None, cfg=None):
        """"""
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdTableWidget").override(cfg))
        self.table = None

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        self.table = NchantdTable(self, cfg).initWidget()
        self.layout.addWidget(self.table)

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()



class NchantdGrid(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdGrid").override(cfg))
        self.rows = None
        self.columns = None
        self.cells = []

    def initModel(self):
        """"""
        super().initModel()
        self.rows = self.config.dikt.get("rows", 3)
        self.columns = self.config.dikt.get("columns", 11)
        return self

    def initView(self):
        """"""
        super().initView()
        # self.setWindowTitle("Grid of Cells")
        # self.resize(400, 400)
        # Create a QGroupBox to hold the grid
        self.grid_group = pyqt.QGroupBox()
        grid_layout = pyqt.QGridLayout()
        # Add cells (as QLabel) to the grid layout
        width, height = self.get_viewport_size().width(), self.get_viewport_size().height()
        logma.info(f"Size {width} {height}")
        size = [width // self.columns, height // self.rows]
        logma.info(f"Size {size}")
        cnt = 0
        for row in range(self.rows):
            for col in range(self.columns):
                cfg = {"row": row, "column": col, "size": size}
                if self.config.dikt.get("number", None) is not None:
                    if self.config.dikt["number"] > cnt:
                        cfg["label"] = cnt
                        if self.config.dikt.get("start_one", None) is not None:
                            cfg["label"] += 1
                cell = NchantdCell(self, cfg).initWidget()
                self.cells.append(cell)
                grid_layout.addWidget(cell, row, col)
                grid_layout.setContentsMargins(0, 0, 0, 0)
                cnt += 1
        # Set the grid layout to the QGroupBox
        self.grid_group.setLayout(grid_layout)
        self.layout.addWidget(self.grid_group)
        self.layout.setContentsMargins(0, 0, 0, 0)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def setTitle(self, title):
        """"""
        self.grid_group.setTitle(title)
        return self

    def update_number(self, number):
        """"""
        if number > len(self.cells):
            pass
        elif number < len(self.cells):
            for cell in self.cells[number:]:
                cell.hide()
            self.cells = self.cells[:number]
        else:
            return self

        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
