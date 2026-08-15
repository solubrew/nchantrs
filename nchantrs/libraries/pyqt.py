import logging
from typing import Any, Dict, List, Optional, Tuple

from PySide6.QtCore import (
    QAbstractItemModel,
    QAbstractListModel,
    QAbstractTableModel,
    QBuffer,
    QByteArray,
    QDate,
    QDir,
    QEvent,
    QIODevice,
    QMetaObject,
    QMimeData,
    QModelIndex,
    QObject,
    QPoint,
    QPointF,
    QProcess,
    QProcessEnvironment,
    QRectF,
    QSettings,
    QSize,
    QSocketNotifier,
    QStandardPaths,
    Qt,
    QThread,
    QThreadPool,
    QTimer,
    QUrl,
    Signal,
    qInstallMessageHandler,
)
from PySide6.QtCore import (
    Slot as Slot,
)

# ===============================================================================||
from PySide6.QtGui import (
    QAction,
    QBrush,
    QCloseEvent,
    QColor,
    QColorTransform,
    QCursor,
    QDoubleValidator,
    QDrag,
    QDragEnterEvent,
    QDragMoveEvent,
    QDropEvent,
    QFont,
    QFontDatabase,
    QFontMetrics,
    QGuiApplication,
    QHoverEvent,
    QIcon,
    QImage,
    QIntValidator,
    QKeySequence,
    QMouseEvent,
    QMoveEvent,
    QMovie,
    QPainter,
    QPainterPath,
    QPainterPathStroker,
    QPen,
    QPixmap,
    QPolygonF,
    QResizeEvent,
    QShortcut,
    QStandardItem,
    QStandardItemModel,
    QSyntaxHighlighter,
    QTextCharFormat,
    QTextCursor,
    QTextFrame,
    QTextFrameFormat,
    QTextLength,
    QTextListFormat,
    QTextOption,
    QTextTableFormat,
    QTransform,
    QWheelEvent,
)

# ===============================================================================||
from PySide6.QtNetwork import QSslSocket
from PySide6.QtPdf import QPdfDocument

# ===============================================================================||
from PySide6.QtPdfWidgets import QPdfView

# ===============================================================================||
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlRelationalTableModel, QSqlTableModel
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import (
    QWebEngineCertificateError,
    QWebEngineClientCertificateSelection,
    QWebEngineClientCertificateStore,
    QWebEngineClientHints,
    QWebEngineCookieStore,
    QWebEngineDownloadRequest,
    QWebEngineFileSystemAccessRequest,
    QWebEngineFrame,
    QWebEngineHistory,
    QWebEnginePage,
    QWebEnginePermission,
    QWebEngineProfile,
    QWebEngineScript,
    QWebEngineSettings,
    QWebEngineUrlRequestInfo,
    QWebEngineUrlRequestInterceptor,
)

# ===============================================================================||
from PySide6.QtWebEngineWidgets import QWebEngineView

# ===============================================================================||
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QBoxLayout,
    QCalendarWidget,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFileDialog,
    QFileSystemModel,
    QFontDialog,
    QFrame,
    QGraphicsEllipseItem,
    QGraphicsLineItem,
    QGraphicsPathItem,
    QGraphicsPixmapItem,
    QGraphicsPolygonItem,
    QGraphicsProxyWidget,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsSimpleTextItem,
    QGraphicsTextItem,
    QGraphicsView,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLayout,
    QLineEdit,
    QListView,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMenuBar,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QSpinBox,
    QSplitter,
    QStackedLayout,
    QStackedWidget,
    QStatusBar,
    QStyle,
    QStyledItemDelegate,
    QStyleFactory,
    QStyleOptionButton,
    QStyleOptionComboBox,
    QStyleOptionViewItem,
    QTableView,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextBrowser,
    QTextEdit,
    QTimeEdit,
    QToolBar,
    QToolBox,
    QToolButton,
    QTreeView,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
    QWizard,
    QWizardPage,
)

# ===============================================================================||
# from PyQt5.QtMultimedia import (
#     QMediaContent,
#     QMediaPlayer,
#     QAudioOutput,
#     QAudioDeviceInfo,
#     QAudio,
#     QAudioInputSelectorControl,
# )
# from PyQt5.QtMultimediaWidgets import QVideoWidget

# ===============================================================================||
# from PySide6.Qsci import QsciScintillaBase
# from AnyQt.QtCore import Qt, QRectF, QSizeF, QPointF, QLineF
# from AnyQt.QtGui import QColor, QBrush, QPen
# from AnyQt.QtWidgets import (
#     QGraphicsWidget,
#     QGraphicsRectItem,
#     QGraphicsLinearLayout,
#     QSizePolicy,
#     QGraphicsLineItem,
# )
#
