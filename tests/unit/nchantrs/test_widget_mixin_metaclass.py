"""Regression test for T-NEW-CRIT-PYS6PD-COMP metaclass fix.

Per ``TODO_CRIT_pyside6pandas_metaclass.md`` (nchantdoffice gamma):

The original ``class NchantdWidgetMixin(object):`` produced a metaclass
conflict when combined with Qt widgets via multiple inheritance:

    class NchantdDataFrameTable(NchantdWidgetMixin, qpandas.DataTableWidget):
        ...

qpandas.DataTableWidget uses Shiboken.ObjectType (PySide6's widget
metaclass), NchantdWidgetMixin used plain ``type`` (from object base).
Python 3.7+'s metaclass-conflict detector rejects this combination.

The user tried ``NchantdWidgetMixin(QObject)`` (commit 02ea57a) which
resolved the metaclass conflict but caused a segmentation fault at
runtime because Qt widgets require ``__init__(parent=...)`` cooperation
that the PyQt5-style cooperative MRO in nchantrs doesn't provide.

THIS fix:

``class NchantdWidgetMixin(object, metaclass=_NCHANTD_MIXIN_META):``
where ``_NCHANTD_MIXIN_META`` subclasses BOTH ``type(pyqt.QObject)`` AND
``type`` (plain Python metaclass). This satisfies Python's MRO check
WITHOUT introducing Qt runtime side-effects.

This test file does NOT use pytest fixtures because the root
``tests/conftest.py`` mocks ``kahndor``, ``squirl``, ``subtrix``,
``pycurity``, ``micromole``, AND ``pyqt`` (PySide6) with MagicMock —
which breaks ``type(QObject)`` when ``QObject`` itself gets mocked.

Run with::

    QT_QPA_PLATFORM=offscreen python -m pytest \\
        tests/unit/nchantrs/test_widget_mixin_metaclass.py \\
        --noconftest

The ``--noconftest`` flag bypasses the SB-stack mocking. Without it,
``pyqt.QObject`` becomes a MagicMock and ``type(QObject)`` raises
``TypeError: type.__new__() takes exactly 3 arguments (0 given)``.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Force offscreen Qt platform for headless tests
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# Add nchantrs root to path so we import the modified widgets.py
_PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))


def _reset_widgets_module():
    """Force fresh import of widgets.py (it caches _NCHANTD_MIXIN_META
    at module load)."""
    for mod in list(sys.modules):
        if mod.startswith("nchantrs.widgets.widgets"):
            del sys.modules[mod]


def test_mixin_metaclass_subclasses_both_type_and_qt():
    """NchantdWidgetMixin's metaclass must subclass BOTH plain ``type``
    AND ``type(pyqt.QObject)`` so it can coexist with Qt widgets
    in multiple inheritance without conflict."""
    import pytest

    try:
        import PySide6.QtCore  # noqa: F401
    except ImportError:
        pytest.skip("PySide6 not installed")

    _reset_widgets_module()
    from nchantrs.widgets.widgets import NchantdWidgetMixin

    Meta = type(NchantdWidgetMixin)
    assert issubclass(Meta, type), (
        f"NchantdWidgetMixin metaclass {Meta} must subclass plain type"
    )

    from PySide6.QtCore import QObject as _QtObject
    QtMeta = type(_QtObject)
    assert issubclass(Meta, QtMeta), (
        f"NchantdWidgetMixin metaclass {Meta} must subclass "
        f"PySide6's {QtMeta} so it can mix with Qt widgets"
    )


def test_mixin_combines_with_qtablewidget():
    """The originally-failing case: NchantdWidgetMixin + QTableWidget."""
    import pytest

    try:
        import PySide6.QtCore  # noqa: F401
    except ImportError:
        pytest.skip("PySide6 not installed")

    _reset_widgets_module()
    from PySide6.QtWidgets import QTableWidget

    from nchantrs.widgets.widgets import NchantdWidgetMixin

    # This used to raise TypeError: metaclass conflict
    cls = type(
        "NchantdDataFrameTableTest",
        (NchantdWidgetMixin, QTableWidget),
        {},
    )
    # Metaclass must be Qt's, so the derived class is a real Qt widget
    assert issubclass(type(cls), type(QTableWidget))


def test_mixin_combines_with_qlabel():
    """NchantdWidgetMixin + QLabel (a previously-working widget)."""
    import pytest

    try:
        import PySide6.QtCore  # noqa: F401
    except ImportError:
        pytest.skip("PySide6 not installed")

    _reset_widgets_module()
    from PySide6.QtWidgets import QLabel

    from nchantrs.widgets.widgets import NchantdWidgetMixin

    cls = type(
        "NchantdLabelTest",
        (NchantdWidgetMixin, QLabel),
        {},
    )
    assert issubclass(type(cls), type(QLabel))


def test_mixin_combines_with_other_qt_widgets():
    """All the other previously-working widgets must still mix."""
    import pytest

    try:
        import PySide6.QtCore  # noqa: F401
    except ImportError:
        pytest.skip("PySide6 not installed")

    _reset_widgets_module()
    from PySide6.QtWidgets import (
        QGroupBox,
        QProgressBar,
        QTabWidget,
        QTreeWidget,
    )

    from nchantrs.widgets.widgets import NchantdWidgetMixin

    for name, BaseCls in [
        ("TestTree", QTreeWidget),
        ("TestTabSet", QTabWidget),
        ("TestGroup", QGroupBox),
        ("TestProgressBar", QProgressBar),
    ]:
        cls = type(name, (NchantdWidgetMixin, BaseCls), {})
        assert issubclass(type(cls), type(BaseCls)), (
            f"{name} metaclass regression: {type(cls).__name__}"
        )


def test_mixin_combines_with_qpandas_datatablewidget():
    """The originally-failing case with bundled pyside6pandas.

    Skipped if pyside6pandas isn't installed locally — but in the
    self-contained .deb it always IS installed, so this case applies
    to the real failure scenario.
    """
    import pytest

    try:
        import PySide6.QtCore  # noqa: F401
    except ImportError:
        pytest.skip("PySide6 not installed")

    try:
        from pyside6pandas.views.DataTableView import DataTableWidget
    except ImportError as exc:
        pytest.skip(f"pyside6pandas not importable: {exc}")

    _reset_widgets_module()
    from nchantrs.widgets.widgets import NchantdWidgetMixin

    # This is the exact line from nchantrs/widgets/tables/tables.py:479
    # that triggered the original TypeError.
    cls = type(
        "NchantdDataFrameTable",
        (NchantdWidgetMixin, DataTableWidget),
        {},
    )
    # The derived class is a real Qt widget (Qt's metaclass)
    assert issubclass(type(cls), type(DataTableWidget))
