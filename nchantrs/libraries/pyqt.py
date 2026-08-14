"""PySide6 + QtSql + QtWebEngineCore namespace shim.

The project writes ``from nchantrs.libraries import pyqt`` and then
``pyqt.QWidget()`` etc. — so this module has to expose every Qt
class the codebase touches. The original implementation only
exported a handful of names (``Slot``, ``QSql*``,
``qWebEngineChromiumVersion``), which made ``pyqt.QColor``,
``pyqt.QTextCharFormat``, ``pyqt.QSyntaxHighlighter``, etc. raise
``AttributeError`` and crash pytest collection.

T-NEW-108 (2026-08-14): comprehensive PySide6 re-export so any
``pyqt.<QtClass>`` reference resolves. We pull from
``PySide6.QtCore``, ``PySide6.QtGui``, ``PySide6.QtWidgets``, and
the optional ``PySide6.QtSql`` / ``PySide6.QtWebEngineCore``
modules. The exact list of Qt classes used across the project is
discovered via ``dir()`` on the relevant submodules — anything not
exported here would have been a pre-existing runtime bug too, so
this list is conservative.

Optional imports (QtSql, QtWebEngineCore) use try/except so the
module still loads when those PySide6 extras are missing — they
fall back to ``None`` placeholders. This mirrors the legacy
behaviour: tests can ``import pyqt`` even on a minimal PySide6
install, and references to the missing classes fail at the call
site rather than at module import time.
"""
from PySide6 import QtCore
from PySide6 import QtGui as _QtGui
from PySide6 import QtWidgets as _QtWidgets

# Re-export every name from these three submodules under ``pyqt.``.
# We use ``dir()`` instead of an explicit list so adding a new
# Qt class to PySide6 automatically makes it available here.
for _mod in (QtCore, _QtGui, _QtWidgets):
    for _name in dir(_mod):
        if _name.startswith("_"):
            continue
        # Only set if not already defined (so our optional fallbacks
        # below aren't overwritten by ``None`` slots in PySide6).
        if _name not in globals():
            globals()[_name] = getattr(_mod, _name)

# Convenience aliases for names that PySide6 exposes under a
# different casing (the project uses mixed-case Qt names).
Qpyqt = QtCore

# Optional: QtSql (removed in some PySide6 builds). Fall back to
# ``None`` placeholders so import-time references survive; only
# actual usage at call time raises AttributeError.
try:
    from PySide6.QtSql import (
        QSqlDatabase,
        QSqlQuery,
        QSqlQueryModel,
        QSqlRelationalTableModel,
        QSqlTableModel,
    )
except ImportError:
    QSqlDatabase = None
    QSqlQuery = None
    QSqlQueryModel = None
    QSqlTableModel = None
    QSqlRelationalTableModel = None

# Optional: QtWebEngineCore (not always installed). The PySide6
# API name uses camelCase (``qWebEngineChromiumVersion``) which
# triggers N816 if we don't alias it.
try:
    from PySide6.QtWebEngineCore import (
        qWebEngineChromiumVersion as qWebEngineChromiumVersion,
    )  # noqa: N816
except ImportError:
    qWebEngineChromiumVersion = None  # noqa: N816
