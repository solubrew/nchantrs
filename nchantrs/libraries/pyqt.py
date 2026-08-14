from PySide6.QtCore import Slot as Slot

try:
    from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlRelationalTableModel, QSqlTableModel
except ImportError:
    # QtSql is optional and removed in newer PySide6 builds.  Provide
    # ``None`` placeholders so imports of this module don't fail when
    # only the widget subset is in use.
    QSqlDatabase = None
    QSqlQuery = None
    QSqlQueryModel = None
    QSqlTableModel = None
    QSqlRelationalTableModel = None
try:
    from PySide6.QtWebEngineCore import qWebEngineChromiumVersion as qWebEngineChromiumVersion  # noqa: N816
except ImportError:
    qWebEngineChromiumVersion = None  # noqa: N816
