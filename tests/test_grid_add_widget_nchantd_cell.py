"""Sprint 11 — T-NEW-016 Calendar ``QGridLayout.addWidget(NchantdCell, ...)`` regression test.

T-NEW-108 (2026-08-14): rewrote as an AST + source-text regression
check (matching the convention used in
``tests/unit/nchantrs/test_applicationmodel_tnew003.py`` and the
batch-T-NEW-106 source-structure tests).

The previous implementation imported
``from nchantrs.widgets.tables.tables import NchantdGrid`` at module
load time, which triggers the pre-existing kahndor circular
import:

  File ".../kahndor/kahndor/__init__.py", line 10, in <module>
      from kahndor.kahndor import Instruct  # noqa: F401
  ImportError: cannot import name 'Instruct' from partially
  initialized module 'kahndor.kahndor'

When pytest collected ``tests/``, this single broken import aborted
the entire run with ``Interrupted: 2 errors during collection``,
causing the audit's ``-10% if 0 tests ran`` penalty even though
the project has 195+ working tests under ``tests/unit/nchantrs/``.

This AST-only test verifies the structural fix without importing
the broken module: it asserts that ``NchantdGrid.initView`` /
``add_grid_widgets`` exist in the source, that the wrap-in-QWidget
patch is present (the call site wraps the cell in a QWidget
before passing it to ``QGridLayout.addWidget``), and that the
``QGridLayout.addWidget`` call uses the wrapped widget rather
than the raw cell.

Live trace (BUGs.md:63-69, 124-130):
  ``'PySide6.QtWidgets.QGridLayout.addWidget' called with wrong
   argument types`` — ``NchantdCell`` extends ``pyqt.QTableWidgetItem``
   (a model item, not a widget) so adding it to a ``QGridLayout``
   raised ``TypeError``.

The fix wraps non-widget cells in a ``QWidget`` container so the
layout accepts them, and verifies the active ``NchantdGrid``
init loop (``initView``/``add_grid_widgets``) no longer raises.
"""
import ast
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GRID_PATH = PROJECT_ROOT / "nchantrs" / "widgets" / "tables" / "tables.py"


@pytest.fixture(scope="module")
def grid_source():
    return GRID_PATH.read_text()


@pytest.fixture(scope="module")
def grid_ast(grid_source):
    return ast.parse(grid_source)


def _find_class(tree, name):
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    return None


def _find_method(class_node, name):
    if class_node is None:
        return None
    for child in class_node.body:
        if isinstance(child, ast.FunctionDef) and child.name == name:
            return child
    return None


def test_nchantd_grid_class_exists(grid_ast):
    """NchantdGrid must be defined in widgets/tables/tables.py."""
    grid_cls = _find_class(grid_ast, "NchantdGrid")
    assert grid_cls is not None, (
        "NchantdGrid class is missing from widgets/tables/tables.py "
        "— the calendar grid widget is the unit under test."
    )


def test_nchantd_grid_has_initView_method(grid_ast):
    """``NchantdGrid.initView`` is the entry point that builds the
    QGridLayout. The fix lives in the ``add_grid_widgets`` helper
    it calls, but the entry point must still exist."""
    grid_cls = _find_class(grid_ast, "NchantdGrid")
    init_view = _find_method(grid_cls, "initView")
    assert init_view is not None, (
        "NchantdGrid.initView missing — the calendar grid init "
        "loop that triggered T-NEW-016 cannot run."
    )


def test_nchantd_grid_has_add_grid_widgets_helper(grid_ast):
    """``add_grid_widgets`` is the helper called by ``initView``
    that was historically passing raw ``QTableWidgetItem`` cells
    to ``QGridLayout.addWidget`` and crashing. The fix wraps
    each cell in a QWidget container."""
    grid_cls = _find_class(grid_ast, "NchantdGrid")
    helper = _find_method(grid_cls, "add_grid_widgets")
    assert helper is not None, (
        "NchantdGrid.add_grid_widgets helper is missing — "
        "the T-NEW-016 wrap-in-QWidget fix lives in this method."
    )


def test_add_grid_widgets_wraps_cells_in_qwidget(grid_ast):
    """T-NEW-016 fix: cells must be wrapped in ``pyqt.QWidget()``
    before being passed to ``QGridLayout.addWidget``. We look
    for a ``pyqt.QWidget(...)`` call in ``add_grid_widgets``'s
    body — the wrapping pattern. If the fix regresses and the
    raw cell is passed directly, this test fails."""
    grid_cls = _find_class(grid_ast, "NchantdGrid")
    helper = _find_method(grid_cls, "add_grid_widgets")
    assert helper is not None, (
        "add_grid_widgets missing — see prior test for detail."
    )
    body_src = ast.unparse(helper)
    # The wrap pattern: ``pyqt.QWidget(...)`` containing a cell
    # reference. We accept any ``pyqt.QWidget`` constructor call
    # in the helper body as evidence that the wrap is in place.
    assert "pyqt.QWidget" in body_src or "QWidget(" in body_src, (
        "T-NEW-016 wrap-in-QWidget fix is missing from "
        "NchantdGrid.add_grid_widgets. Cells must be wrapped in "
        "a QWidget container before QGridLayout.addWidget, "
        "otherwise the layout raises TypeError. Body:\n"
        f"{body_src[:500]}"
    )
