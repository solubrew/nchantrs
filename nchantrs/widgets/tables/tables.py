from typing import Any, List, Tuple

"\n---\n<(META)>:\n    docid:\n    name: Nchantrs Widgets Tables Python Excecution Document  #\t||\n    description: >\n    version: 0.0.0.0.0.0\n    authority: filesystem\n    security: seclvl2\n    <(WT)>: -32\n"
from os.path import abspath, dirname, join
import datetime as dt
from pandas import DataFrame
from kahndor import kahndor
from nchantrs.libraries import pyqt, qpandas
from nchantrs.widgets.items.cells import NchantdCell, NchantdTableCell
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from kahndor.logma import Logma
from thingery.numbers.numerals import calcExtendedRomanNumerals, calcArabicNumerals

here = join(dirname(__file__), "")
debug = True
logma = Logma(__name__)
log = True
if not log:
    logma.off()
pxcfg = join(abspath(here), "_data_", "tables.yaml")


class NchantdTable(NchantdWidgetMixin, pyqt.QTableWidget):
    """ """

    def __init__(self, parent=None, cfg=None) -> None:
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

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, initialize_rows=False) -> Any:
        """ """
        super().initView()
        self.set_handler_cell(self.config.dikt.get("cell_handler", None))
        self.set_handler_column(self.config.dikt.get("column_handler", None))
        self.set_handler_row(self.config.dikt.get("row_handler", None))
        self.set_columns(self.config.dikt.get("columns", None))
        self.set_column_widths()
        self.horizontalHeader().sectionPressed.connect(self.on_column_selected)
        self.horizontalHeader().sectionClicked.connect(self.on_column_clicked)
        self.verticalHeader().sectionClicked.connect(self.on_row_clicked)
        self.verticalHeader().sectionPressed.connect(self.on_row_selected)
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

    def initWidget(self, initialize_rows=False) -> Any:
        """ """
        self.initModel()
        self.initView(initialize_rows)
        return self

    def get_cell(self, row=None, column=None) -> Any:
        """"""
        if row is None or column is None:
            row, column = self.get_current_cell()
        logma.info(f"Cell Value {row} {column}")
        return self.item(int(row), int(column))

    def get_cell_value(self, row=None, column=None) -> Any:
        """"""
        if row is None or column is None:
            row, column = self.get_current_cell()
        logma.info(f"Cell Value {row} {column}")
        return self.item(int(row), int(column)).text()

    def get_current_cell(self) -> Tuple[int, int]:
        """"""
        column, row = self.current_cell.split("|")
        return (int(row), int(self.lookup_column(column)))

    def get_roman_numeral_headers(self) -> List[Any]:
        """"""
        logma.warning(f"calc roman numerals")
        return [calcExtendedRomanNumerals(x) for x in range(1, self.columnCount() + 1)]

    def lookup_column(self, column) -> Any:
        """"""
        column = calcArabicNumerals(column)
        return column

    def on_cell_changed(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_cell_changed {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_cell_activated(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_cell_activated {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_cell_clicked(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_cell_clicked {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_cell_clicked_double(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_cell_clicked_double {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_cell_clicked_right(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        """"""
        self.set_current_cell(row, column)
        return self

    def on_cell_entered(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_cell_entered {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_cell_pressed(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        """"""
        self.set_current_cell(row, column)
        if column in self.column_handlers.keys():
            if self.column_handlers[column] is not None:
                if callable(self.column_handlers[column]):
                    self.column_handlers[column]()
        return self

    def on_column_activated(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_column_activated {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_column_changed(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_column_changed {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_column_clicked(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_column_clicked {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_column_selected(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_column_selected {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_item_activated(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_item_activated {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_item_changed(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_item_changed {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_item_clicked(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_item_clicked {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_item_clicked_double(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_item_clicked_double {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_item_clicked_left(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_item_clicked_left {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_item_clicked_middle(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_item_clicked_middle {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_item_clicked_right(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_item_clicked_right {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_item_entered(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_item_entered {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_item_pressed(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_item_pressed {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_item_selection_changed(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_item_selection_changed {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_row_activated(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_row_activated {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_row_clicked(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_row_clicked {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_row_selected(self, row=None, column=None, event=None, *args, **kwargs) -> Any:
        logma.info(f"on_row_selected {event} {row} {column}")
        if row is not None and column is not None:
            self.set_current_cell(row, column)
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def reset_column_widths(self) -> None:
        """"""
        self.horizontalHeader().setSectionResizeMode(pyqt.QHeaderView.Stretch)

    def set_columns(self, columns) -> Any:
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

    def set_column_numbers(self, data=None) -> None:
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

    def set_column_widths(self) -> Any:
        """"""
        self.default_column_width = self.config.dikt.get("column_width", None)
        self.max_column_width = self.config.dikt.get("max_column_width", None)
        self.min_column_width = self.config.dikt.get("min_column_width", None)
        if self.max_column_width is None:
            self.max_column_width = 300
        if self.min_column_width is None:
            self.min_column_width = 20
        return self

    def set_current_cell(self, row, column) -> Any:
        """"""
        logma.info(f"Set Current Cell {row} {column}")
        logma.info(f"calc roman numerals")
        column = calcExtendedRomanNumerals(column)
        self.current_cell = f"{column}|{row}"
        return self

    def set_row_numbers(self, data=None) -> None:
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

    def set_data(self, data) -> Any:
        """"""
        self.setRowCount(self.config.dikt.get("num_rows", 3))
        self.set_column_numbers(self.config.dikt.get("num_columns", 3))
        logma.info(f"Data {data}")
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
                except Exception as e:
                    if debug:
                        logma.warning(e)
                        raise e
                if column_widget is None:
                    cfg = {"text": d}
                    self.setItem(y, x, NchantdTableCell(self, cfg).initWidget())
                    self.set_font()
                else:
                    self.assign_widget(column_name, x, y, d)
                y += 1
            x += 1
        self.set_column_numbers()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        return self

    def assign_widget(self, column_name, x, y, d=None) -> Any:
        """Override in subclasses to render a non-text cell (buttonbar, datetime, etc.).

        ``d`` is the cell's data value (kept for subclass overrides that
        need it). The base class returns ``NotImplemented`` so the
        caller can fall through to a text-cell render.
        """
        return NotImplemented

    def set_font(self) -> Any:
        """"""
        self.font = pyqt.QFont("Arial", 10)
        return self

    def set_font_size(self) -> Any:
        font = pyqt.QFont()

    def set_handler_cell(self, handler) -> Any:
        if handler is not None and callable(handler):
            self.cell_handlers[key] = handler
        return self

    def set_handler_row(self, handler) -> Any:
        if handler is not None and callable(handler):
            self.row_handlers[key] = handler
        return self

    def set_handler_column(self, handler, column=0) -> Any:
        """"""
        logma.info(f"Set Handler Column {handler} {column}")
        self.column_handlers[column] = handler
        logma.info(f"Column Handlers {self.column_handlers}")
        return self

    def setHorizontalHeaderLabels(self, labels) -> None:
        super().setHorizontalHeaderLabels(labels)
        for col in range(self.columnCount()):
            if len(labels) > col:
                header_length = self._check_text_length_size(labels[col])
                if self.columnWidth(col) < header_length * 1.1:
                    self.setColumnWidth(col, int(header_length * 1.1))

    def set_row_select(self) -> Any:
        """"""
        self.setSelectionBehavior(pyqt.QAbstractItemView.SelectRows)
        return self

    def setSelectionBehavior(self, behavior) -> None:
        logma.info(f"setSelectionBehavior called")
        return self

    def update_data(self, data) -> Any:
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
        return self

    def _check_text_length_size(self, text) -> Any:
        """"""
        self.set_font()
        if self.font is not None:
            metrics = pyqt.QFontMetrics(self.font)
            return metrics.horizontalAdvance(text)


class NchantdDataFrameTable(NchantdWidgetMixin, qpandas.DataTableWidget):
    """A pandas-backed table widget."""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__()
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdDataFrameTable").override(parent.config).override(cfg)
        self.model = qpandas.DataFrameModel()
        logma.info(f"NchantdDataFrameTable initialized")

    def initModel(self, df=None) -> Any:
        """ """
        super().initModel()
        if df is None:
            df = DataFrame()
        self.model.setDataFrame(df)
        return self

    def initView(self) -> Any:
        """ """
        super().initView()
        self.setFrameShape(pyqt.QTableWidget.NoFrame)
        self.setFrameShadow(pyqt.QTableWidget.Plain)
        self.setViewModel(self.model)
        return self

    def initWidget(self) -> Any:
        """ """
        self.initModel()
        self.initView()
        return self

    def set_dataframe(self, df, copy=False) -> Any:
        """"""
        self.model.setDataFrame(df, copy)
        return self


class NchantdTableWidget(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdTableWidget").override(cfg))
        self.table = None

    def initModel(self, cfg=None) -> None:
        """"""
        super().initModel(cfg)

    def initView(self, cfg=None) -> None:
        """"""
        super().initView(cfg)
        self.table = NchantdTable(self, cfg).initWidget()
        self.layout.addWidget(self.table)

    def initWidget(self) -> None:
        """"""
        self.initModel()
        self.initView()


class NchantdGrid(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdGrid").override(cfg))
        self.rows = None
        self.columns = None
        self.cells = []

    def initModel(self) -> Any:
        """"""
        super().initModel()
        self.rows = self.config.dikt.get("rows", 3)
        self.columns = self.config.dikt.get("columns", 11)
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.grid_group = pyqt.QGroupBox()
        grid_layout = pyqt.QGridLayout()
        # width, height = (self.get_viewport_size().width(), self.get_viewport_size().height())
        # logma.info(f'Size {width} {height}')
        # size = [width // self.columns, height // self.rows]
        # logma.info(f'Size {size}')
        size = 10
        cnt = 0
        for row in range(self.rows):
            for col in range(self.columns):
                cfg = {"row": row, "column": col, "size": size}
                if self.config.get("number", None) is not None:
                    if self.config.get("number", 0) > cnt:
                        cfg["text"] = cnt
                        if self.config.get("start_one", None) is not None:
                            cfg["text"] += 1
                cell = NchantdCell(self, cfg).initWidget()
                if not isinstance(cell, pyqt.QWidget):
                    container = pyqt.QWidget(self)
                    layout = pyqt.QVBoxLayout(container)
                    layout.setContentsMargins(0, 0, 0, 0)
                    if isinstance(cell, pyqt.QTableWidgetItem):
                        label = pyqt.QLabel(container)
                        label.setText(str(getattr(cell, "text", lambda: "")()) or "")
                        layout.addWidget(label)
                    container.setLayout(layout)
                    self.cells.append(container)
                    grid_layout.addWidget(container, row, col)
                else:
                    self.cells.append(cell)
                    grid_layout.addWidget(cell, row, col)
                grid_layout.setContentsMargins(0, 0, 0, 0)
                cnt += 1
        self.grid_group.setLayout(grid_layout)
        self.layout.addWidget(self.grid_group)
        self.layout.setContentsMargins(0, 0, 0, 0)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def setTitle(self, title) -> Any:
        """"""
        self.grid_group.setTitle(title)
        return self

    def update_number(self, number) -> Any:
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
