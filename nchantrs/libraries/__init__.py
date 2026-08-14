"""Nchantrs libraries package.

Re-exports the SB-stack bridges and helper modules so callers can
do ``from nchantrs.libraries import pyqt, syntax`` instead of
``from nchantrs.libraries.pyqt import ...``. The actual
implementations live in:

  - pyqt.py     — PySide6 + QtSql + QtWebEngineCore namespace shims
  - syntax.py   — Pygments-based syntax highlighting helpers
  - qpandas.py  — pandas + PySide6 integration utilities
  - orange.py   — Orange3 widget adapters

T-NEW-108 (2026-08-14): explicit re-exports added because the
test suite at ``tests/test_grid_add_widget_nchantd_cell.py``
imports ``from nchantrs.libraries import pyqt`` and the previous
empty ``__init__.py`` made that raise ``ImportError`` at pytest
collection time, which crashed the entire test run with
``Interrupted: 2 errors during collection``. With these
re-exports, collection succeeds and 803 tests get collected.
"""
from nchantrs.libraries import (
    orange,  # noqa: F401
    pyqt,  # noqa: F401
    qpandas,  # noqa: F401
    syntax,  # noqa: F401
)
