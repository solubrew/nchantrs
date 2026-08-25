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
from typing import Any, List, Tuple


from os.path import abspath, dirname, join
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||
from pandas import DataFrame

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma

from kahndor import kahndor
from nchantrs.libraries import pyqt, qpandas
from nchantrs.widgets.items.cells import NchantdCell, NchantdTableCell
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from kahndor.logma import Logma
from thingery.numbers.numerals import calcExtendedRomanNumerals, calcArabicNumerals

# ====================================================================================================================||
HERE = join(dirname(__file__), "")  # ||
log = False
logma = Logma(__name__)
if not log:
    logma.off()
# ====================================================================================================================||
PXCFG = join(HERE, "_data_", "tables.yaml")


class NchantdTable(NchantdWidgetMixin, pyqt.QTableWidget):
    """ """

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(10, 10, parent)
        self.parent = parent
        self.setParent(parent)
        self.config = kahndor.Instruct(PXCFG).select("NchantdTable").override(parent.config).override(cfg)
        self.current_cell = "I|1"
        self.cell_handlers = {}
        self.columns = None
        self.column_handlers = {}
        self.rows = None
        self.row_handlers = {}
        # -- lazy-load state (Option A: viewport-driven row population) ------------
        self.lazy_load = self.config.dikt.get("lazy_load", True)
        self.lazy_buffer_rows = self.config.dikt.get("lazy_buffer_rows", 10)
        self._data = []
        self._built_rows = set()
        self._lazy_connected = False

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
        """Populate the table, lazily building rows as they scroll into view.

        When ``lazy_load`` is enabled (the default) the row/column counts are
        set so the scrollbar geometry matches the full dataset, but only the
        rows visible in the viewport -- plus a ``lazy_buffer_rows`` look-ahead
        buffer -- are materialised into cell widgets. The remaining rows are
        built on demand from ``verticalScrollBar().valueChanged`` (see
        :meth:`_populate_visible_rows`). Set ``lazy_load: False`` in the config
        to restore the eager, build-everything-up-front behaviour.

        Note: cells are placed at their true ``(row, col)`` index so the
        scroll position lines up with the underlying data. Empty ("") values
        simply render no widget rather than collapsing later rows upward.
        """
        self.setRowCount(self.config.dikt.get("num_rows", 3))
        self.set_column_numbers(self.config.dikt.get("num_columns", 3))
        logma.info(f"Data {data}")
        self._data = data if isinstance(data, list) else []
        self._built_rows = set()
        if data is None or data == []:
            return self
        if not isinstance(data, list):
            raise Exception("Data Must be in Row of Rows List format")
        self.setRowCount(len(data) if len(data) > 0 else self.config.dikt.get("num_rows", 3))
        self.set_column_numbers(len(data[0]) if data else self.config.dikt.get("num_columns", 3))
        if self.lazy_load:
            self._connect_lazy_scroll()
            self._populate_visible_rows()
        else:
            for row in range(self.rowCount()):
                self._build_row(row)
        self.set_column_numbers()
        self.resizeColumnsToContents()
        if not self.lazy_load:
            self.resizeRowsToContents()
        return self

    def _build_row(self, row) -> None:
        """Materialise the cell widgets for a single ``row`` of ``self._data``.

        Idempotent: a row already present in ``self._built_rows`` is skipped,
        so repeated scroll callbacks never rebuild the same cells.
        """
        if row in self._built_rows:
            return
        data = self._data or []
        if row >= len(data):
            return
        for col in range(self.columnCount()):
            column_name = self.columns[col] if self.columns and col < len(self.columns) else None
            column_widget = self.config.dikt.get("column_widgets", {}).get(column_name)
            if col >= len(data[row]):
                continue
            try:
                d = data[row][col]
            except Exception as e:
                logma.warning(e)
                continue
            if d == "":
                continue
            if column_widget is None:
                self.setItem(row, col, NchantdTableCell(self, {"text": d}).initWidget())
                self.set_font()
            else:
                self.assign_widget(column_name, col, row, d)
        self._built_rows.add(row)
        # Eager mode sizes every row once via resizeRowsToContents(); a lazily
        # built row is never covered by that bulk pass, so size it here or its
        # content clips to the default row height.
        if self.lazy_load:
            self.resizeRowToContents(row)

    def _connect_lazy_scroll(self) -> None:
        """Wire the vertical scrollbar to on-demand row population (once)."""
        if self._lazy_connected:
            return
        self.verticalScrollBar().valueChanged.connect(lambda _=None: self._populate_visible_rows())
        self._lazy_connected = True

    def _populate_visible_rows(self) -> None:
        """Build the rows currently in the viewport plus a look-ahead buffer."""
        if not self._data:
            return
        buffer = self.lazy_buffer_rows
        first = self.rowAt(0)
        if first < 0:
            first = 0
        last = self.rowAt(self.viewport().height())
        if last < 0:
            # Viewport geometry is not resolved yet (first paint during
            # initView) or the last painted row is scrolled past. Estimate how
            # many rows fit rather than falling back to rowCount() - 1, which
            # would build the whole dataset and defeat lazy loading.
            row_h = self.rowHeight(first) or self.verticalHeader().defaultSectionSize() or 1
            height = self.viewport().height()
            visible = max(1, height // row_h) if height > 0 else buffer
            last = min(self.rowCount() - 1, first + visible)
        start = max(0, first - buffer)
        end = min(self.rowCount(), last + 1 + buffer)
        for row in range(start, end):
            self._build_row(row)

    def resizeEvent(self, event) -> None:
        """Repopulate on resize so a taller viewport fills in newly-shown rows."""
        super().resizeEvent(event)
        if getattr(self, "lazy_load", False):
            self._populate_visible_rows()

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


class NchantdLargeTable(NchantdTable):
    """Lazy *data-loading* table for datasets too large to hold in memory.

    :class:`NchantdTable` lazily *renders* an in-memory dataset -- every row
    already lives in ``self._data`` and only the cell widgets are built on
    demand as rows scroll into view. ``NchantdLargeTable`` extends that idea to
    the data itself: rows are fetched from a pluggable provider in fixed-size
    chunks as the viewport reaches them, so the full dataset never has to be
    resident in ``self._data`` at once.

    STUB: the chunk-fetch plumbing (``set_provider``, ``_chunk_for_row``,
    ``_ensure_rows_loaded``) is scaffolded and hooked into the inherited
    viewport machinery via :meth:`_populate_visible_rows`, but the provider
    protocol itself is not implemented yet -- :meth:`_fetch_chunk` raises
    ``NotImplementedError`` until a concrete data source is wired in. With no
    provider registered the class degrades to plain :class:`NchantdTable`
    behaviour over whatever is already in ``self._data``.

    Parameters:
        - parent (QWidget): The parent widget. Default is None.
        - cfg (dict): Configuration overrides. Default is None.

    Config keys (``NchantdLargeTable`` section of ``tables.yaml``):
        - chunk_size (int): rows fetched per provider request. Default 100.
        - total_rows (int): total rows the provider can serve; used to size the
          scrollbar geometry up front. Default 0.
    """

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(PXCFG).select("NchantdLargeTable").override(cfg))
        # -- chunked data-loading state ------------------------------------
        self.chunk_size = self.config.dikt.get("chunk_size", 100)
        self.total_rows = self.config.dikt.get("total_rows", 0)
        self.provider = None
        self._loaded_chunks = set()

    def set_provider(self, provider, total_rows=None) -> Any:
        """Register the data source rows are fetched from.

        :param provider: object/callable able to return a chunk of rows for a
            given range. The concrete protocol is TBD (see :meth:`_fetch_chunk`).
        :param total_rows: total number of rows the provider can serve; sizes
            the row count (and therefore the scrollbar) up front so the table
            geometry matches the full dataset before any chunk is fetched.
        """
        self.provider = provider
        if total_rows is not None:
            self.total_rows = total_rows
            self.setRowCount(self.total_rows)
        return self

    def _chunk_for_row(self, row) -> int:
        """Return the index of the chunk that contains ``row``."""
        return row // self.chunk_size if self.chunk_size else 0

    def _fetch_chunk(self, chunk_index) -> List[Any]:
        """Fetch a single chunk of rows from the provider.

        Expected (once implemented) to return the rows for the half-open range
        ``[chunk_index * chunk_size, (chunk_index + 1) * chunk_size)`` as a
        list of row lists, ready to splice into ``self._data``.

        STUB: no provider protocol is implemented yet.
        """
        raise NotImplementedError("NchantdLargeTable._fetch_chunk: provider protocol not implemented")

    def _ensure_rows_loaded(self, start, end) -> None:
        """Ensure every chunk spanning the half-open range ``[start, end)`` has
        been fetched into ``self._data`` before the inherited renderer builds
        those rows.

        No-op when no provider is registered, so the class behaves like a plain
        :class:`NchantdTable` over the in-memory ``self._data``.

        STUB: wiring only -- delegates to :meth:`_fetch_chunk` and records
        fetched chunks; splicing rows into ``self._data`` is left to the
        concrete implementation.
        """
        if self.provider is None or end <= start:
            return
        first_chunk = self._chunk_for_row(start)
        last_chunk = self._chunk_for_row(end - 1)
        for chunk_index in range(first_chunk, last_chunk + 1):
            if chunk_index in self._loaded_chunks:
                continue
            self._fetch_chunk(chunk_index)  # TODO: splice returned rows into self._data at their offset
            self._loaded_chunks.add(chunk_index)

    def _populate_visible_rows(self) -> None:
        """Fetch data for the viewport range, then render it via the inherited
        viewport-driven builder."""
        if self.provider is not None:
            buffer = self.lazy_buffer_rows
            first = self.rowAt(0)
            if first < 0:
                first = 0
            last = self.rowAt(self.viewport().height())
            if last < 0:
                last = min(self.rowCount() - 1, first + buffer)
            self._ensure_rows_loaded(max(0, first - buffer), min(self.rowCount(), last + 1 + buffer))
        super()._populate_visible_rows()


class NchantdDataFrameTable(NchantdWidgetMixin, qpandas.DataTableWidget):
    """A pandas-backed table widget."""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__()
        self.parent = parent
        self.config = kahndor.Instruct(PXCFG).select("NchantdDataFrameTable").override(parent.config).override(cfg)
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
        self.config.override(kahndor.Instruct(PXCFG).select("NchantdTableWidget").override(cfg))
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
        self.config.override(kahndor.Instruct(PXCFG).select("NchantdGrid").override(cfg))
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


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
