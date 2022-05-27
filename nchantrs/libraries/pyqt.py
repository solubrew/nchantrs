try:
	fail #this ensures fail over to PyQT5
#===============================================================================||
	from PySide2.QtCore import Signal, QAbstractListModel, QDir, Qt#		||
#===============================================================================||
	from PySide2.QtGui import QIcon, QFont
#===============================================================================||
	from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QToolButton
	from PySide2.QtWidgets import QApplication, QComboBox, QDialog, QFileDialog, QFrame#	||
	from PySide2.QtWidgets import QGridLayout, QLabel, QListView, QLabel#		||
	from PySide2.QtWidgets import QLineEdit, QMenu, QMenuBar, QPushButton#	||
	from PySide2.QtWidgets import QTextBrowser, QScrollArea, QSizePolicy, QProgressBar#	||
	from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QTextEdit, QGroupBox
#===============================================================================||
except:
	print('PySide2 Import Failed')
#===============================================================================||
	from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot, QAbstractListModel, QAbstractItemModel#||
	from PyQt5.QtCore import QModelIndex, QDir, QDate, Qt, QSettings, QTimer, QUrl#						||
#===============================================================================||
	from PyQt5.QtGui import QIcon, QFont, QPixmap, QStandardItemModel, QImage, QPainter
	from PyQt5.QtGui import QTextTableFormat, QStandardItem
	from PyQt5.QtGui import QColor, QFont, QTextCharFormat, QTextLength, QDoubleValidator, QIntValidator
#===============================================================================||
	from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
	from PyQt5.QtSql import QSqlTableModel, QSqlRelationalTableModel
#===============================================================================||
	from PyQt5.QtWebEngineWidgets import QWebEngineView
#===============================================================================||
	from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QToolButton, QDateTimeEdit
	from PyQt5.QtWidgets import QApplication, QComboBox, QDialog, QFileDialog, QFrame#	||
	from PyQt5.QtWidgets import QGridLayout, QLabel, QLayout, QListView, QLabel#		||
	from PyQt5.QtWidgets import QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox#	||
	from PyQt5.QtWidgets import QTextBrowser, QScrollArea, QSizePolicy, QProgressBar, QFileSystemModel#	||
	from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QTableWidget, QTextEdit, QGroupBox, QTableView, QTreeView
	from PyQt5.QtWidgets import QBoxLayout, QCalendarWidget, QCheckBox, QRadioButton, QSlider
#===============================================================================||
	from PyQt5.Qsci import QsciScintillaBase
#===============================================================================||
	#from PyQt5.QtPrintSupport


	# if QT_VERSION < 0x40700:
	# 	# Qt 4.6 does not yet have placeholder text
	# 	def setPlaceholderText(self, text):
	# 		self.__placeholderText = text
	# 		self.update()
	# 	def placeholderText(self):
	# 		try:
	# 			return self.__placeholderText
	# 		except AttributeError:
	# 			return ""
	# 	def paintEvent(self, event):
	# 		QLineEdit.paintEvent(self, event)
	# 		if not self.text() and self.placeholderText() and \
	# 				not self.hasFocus():
	# 			p = QStylePainter(self)
	# 			font = self.font()
	# 			metrics = QFontMetrics(font)
	# 			p.setFont(font)
	# 			color = self.palette().color(QPalette.Mid)
	# 			p.setPen(color)
	# 			left, top, right, bottom = self.getTextMargins()
	# 			contents = self.contentsRect()
	# 			contents = contents.adjusted(left, top, -right, -bottom)
	# 			text = metrics.elidedText(self.placeholderText(),
	# 									  Qt.ElideMiddle,
	# 									  contents.width())
	# 			p.drawText(contents, Qt.AlignLeft | Qt.AlignVCenter, text)
