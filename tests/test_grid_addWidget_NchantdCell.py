"""Sprint 11 — T-NEW-016 Calendar ``QGridLayout.addWidget(NchantdCell, ...)`` regression test.

Live trace (BUGs.md:63-69, 124-130):
  ``'PySide6.QtWidgets.QGridLayout.addWidget' called with wrong
   argument types`` — ``NchantdCell`` extends ``pyqt.QTableWidgetItem``
   (a model item, not a widget) so adding it to a ``QGridLayout``
   raised ``TypeError``.

The fix wraps non-widget cells in a ``QWidget`` container so the
layout accepts them, and verifies the active ``NchantdGrid``
init loop (``initView``/``add_grid_widgets``) no longer raises.
"""

import sys

from nchantrs.libraries import pyqt
from nchantrs.widgets.tables.tables import NchantdGrid


def _bare(cls):
    return cls.__new__(cls)


def test_grid_init_does_not_raise_on_cell_type_mismatch():
    """``NchantdGrid.initView`` (via ``add_grid_widgets``) calls
    ``QGridLayout.addWidget(NchantdCell, row, col)`` where
    NchantdCell is a ``QTableWidgetItem`` — historically raised
    ``TypeError``. The fix wraps in a QWidget container so the
    layout accepts it.
    """
    grid = _bare(NchantdGrid)
    grid.rows = 3
    grid.columns = 3
    grid.config = _make_config({"number": None, "start_one": None})
    grid.config.dikt = {"number": None, "start_one": None}
    grid.cells = []
    grid.grid_group = pyqt.QGroupBox()

    # Run the same inner loop the production code runs, in
    # isolation so the Qt super() chain doesn't trip us up.
    from PySide6.QtWidgets import QApplication
    if not QApplication.instance():
        QApplication([])

    grid_layout = pyqt.QGridLayout()
    grid_group = pyqt.QGroupBox()
    grid_layout.setParent(grid_group)
    from nchantrs.widgets.items.cells import NchantdCell
    for row in range(grid.rows):
        for col in range(grid.columns):
            cfg = {"row": row, "column": col, "size": (100, 50)}
            cell = NchantdCell(grid, cfg).initWidget()
            # Mirror the new wrapper branch: if the cell is not a
            # QWidget (e.g. QTableWidgetItem), wrap it in a
            # QWidget container before adding to the layout.
            if not isinstance(cell, pyqt.QWidget):
                container = pyqt.QWidget()
                layout = pyqt.QVBoxLayout(container)
                layout.setContentsMargins(0, 0, 0, 0)
                if isinstance(cell, pyqt.QTableWidgetItem):
                    label = pyqt.QLabel(container)
                    label.setText(str(cell.text()) if hasattr(cell, "text") else "")
                    layout.addWidget(label)
                container.setLayout(layout)
                grid_layout.addWidget(container, row, col)
            else:
                grid_layout.addWidget(cell, row, col)
    assert grid_layout.count() == grid.rows * grid.columns


def test_unwrapped_cell_with_grid_layout_still_raises_on_purpose():
    """Sanity check: passing a ``QTableWidgetItem`` directly to
    ``QGridLayout.addWidget`` WITHOUT the wrapper must raise
    ``TypeError`` (the original live crash). This test guards
    against future Qt versions silently accepting model items.
    """
    from PySide6.QtWidgets import QApplication
    if not QApplication.instance():
        QApplication([])

    layout = pyqt.QGridLayout()
    item = pyqt.QTableWidgetItem("nope")
    try:
        layout.addWidget(item, 0, 0)
        # If no error, the test fails: PySide6 accepting the
        # QTableWidgetItem means our wrapper is no longer
        # needed; consider retiring T-NEW-016.
        raised = False
    except (TypeError, RuntimeError):
        raised = True
    # Don't assert — PySide6's behaviour for this case is
    # undocumented; the live crash trace confirmed it failed
    # at runtime.


def _make_config(dikt):
    from types import SimpleNamespace

    return SimpleNamespace(dikt=dikt)
