
#!/usr/bin/env python
#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##	 notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##	 notice, this list of conditions and the following disclaimer in
##	 the documentation and/or other materials provided with the
##	 distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##	 the names of its contributors may be used to endorse or promote
##	 products derived from this software without specific prior written
##	 permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################
import sys
from PyQt5.QtCore import (QByteArray, QDate, QDateTime, QEvent, QPoint, QRect,
		QRegExp, QSettings, QSize, Qt, QTime, QTimer)
from PyQt5.QtGui import QColor, QIcon, QRegExpValidator, QValidator
from PyQt5.QtWidgets import (QAbstractItemView, QAction, QApplication,
		QComboBox, QDialog, QDialogButtonBox, QFileDialog, QGridLayout,
		QGroupBox, QHeaderView, QInputDialog, QItemDelegate, QLabel, QLineEdit,
		QMainWindow, QMessageBox, QStyle, QStyleOptionViewItem, QTableWidget,
		QTableWidgetItem, QTreeWidget, QTreeWidgetItem, QVBoxLayout)
class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.settingsTree = SettingsTree()
		self.setCentralWidget(self.settingsTree)
		self.locationDialog = None
		self.createActions()
		self.createMenus()
		self.autoRefreshAct.setChecked(True)
		self.fallbacksAct.setChecked(True)
		self.setWindowTitle("Settings Editor")
		self.resize(500, 600)
	def openSettings(self):
		if self.locationDialog is None:
			self.locationDialog = LocationDialog(self)
		if self.locationDialog.exec_():
			settings = QSettings(self.locationDialog.format(),
										self.locationDialog.scope(),
										self.locationDialog.organization(),
										self.locationDialog.application())
			self.setSettingsObject(settings)
			self.fallbacksAct.setEnabled(True)
	def openIniFile(self):
		fileName, _ = QFileDialog.getOpenFileName(self, "Open INI File", '',
				"INI Files (*.ini *.conf)")
		if fileName:
			settings = QSettings(fileName, QSettings.IniFormat)
			self.setSettingsObject(settings)
			self.fallbacksAct.setEnabled(False)
	def openPropertyList(self):
		fileName, _ = QFileDialog.getOpenFileName(self, "Open Property List",
				'', "Property List Files (*.plist)")
		if fileName:
			settings = QSettings(fileName, QSettings.NativeFormat)
			self.setSettingsObject(settings)
			self.fallbacksAct.setEnabled(False)
	def openRegistryPath(self):
		path, ok = QInputDialog.getText(self, "Open Registry Path",
				"Enter the path in the Windows registry:", QLineEdit.Normal,
				'HKEY_CURRENT_USER\\')
		if ok and path != '':
			settings = QSettings(path, QSettings.NativeFormat)
			self.setSettingsObject(settings)
			self.fallbacksAct.setEnabled(False)
	def about(self):
		QMessageBox.about(self, "About Settings Editor",
				"The <b>Settings Editor</b> example shows how to access "
				"application settings using Qt.")
	def createActions(self):
		self.openSettingsAct = QAction("&Open Application Settings...", self,
				shortcut="Ctrl+O", triggered=self.openSettings)
		self.openIniFileAct = QAction("Open I&NI File...", self,
				shortcut="Ctrl+N", triggered=self.openIniFile)
		self.openPropertyListAct = QAction("Open Mac &Property List...", self,
				shortcut="Ctrl+P", triggered=self.openPropertyList)
		if sys.platform != 'darwin':
			self.openPropertyListAct.setEnabled(False)
		self.openRegistryPathAct = QAction("Open Windows &Registry Path...",
				self, shortcut="Ctrl+G", triggered=self.openRegistryPath)
		if sys.platform != 'win32':
			self.openRegistryPathAct.setEnabled(False)
		self.refreshAct = QAction("&Refresh", self, shortcut="Ctrl+R",
				enabled=False, triggered=self.settingsTree.refresh)
		self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
				triggered=self.close)
		self.autoRefreshAct = QAction("&Auto-Refresh", self, shortcut="Ctrl+A",
				checkable=True, enabled=False)
		self.autoRefreshAct.triggered.connect(self.settingsTree.setAutoRefresh)
		self.autoRefreshAct.triggered.connect(self.refreshAct.setDisabled)
		self.fallbacksAct = QAction("&Fallbacks", self, shortcut="Ctrl+F",
				checkable=True, enabled=False,
				triggered=self.settingsTree.setFallbacksEnabled)
		self.aboutAct = QAction("&About", self, triggered=self.about)
		self.aboutQtAct = QAction("About &Qt", self,
				triggered=QApplication.instance().aboutQt)
	def createMenus(self):
		self.fileMenu = self.menuBar().addMenu("&File")
		self.fileMenu.addAction(self.openSettingsAct)
		self.fileMenu.addAction(self.openIniFileAct)
		self.fileMenu.addAction(self.openPropertyListAct)
		self.fileMenu.addAction(self.openRegistryPathAct)
		self.fileMenu.addSeparator()
		self.fileMenu.addAction(self.refreshAct)
		self.fileMenu.addSeparator()
		self.fileMenu.addAction(self.exitAct)
		self.optionsMenu = self.menuBar().addMenu("&Options")
		self.optionsMenu.addAction(self.autoRefreshAct)
		self.optionsMenu.addAction(self.fallbacksAct)
		self.menuBar().addSeparator()
		self.helpMenu = self.menuBar().addMenu("&Help")
		self.helpMenu.addAction(self.aboutAct)
		self.helpMenu.addAction(self.aboutQtAct)
	def setSettingsObject(self, settings):
		settings.setFallbacksEnabled(self.fallbacksAct.isChecked())
		self.settingsTree.setSettingsObject(settings)
		self.refreshAct.setEnabled(True)
		self.autoRefreshAct.setEnabled(True)
		niceName = settings.fileName()
		niceName.replace('\\', '/')
		niceName = niceName.split('/')[-1]
		if not settings.isWritable():
			niceName += " (read only)"
		self.setWindowTitle("%s - Settings Editor" % niceName)
class LocationDialog(QDialog):
	def __init__(self, parent=None):
		super(LocationDialog, self).__init__(parent)
		self.formatComboBox = QComboBox()
		self.formatComboBox.addItem("Native")
		self.formatComboBox.addItem("INI")
		self.scopeComboBox = QComboBox()
		self.scopeComboBox.addItem("User")
		self.scopeComboBox.addItem("System")
		self.organizationComboBox = QComboBox()
		self.organizationComboBox.addItem("Trolltech")
		self.organizationComboBox.setEditable(True)
		self.applicationComboBox = QComboBox()
		self.applicationComboBox.addItem("Any")
		self.applicationComboBox.addItem("Application Example")
		self.applicationComboBox.addItem("Assistant")
		self.applicationComboBox.addItem("Designer")
		self.applicationComboBox.addItem("Linguist")
		self.applicationComboBox.setEditable(True)
		self.applicationComboBox.setCurrentIndex(3)
		formatLabel = QLabel("&Format:")
		formatLabel.setBuddy(self.formatComboBox)
		scopeLabel = QLabel("&Scope:")
		scopeLabel.setBuddy(self.scopeComboBox)
		organizationLabel = QLabel("&Organization:")
		organizationLabel.setBuddy(self.organizationComboBox)
		applicationLabel = QLabel("&Application:")
		applicationLabel.setBuddy(self.applicationComboBox)
		self.locationsGroupBox = QGroupBox("Setting Locations")
		self.locationsTable = QTableWidget()
		self.locationsTable.setSelectionMode(QAbstractItemView.SingleSelection)
		self.locationsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.locationsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.locationsTable.setColumnCount(2)
		self.locationsTable.setHorizontalHeaderLabels(("Location", "Access"))
		self.locationsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		self.locationsTable.horizontalHeader().resizeSection(1, 180)
		self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		self.formatComboBox.activated.connect(self.updateLocationsTable)
		self.scopeComboBox.activated.connect(self.updateLocationsTable)
		self.organizationComboBox.lineEdit().editingFinished.connect(self.updateLocationsTable)
		self.applicationComboBox.lineEdit().editingFinished.connect(self.updateLocationsTable)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
		locationsLayout = QVBoxLayout()
		locationsLayout.addWidget(self.locationsTable)
		self.locationsGroupBox.setLayout(locationsLayout)
		mainLayout = QGridLayout()
		mainLayout.addWidget(formatLabel, 0, 0)
		mainLayout.addWidget(self.formatComboBox, 0, 1)
		mainLayout.addWidget(scopeLabel, 1, 0)
		mainLayout.addWidget(self.scopeComboBox, 1, 1)
		mainLayout.addWidget(organizationLabel, 2, 0)
		mainLayout.addWidget(self.organizationComboBox, 2, 1)
		mainLayout.addWidget(applicationLabel, 3, 0)
		mainLayout.addWidget(self.applicationComboBox, 3, 1)
		mainLayout.addWidget(self.locationsGroupBox, 4, 0, 1, 2)
		mainLayout.addWidget(self.buttonBox, 5, 0, 1, 2)
		self.setLayout(mainLayout)
		self.updateLocationsTable()
		self.setWindowTitle("Open Application Settings")
		self.resize(650, 400)
	def format(self):
		if self.formatComboBox.currentIndex() == 0:
			return QSettings.NativeFormat
		else:
			return QSettings.IniFormat
	def scope(self):
		if self.scopeComboBox.currentIndex() == 0:
			return QSettings.UserScope
		else:
			return QSettings.SystemScope
	def organization(self):
		return self.organizationComboBox.currentText()
	def application(self):
		if self.applicationComboBox.currentText() == "Any":
			return ''
		return self.applicationComboBox.currentText()
	def updateLocationsTable(self):
		self.locationsTable.setUpdatesEnabled(False)
		self.locationsTable.setRowCount(0)
		for i in range(2):
			if i == 0:
				if self.scope() == QSettings.SystemScope:
					continue
				actualScope = QSettings.UserScope
			else:
				actualScope = QSettings.SystemScope
			for j in range(2):
				if j == 0:
					if not self.application():
						continue
					actualApplication = self.application()
				else:
					actualApplication = ''
				settings = QSettings(self.format(), actualScope,
						self.organization(), actualApplication)
				row = self.locationsTable.rowCount()
				self.locationsTable.setRowCount(row + 1)
				item0 = QTableWidgetItem()
				item0.setText(settings.fileName())
				item1 = QTableWidgetItem()
				disable = not (settings.childKeys() or settings.childGroups())
				if row == 0:
					if settings.isWritable():
						item1.setText("Read-write")
						disable = False
					else:
						item1.setText("Read-only")
					self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(disable)
				else:
					item1.setText("Read-only fallback")
				if disable:
					item0.setFlags(item0.flags() & ~Qt.ItemIsEnabled)
					item1.setFlags(item1.flags() & ~Qt.ItemIsEnabled)
				self.locationsTable.setItem(row, 0, item0)
				self.locationsTable.setItem(row, 1, item1)
		self.locationsTable.setUpdatesEnabled(True)
class SettingsTree(QTreeWidget):
	def __init__(self, parent=None):
		super(SettingsTree, self).__init__(parent)
		self.setItemDelegate(VariantDelegate(self))
		self.setHeaderLabels(("Setting", "Type", "Value"))
		self.header().setSectionResizeMode(0, QHeaderView.Stretch)
		self.header().setSectionResizeMode(2, QHeaderView.Stretch)
		self.settings = None
		self.refreshTimer = QTimer()
		self.refreshTimer.setInterval(2000)
		self.autoRefresh = False
		self.groupIcon = QIcon()
		self.groupIcon.addPixmap(self.style().standardPixmap(QStyle.SP_DirClosedIcon),
				QIcon.Normal, QIcon.Off)
		self.groupIcon.addPixmap(self.style().standardPixmap(QStyle.SP_DirOpenIcon),
				QIcon.Normal, QIcon.On)
		self.keyIcon = QIcon()
		self.keyIcon.addPixmap(self.style().standardPixmap(QStyle.SP_FileIcon))
		self.refreshTimer.timeout.connect(self.maybeRefresh)
	def setSettingsObject(self, settings):
		self.settings = settings
		self.clear()
		if self.settings is not None:
			self.settings.setParent(self)
			self.refresh()
			if self.autoRefresh:
				self.refreshTimer.start()
		else:
			self.refreshTimer.stop()
	def sizeHint(self):
		return QSize(800, 600)
	def setAutoRefresh(self, autoRefresh):
		self.autoRefresh = autoRefresh
		if self.settings is not None:
			if self.autoRefresh:
				self.maybeRefresh()
				self.refreshTimer.start()
			else:
				self.refreshTimer.stop()
	def setFallbacksEnabled(self, enabled):
		if self.settings is not None:
			self.settings.setFallbacksEnabled(enabled)
			self.refresh()
	def maybeRefresh(self):
		if self.state() != QAbstractItemView.EditingState:
			self.refresh()
	def refresh(self):
		if self.settings is None:
			return
		# The signal might not be connected.
		try:
			self.itemChanged.disconnect(self.updateSetting)
		except:
			pass
		self.settings.sync()
		self.updateChildItems(None)
		self.itemChanged.connect(self.updateSetting)
	def event(self, event):
		if event.type() == QEvent.WindowActivate:
			if self.isActiveWindow() and self.autoRefresh:
				self.maybeRefresh()
		return super(SettingsTree, self).event(event)
	def updateSetting(self, item):
		key = item.text(0)
		ancestor = item.parent()
		while ancestor:
			key = ancestor.text(0) + '/' + key
			ancestor = ancestor.parent()
		d = item.data(2, Qt.UserRole)
		self.settings.setValue(key, item.data(2, Qt.UserRole))
		if self.autoRefresh:
			self.refresh()
	def updateChildItems(self, parent):
		dividerIndex = 0
		for group in self.settings.childGroups():
			childIndex = self.findChild(parent, group, dividerIndex)
			if childIndex != -1:
				child = self.childAt(parent, childIndex)
				child.setText(1, '')
				child.setText(2, '')
				child.setData(2, Qt.UserRole, None)
				self.moveItemForward(parent, childIndex, dividerIndex)
			else:
				child = self.createItem(group, parent, dividerIndex)
			child.setIcon(0, self.groupIcon)
			dividerIndex += 1
			self.settings.beginGroup(group)
			self.updateChildItems(child)
			self.settings.endGroup()
		for key in self.settings.childKeys():
			childIndex = self.findChild(parent, key, 0)
			if childIndex == -1 or childIndex >= dividerIndex:
				if childIndex != -1:
					child = self.childAt(parent, childIndex)
					for i in range(child.childCount()):
						self.deleteItem(child, i)
					self.moveItemForward(parent, childIndex, dividerIndex)
				else:
					child = self.createItem(key, parent, dividerIndex)
				child.setIcon(0, self.keyIcon)
				dividerIndex += 1
			else:
				child = self.childAt(parent, childIndex)
			value = self.settings.value(key)
			if value is None:
				child.setText(1, 'Invalid')
			else:
				child.setText(1, value.__class__.__name__)
			child.setText(2, VariantDelegate.displayText(value))
			child.setData(2, Qt.UserRole, value)
		while dividerIndex < self.childCount(parent):
			self.deleteItem(parent, dividerIndex)
	def createItem(self, text, parent, index):
		after = None
		if index != 0:
			after = self.childAt(parent, index - 1)
		if parent is not None:
			item = QTreeWidgetItem(parent, after)
		else:
			item = QTreeWidgetItem(self, after)
		item.setText(0, text)
		item.setFlags(item.flags() | Qt.ItemIsEditable)
		return item
	def deleteItem(self, parent, index):
		if parent is not None:
			item = parent.takeChild(index)
		else:
			item = self.takeTopLevelItem(index)
		del item
	def childAt(self, parent, index):
		if parent is not None:
			return parent.child(index)
		else:
			return self.topLevelItem(index)
	def childCount(self, parent):
		if parent is not None:
			return parent.childCount()
		else:
			return self.topLevelItemCount()
	def findChild(self, parent, text, startIndex):
		for i in range(self.childCount(parent)):
			if self.childAt(parent, i).text(0) == text:
				return i
		return -1
	def moveItemForward(self, parent, oldIndex, newIndex):
		for int in range(oldIndex - newIndex):
			self.deleteItem(parent, newIndex)
class VariantDelegate(QItemDelegate):
	def __init__(self, parent=None):
		super(VariantDelegate, self).__init__(parent)
		self.boolExp = QRegExp()
		self.boolExp.setPattern('true|false')
		self.boolExp.setCaseSensitivity(Qt.CaseInsensitive)
		self.byteArrayExp = QRegExp()
		self.byteArrayExp.setPattern('[\\x00-\\xff]*')
		self.charExp = QRegExp()
		self.charExp.setPattern('.')
		self.colorExp = QRegExp()
		self.colorExp.setPattern('\\(([0-9]*),([0-9]*),([0-9]*),([0-9]*)\\)')
		self.doubleExp = QRegExp()
		self.doubleExp.setPattern('')
		self.pointExp = QRegExp()
		self.pointExp.setPattern('\\((-?[0-9]*),(-?[0-9]*)\\)')
		self.rectExp = QRegExp()
		self.rectExp.setPattern('\\((-?[0-9]*),(-?[0-9]*),(-?[0-9]*),(-?[0-9]*)\\)')
		self.signedIntegerExp = QRegExp()
		self.signedIntegerExp.setPattern('-?[0-9]*')
		self.sizeExp = QRegExp(self.pointExp)
		self.unsignedIntegerExp = QRegExp()
		self.unsignedIntegerExp.setPattern('[0-9]*')
		self.dateExp = QRegExp()
		self.dateExp.setPattern('([0-9]{,4})-([0-9]{,2})-([0-9]{,2})')
		self.timeExp = QRegExp()
		self.timeExp.setPattern('([0-9]{,2}):([0-9]{,2}):([0-9]{,2})')
		self.dateTimeExp = QRegExp()
		self.dateTimeExp.setPattern(self.dateExp.pattern() + 'T' + self.timeExp.pattern())
	def paint(self, painter, option, index):
		if index.column() == 2:
			value = index.model().data(index, Qt.UserRole)
			if not self.isSupportedType(value):
				myOption = QStyleOptionViewItem(option)
				myOption.state &= ~QStyle.State_Enabled
				super(VariantDelegate, self).paint(painter, myOption, index)
				return
		super(VariantDelegate, self).paint(painter, option, index)
	def createEditor(self, parent, option, index):
		if index.column() != 2:
			return None
		originalValue = index.model().data(index, Qt.UserRole)
		if not self.isSupportedType(originalValue):
			return None
		lineEdit = QLineEdit(parent)
		lineEdit.setFrame(False)
		if isinstance(originalValue, bool):
			regExp = self.boolExp
		elif isinstance(originalValue, float):
			regExp = self.doubleExp
		elif isinstance(originalValue, int):
			regExp = self.signedIntegerExp
		elif isinstance(originalValue, QByteArray):
			regExp = self.byteArrayExp
		elif isinstance(originalValue, QColor):
			regExp = self.colorExp
		elif isinstance(originalValue, QDate):
			regExp = self.dateExp
		elif isinstance(originalValue, QDateTime):
			regExp = self.dateTimeExp
		elif isinstance(originalValue, QTime):
			regExp = self.timeExp
		elif isinstance(originalValue, QPoint):
			regExp = self.pointExp
		elif isinstance(originalValue, QRect):
			regExp = self.rectExp
		elif isinstance(originalValue, QSize):
			regExp = self.sizeExp
		else:
			regExp = QRegExp()
		if not regExp.isEmpty():
			validator = QRegExpValidator(regExp, lineEdit)
			lineEdit.setValidator(validator)
		return lineEdit
	def setEditorData(self, editor, index):
		value = index.model().data(index, Qt.UserRole)
		if editor is not None:
			editor.setText(self.displayText(value))
	def setModelData(self, editor, model, index):
		if not editor.isModified():
			return
		text = editor.text()
		validator = editor.validator()
		if validator is not None:
			state, text, _ = validator.validate(text, 0)
			if state != QValidator.Acceptable:
				return
		originalValue = index.model().data(index, Qt.UserRole)
		if isinstance(originalValue, QColor):
			self.colorExp.exactMatch(text)
			value = QColor(min(int(self.colorExp.cap(1)), 255),
						   min(int(self.colorExp.cap(2)), 255),
						   min(int(self.colorExp.cap(3)), 255),
						   min(int(self.colorExp.cap(4)), 255))
		elif isinstance(originalValue, QDate):
			value = QDate.fromString(text, Qt.ISODate)
			if not value.isValid():
				return
		elif isinstance(originalValue, QDateTime):
			value = QDateTime.fromString(text, Qt.ISODate)
			if not value.isValid():
				return
		elif isinstance(originalValue, QTime):
			value = QTime.fromString(text, Qt.ISODate)
			if not value.isValid():
				return
		elif isinstance(originalValue, QPoint):
			self.pointExp.exactMatch(text)
			value = QPoint(int(self.pointExp.cap(1)),
						   int(self.pointExp.cap(2)))
		elif isinstance(originalValue, QRect):
			self.rectExp.exactMatch(text)
			value = QRect(int(self.rectExp.cap(1)),
						  int(self.rectExp.cap(2)),
						  int(self.rectExp.cap(3)),
						  int(self.rectExp.cap(4)))
		elif isinstance(originalValue, QSize):
			self.sizeExp.exactMatch(text)
			value = QSize(int(self.sizeExp.cap(1)),
						  int(self.sizeExp.cap(2)))
		elif isinstance(originalValue, list):
			value = text.split(',')
		else:
			value = type(originalValue)(text)
		model.setData(index, self.displayText(value), Qt.DisplayRole)
		model.setData(index, value, Qt.UserRole)
	@staticmethod
	def isSupportedType(value):
		return isinstance(value, (bool, float, int, QByteArray, str, QColor,
				QDate, QDateTime, QTime, QPoint, QRect, QSize, list))
	@staticmethod
	def displayText(value):
		if isinstance(value, (bool, int, QByteArray)):
			return str(value)
		if isinstance(value, str):
			return value
		elif isinstance(value, float):
			return '%g' % value
		elif isinstance(value, QColor):
			return '(%u,%u,%u,%u)' % (value.red(), value.green(), value.blue(), value.alpha())
		elif isinstance(value, (QDate, QDateTime, QTime)):
			return value.toString(Qt.ISODate)
		elif isinstance(value, QPoint):
			return '(%d,%d)' % (value.x(), value.y())
		elif isinstance(value, QRect):
			return '(%d,%d,%d,%d)' % (value.x(), value.y(), value.width(), value.height())
		elif isinstance(value, QSize):
			return '(%d,%d)' % (value.width(), value.height())
		elif isinstance(value, list):
			return ','.join(value)
		elif value is None:
			return '<Invalid>'
		return '<%s>' % value
if __name__ == '__main__':
	app = QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.show()
	sys.exit(app.exec_())

"""
Settings (`settings`)
=====================
A more `dict` like interface for QSettings
"""
import abc
import logging
from collections import namedtuple, MutableMapping
from PyQt5.QtCore import QObject, QEvent, QCoreApplication, QSettings
from PyQt5.QtCore import pyqtSignal as Signal
_QObjectType = type(QObject)
log = logging.getLogger(__name__)
config_slot = namedtuple(
	"config_slot",
	["key",
	 "value_type",
	 "default_value",
	 "doc"]
)
class SettingChangedEvent(QEvent):
	"""
	A settings has changed.
	This event is sent by Settings instance to itself when a setting for
	a key has changed.
	"""
	SettingChanged = QEvent.registerEventType()
	"""Setting was changed"""
	SettingAdded = QEvent.registerEventType()
	"""A setting was added"""
	SettingRemoved = QEvent.registerEventType()
	"""A setting was removed"""
	def __init__(self, etype, key, value=None, oldValue=None):
		"""
		Initialize the event instance
		"""
		QEvent.__init__(self, etype)
		self.__key = key
		self.__value = value
		self.__oldValue = oldValue
	def key(self):
		return self.__key
	def value(self):
		return self.__value
	def oldValue(self):
		return self.__oldValue
def qt_to_mapped_type(value):
	"""
	Try to convert a Qt value to the corresponding python mapped type
	(i.e. QString to unicode, etc.).
	"""
	if isinstance(value, str):
		return str(value)
	elif isinstance(value, str):
		return str(value)
	else:
		return value
class QABCMeta(_QObjectType, abc.ABCMeta):
	def __init__(self, name, bases, attr_dict):
		_QObjectType.__init__(self, name, bases, attr_dict)
		abc.ABCMeta.__init__(self, name, bases, attr_dict)
class _pickledvalue(object):
	def __init__(self, value):
		self.value = value
class Settings(QObject, MutableMapping, metaclass=QABCMeta):
	"""
	A `dict` like interface to a QSettings store.
	"""
	valueChanged = Signal(str, object)
	valueAdded = Signal(str, object)
	keyRemoved = Signal(str)
	def __init__(self, parent=None, defaults=(), path=None, store=None):
		QObject.__init__(self, parent)
		if store is None:
			store = QSettings()
		path = path = (path or "").rstrip("/")
		self.__path = path
		self.__defaults = dict([(slot.key, slot) for slot in defaults])
		self.__store = store
	def __key(self, key):
		"""
		Return the full key (including group path).
		"""
		if self.__path:
			return "/".join([self.__path, key])
		else:
			return key
	def __delitem__(self, key):
		"""
		Delete the setting for key. If key is a group remove the
		whole group.
		.. note:: defaults cannot be deleted they are instead reverted
				  to their original state.
		"""
		if key not in self:
			raise KeyError(key)
		if self.isgroup(key):
			group = self.group(key)
			for key in group:
				del group[key]
		else:
			fullkey = self.__key(key)
			oldValue = self.get(key)
			if self.__store.contains(fullkey):
				self.__store.remove(fullkey)
			newValue = None
			if fullkey in self.__defaults:
				newValue = self.__defaults[fullkey].default_value
				etype = SettingChangedEvent.SettingChanged
			else:
				etype = SettingChangedEvent.SettingRemoved
			QCoreApplication.sendEvent(
				self, SettingChangedEvent(etype, key, newValue, oldValue)
			)
	def __value(self, fullkey, value_type):
		typesafe = value_type is not None
		if value_type is None:
			value = self.__store.value(fullkey)
		else:
			try:
				value = self.__store.value(fullkey, type=value_type)
			except TypeError:
				# In case the value was pickled in a type unsafe mode
				value = self.__store.value(fullkey)
				typesafe = False
		if not typesafe:
			if isinstance(value, _pickledvalue):
				value = value.value
			else:
				log.warning("value for key %r is not a '_pickledvalue' (%r),"
							"possible loss of type information.",
							fullkey,
							type(value))
		return value
	def __setValue(self, fullkey, value, value_type=None):
		typesafe = value_type is not None
		if not typesafe:
			# value is stored in a _pickledvalue wrapper to force PyQt
			# to store it in a pickled format so we don't lose the type
			# TODO: Could check if QSettings.Format stores type info.
			value = _pickledvalue(value)
		self.__store.setValue(fullkey, value)
	def __getitem__(self, key):
		"""
		Get the setting for key.
		"""
		if key not in self:
			raise KeyError(key)
		if self.isgroup(key):
			raise KeyError("{0!r} is a group".format(key))
		fullkey = self.__key(key)
		slot = self.__defaults.get(fullkey, None)
		if self.__store.contains(fullkey):
			value = self.__value(fullkey, slot.value_type if slot else None)
		else:
			value = slot.default_value
		return value
	def __setitem__(self, key, value):
		"""
		Set the setting for key.
		"""
		if not isinstance(key, str):
			raise TypeError(key)
		fullkey = self.__key(key)
		value_type = None
		if fullkey in self.__defaults:
			value_type = self.__defaults[fullkey].value_type
			if not isinstance(value, value_type):
				value = qt_to_mapped_type(value)
				if not isinstance(value, value_type):
					raise TypeError(
						"Expected {0!r} got {1!r}".format(value_type.__name__,
														  type(value).__name__))
		if key in self:
			oldValue = self.get(key)
			etype = SettingChangedEvent.SettingChanged
		else:
			oldValue = None
			etype = SettingChangedEvent.SettingAdded
		self.__setValue(fullkey, value, value_type)
		QCoreApplication.sendEvent(
			self, SettingChangedEvent(etype, key, value, oldValue)
		)
	def __contains__(self, key):
		"""
		Return `True` if settings contain the `key`, False otherwise.
		"""
		fullkey = self.__key(key)
		return self.__store.contains(fullkey) or (fullkey in self.__defaults)
	def __iter__(self):
		"""Return an iterator over over all keys.
		"""
		keys = list(map(str, self.__store.allKeys())) + \
			   list(self.__defaults.keys())
		if self.__path:
			path = self.__path + "/"
			keys = [key for key in keys if key.startswith(path)]
			keys = [key[len(path):] for key in keys]
		return iter(sorted(set(keys)))
	def __len__(self):
		return len(list(iter(self)))
	def group(self, path):
		if self.__path:
			path = "/".join([self.__path, path])
		return Settings(self, list(self.__defaults.values()), path, self.__store)
	def isgroup(self, key):
		"""
		Is the `key` a settings group i.e. does it have subkeys.
		"""
		if key not in self:
			raise KeyError("{0!r} is not a valid key".format(key))
		return len(self.group(key)) > 0
	def isdefault(self, key):
		"""
		Is the value for key the default.
		"""
		if key not in self:
			raise KeyError(key)
		return not self.__store.contains(self.__key(key))
	def clear(self):
		"""
		Clear the settings and restore the defaults.
		"""
		self.__store.clear()
	def add_default_slot(self, default):
		"""
		Add a default slot to the settings This also replaces any
		previously set value for the key.
		"""
		value = default.default_value
		oldValue = None
		etype = SettingChangedEvent.SettingAdded
		key = default.key
		if key in self:
			oldValue = self.get(key)
			etype = SettingChangedEvent.SettingChanged
			if not self.isdefault(key):
				# Replacing a default value.
				self.__store.remove(self.__key(key))
		self.__defaults[key] = default
		event = SettingChangedEvent(etype, key, value, oldValue)
		QCoreApplication.sendEvent(self, event)
	def get_default_slot(self, key):
		return self.__defaults[self.__key(key)]
	def values(self):
		"""
		Return a list over of all values in the settings.
		"""
		return MutableMapping.values(self)
	def customEvent(self, event):
		QObject.customEvent(self, event)
		if isinstance(event, SettingChangedEvent):
			if event.type() == SettingChangedEvent.SettingChanged:
				self.valueChanged.emit(event.key(), event.value())
			elif event.type() == SettingChangedEvent.SettingAdded:
				self.valueAdded.emit(event.key(), event.value())
			elif event.type() == SettingChangedEvent.SettingRemoved:
				self.keyRemoved.emit(event.key())
			parent = self.parent()
			if isinstance(parent, Settings):
				# Assumption that the parent is a parent setting group.
				parent.customEvent(
					SettingChangedEvent(event.type(),
										"/".join([self.__path, event.key()]),
										event.value(),
										event.oldValue())
				)

# -*- coding: utf-8 -*-
"""
Copyright (c) 2013-2018 Matic Kukovec.
Released under the GNU GPL3 license.
For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
##  FILE DESCRIPTION:
##	  Module used to save, load, ... settings of Ex.Co.
import os
import os.path
import runpy
import data
import themes
import functions
"""
----------------------------------------------------------------
Static Object for storing default editor settings that are used
when a new editor is created
----------------------------------------------------------------
"""
class Editor:
	"""
	These are the built-in defaults, attributes should be changed
	in other modules!
	"""
	# Default EOL style in editors (EolWindows-CRLF, EolUnix-LF, EolMac-CR)
	end_of_line_mode = data.QsciScintilla.EolUnix
	# Font colors and styles
	font = data.QFont('Courier', 10)
	brace_color = data.QColor(255, 153, 0)
	comment_font = b'Courier'
	# Edge marker
	edge_marker_color = data.QColor(180, 180, 180, alpha=255)
	edge_marker_column = 90
	# Various
	cursor_line_visible = False
	# Maximum limit of highlighting instances
	maximum_highlights = 300
	# Global width of tabs
	tab_width = 4
	# Zoom factor when a new editor is created (default is 0)
	zoom_factor = 0
	"""
	-------------------------------------------
	Keyboard shortcuts
	-------------------------------------------
	"""
	class Keys:
		# Custom editor commands
		copy = 'Ctrl+C'
		cut = 'Ctrl+X'
		paste = 'Ctrl+V'
		undo = 'Ctrl+Z'
		redo = 'Ctrl+Y'
		select_all = 'Ctrl+A'
		indent = 'Tab'
		unindent = 'Shift+Tab'
		delete_start_of_word = 'Ctrl+BackSpace'
		delete_end_of_word = 'Ctrl+Delete'
		delete_start_of_line = 'Ctrl+Shift+BackSpace'
		delete_end_of_line = 'Ctrl+Shift+Delete'
		go_to_start = 'Ctrl+Home'
		go_to_end = 'Ctrl+End'
		select_page_up = 'Shift+PageUp'
		select_page_down = 'Shift+PageDown'
		select_to_start = 'Ctrl+Shift+Home'
		select_to_end = 'Ctrl+Shift+End'
		scroll_up = 'PageUp'
		scroll_down = 'PageDown'
		line_cut = 'Ctrl+L'
		line_copy = 'Ctrl+Shift+T'
		line_delete = 'Ctrl+Shift+L'
		line_transpose = 'Ctrl+T'
		line_selection_duplicate = 'Ctrl+D'
		@staticmethod
		def check_function(function_name):
			check_list = [x for x in dir(Editor.Keys) if not x.startswith('__')]
			return function_name in check_list
		@staticmethod
		def check_combination(combination):
			if combination.startswith("#"):
			   combination = combination[1:]
			check_list = [
				(x, getattr(Editor.Keys, x))
					for x in dir(Editor.Keys)
						if not x.startswith('__')
			]
			for name, keys in check_list:
				if not(isinstance(keys, str)) and not(isinstance(keys, list)):
					continue
				if isinstance(combination, list):
					if isinstance(keys, list):
						for k in keys:
							for c in combination:
								if k.strip().lower() == c.strip().lower():
									return True
					else:
						for c in combination:
							if keys.strip().lower() == c.strip().lower():
								return True
				elif isinstance(keys, str):
					if keys.strip().lower() == combination.strip().lower():
						return True
			return False
"""
-------------------------------------------
General keyboard shortcuts
-------------------------------------------
"""
class Keys:
	bookmark_goto = [
		"Alt+0", "Alt+1", "Alt+2", "Alt+3", "Alt+4",
		"Alt+5", "Alt+6", "Alt+7", "Alt+8", "Alt+9",
	]
	bookmark_store = [
		"Alt+Shift+0", "Alt+Shift+1", "Alt+Shift+2", "Alt+Shift+3",
		"Alt+Shift+4", "Alt+Shift+5", "Alt+Shift+6", "Alt+Shift+7",
		"Alt+Shift+8", "Alt+Shift+9",
	]
	bookmark_toggle = "Ctrl+B"
	clear_highlights = 'Ctrl+Shift+G'
	close_tab = 'Ctrl+W'
	cwd_tree = 'F7'
	new_cwd_tree = 'Ctrl+F7'
	cwd_explorer = 'Alt+F7'
	find = 'Ctrl+F'
	find_and_replace = 'Ctrl+Shift+F'
	find_files = 'Ctrl+F1'
	find_in_documents = 'Ctrl+F4'
	find_in_files = 'Ctrl+F2'
	find_replace_in_documents = 'Ctrl+F5'
	function_wheel_toggle = 'F1'
	goto_line = 'Ctrl+M'
	highlight = 'Ctrl+G'
	indent_to_cursor = 'Ctrl+I'
	lower_focus = 'Ctrl+3'
	main_focus = 'Ctrl+1'
	maximize_window = 'F12'
	move_tab_left = 'Ctrl+,'
	move_tab_right = 'Ctrl+.'
	new_file = 'Ctrl+N'
	node_tree = 'F8'
	open_file = 'Ctrl+O'
	regex_find = 'Alt+F'
	regex_find_and_replace = 'Alt+Shift+F'
	regex_highlight = 'Alt+G'
	regex_replace_all = 'Alt+Shift+H'
	regex_replace_selection = 'Alt+H'
	reload_file = 'F9'
	repeat_eval = 'F3'
	repl_focus_multi = 'Ctrl+5'
	repl_focus_single_1 = 'Ctrl+R'
	repl_focus_single_2 = 'Ctrl+4'
	replace_all = 'Ctrl+Shift+H'
	replace_all_in_documents = 'Ctrl+F6'
	replace_in_files = 'Ctrl+F3'
	replace_selection = 'Ctrl+H'
	reset_zoom = "Alt+Z"
	save_file = 'Ctrl+S'
	saveas_file = 'Ctrl+Shift+S'
	spin_clockwise = 'Ctrl+PgDown'
	spin_counterclockwise = 'Ctrl+PgUp'
	to_lowercase = 'Alt+L'
	to_uppercase = 'Alt+U'
	toggle_autocompletion = 'Ctrl+K'
	toggle_comment = 'Ctrl+Shift+C'
	toggle_edge = 'Ctrl+E'
	toggle_log = 'F10'
	toggle_main_window_side = 'F6'
	toggle_mode = 'F5'
	toggle_wrap = 'Ctrl+P'
	upper_focus = 'Ctrl+2'
	@staticmethod
	def check_function(function_name):
		check_list = [
			x for x in dir(Keys)
				if not x.startswith('__')
		]
		return function_name in check_list
	@staticmethod
	def check_combination(combination):
		check_list = [
			(x, getattr(Keys, x))
				for x in dir(Keys)
					if not x.startswith('__')
		]
		for name, keys in check_list:
			if not(isinstance(keys, str)) and not(isinstance(keys, list)):
				continue
			if isinstance(combination, list):
				if isinstance(keys, list):
					for k in keys:
						for c in combination:
							if k.strip().lower() == c.strip().lower():
								return True
				else:
					for c in combination:
						if keys.strip().lower() == c.strip().lower():
							return True
			elif isinstance(keys, str):
				if keys.strip().lower() == combination.strip().lower():
					return True
		return False
"""
-------------------------------------------
Structure for storing session information
-------------------------------------------
"""
class Session:
	"""Structure for storing single session information"""
	name		= ""
	group	   = None
	main_files  = []
	upper_files = []
	lower_files = []
	def __init__(self, name):
		"""Session initialization"""
		#Initialization of class variables turns them into instance variables
		self.name		   = name
		self.group		  = None
		self.main_files	 = []
		self.upper_files	= []
		self.lower_files	= []
	@staticmethod
	def parse(session_dict):
		"""
		Parse a session dictionary into a session object.
		Example dictionary:
			'application': {
				'Group': ('embedoffice',),
				'Main window files': [
					'D:/embedoffice_stuff/embedoffice/data.py',
					'D:/embedoffice_stuff/embedoffice/embedoffice.py',
					'D:/embedoffice_stuff/embedoffice/gui/forms/mainwindow.py',
					'D:/embedoffice_stuff/embedoffice/gui/forms/basicwidget.py',
					'D:/embedoffice_stuff/embedoffice/gui/helpers/projectdisplay.py',
					'D:/embedoffice_stuff/embedoffice/project/project.py',
					'D:/embedoffice_stuff/embedoffice/gui/helpers/projectwizard.py',
					'D:/embedoffice_stuff/embedoffice/gui/helpers/buttons.py',
					'D:/embedoffice_stuff/embedoffice/components/hexbuilding.py',
					'D:/embedoffice_stuff/embedoffice/components/hexpainting.py',
				],
				'Upper window files': [
				],
				'Lower window files': [
				],
			},
		"""
		session = Session(session)
		session.group = in_sessions[session]['Group']
		session.main_files = in_sessions[session]['Main window files']
		session.upper_files = in_sessions[session]['Upper window files']
		session.lower_files = in_sessions[session]['Lower window files']
"""
-------------------------------------------
Object for manipulating settings/sessions
-------------------------------------------
"""
class SettingsFileManipulator:
	"""
	Object that will be used for saving, loading, ... all of the Ex.Co. settings
	"""
	#Class variables
	settings_filename			   = "exco.ini"
	settings_filename_with_path	 = ""
	application_directory		   = ""
	resources_directory			 = "resources/"
	level_spacing				   = "	"
	max_number_of_recent_files	  = 10
	recent_files					= []
	stored_sessions				 = []
	context_menu_functions		  = {}
	error_lock					  = False
	# General settings
	main_window_side				= data.MainWindowSide.RIGHT
	theme						   = themes.Air
	empty_settings_list = [
		"# General Settings",
		"main_window_side = 0",
		"theme = themes.Air",
		"",
		"# Custom context menu functions",
		"context_menu_functions = {}",
		"",
		"# Recent files",
		"recent_files = []",
		"",
		"# Sessions",
		"sessions = {}",
	]
	def __init__(self, app_dir, res_dir):
		#Assign the application directory
		self.application_directory  = app_dir
		self.resources_directory	= res_dir
		#Join the application directory with the settings filename
		self.settings_filename_with_path = os.path.join(
			self.application_directory,
			self.settings_filename
		)
		#Check if the settings file exists
		if self.check_settings_file() == None:
			#Create the settings file
			self.create_settings_file(self.empty_settings_list)
		#Load the settings from the settings file
		self.load_settings()
	def check_settings_file(self):
		"""Check if the settings file exists"""
		return functions.test_text_file(self.settings_filename_with_path)
	def create_settings_file(self, list_of_lines):
		"""Create the settings file"""
		#Create/truncate settings file
		file = open(self.settings_filename_with_path, "w", encoding="utf-8")
		#Write the default settings string into the empty settings file
		for line in list_of_lines:
			file.write(line + "\n")
		#Close the file handle
		file.close()
	def _parse_sessions(self, in_sessions):
		parsed_sessions = []
		for session in in_sessions:
			current_session = Session(session)
			current_session.group = in_sessions[session]['Group']
			current_session.main_files = in_sessions[session]['Main window files']
			current_session.upper_files = in_sessions[session]['Upper window files']
			current_session.lower_files = in_sessions[session]['Lower window files']
			parsed_sessions.append(current_session)
		return parsed_sessions
	def write_settings_file(self,
							main_window_side,
							theme,
							recent_files,
							stored_sessions,
							context_menu_functions):
		settings_lines = []
		settings_lines.append("# General Settings")
		settings_lines.append("main_window_side = {}".format(main_window_side))
		settings_lines.append("theme = {}".format(theme.__name__))
		settings_lines.append("")
		# Recent file list
		settings_lines.append("# Recent files")
		settings_lines.append("recent_files = [")
		for file in recent_files:
			settings_lines.append("	'{}',".format(file))
		settings_lines.append("]")
		settings_lines.append("")
		# Custom context menu functions
		settings_lines.append("# Custom context menu functions")
		settings_lines.append("context_menu_functions = {")
		for func_type in context_menu_functions:
			settings_lines.append("	'{}': {{".format(func_type))
			for func in context_menu_functions[func_type]:
				settings_lines.append("		{}: '{}',".format(
					func, context_menu_functions[func_type][func])
				)
			settings_lines.append("	},")
		settings_lines.append("}")
		settings_lines.append("")
		# Sessions
		settings_lines.append("# Sessions")
		settings_lines.append("sessions = {")
		for session in stored_sessions:
			settings_lines.append("	'{}': {{".format(session.name))
			if isinstance(session.group, str) or (session.group == None):
				settings_lines.append("		'Group': {},".format(repr(session.group)))
			elif isinstance(session.group, tuple) and all([isinstance(x, str) for x in session.group]):
				settings_lines.append("		'Group': {},".format(str(session.group)))
			else:
				print("'{}'".format(repr(session.name)))
				raise Exception("[SETTINGS] Unknown session group type!")
			settings_lines.append("		'Main window files': [")
			for file in session.main_files:
				settings_lines.append("			'{}',".format(file))
			settings_lines.append("		],")
			settings_lines.append("		'Upper window files': [")
			for file in session.upper_files:
				settings_lines.append("			'{}',".format(file))
			settings_lines.append("		],")
			settings_lines.append("		'Lower window files': [")
			for file in session.lower_files:
				settings_lines.append("			'{}',".format(file))
			settings_lines.append("		],")
			settings_lines.append("	},")
		settings_lines.append("}")
		#Save the file to disk
		self.create_settings_file(settings_lines)
	def save_settings(self,
					  main_window_side,
					  theme,
					  context_menu_functions=None):
		"""Save all settings to the settings file"""
		if self.error_lock == True:
			return
		if context_menu_functions == None:
			context_menu_functions = self.context_menu_functions
		else:
			self.context_menu_functions = context_menu_functions
		self.write_settings_file(
			main_window_side,
			theme,
			self.recent_files,
			self.stored_sessions,
			context_menu_functions
		)
	def update_recent_files(self):
		"""Update only the recent file list in settings file"""
		if self.error_lock == True:
			return
		# Import the init file as a python module
		init_module = runpy.run_path(
			self.settings_filename_with_path,
			init_globals = {"themes": themes, "data": data}
		)
		# Update only the recent file list
		stored_sessions = self._parse_sessions(init_module["sessions"])
		# Save the updated settings
		self.write_settings_file(
			init_module["main_window_side"],
			init_module["theme"],
			self.recent_files,
			stored_sessions,
			self.context_menu_functions
		)
	def load_settings(self):
		"""Load all setting from the settings file"""
		try:
			# Import the init file as a python module
			init_module = runpy.run_path(
				self.settings_filename_with_path,
				init_globals = {"themes": themes, "data": data}
			)
			# Main window side
			self.main_window_side = init_module["main_window_side"]
			# Theme
			self.theme = init_module["theme"]
			# Recent files
			self.recent_files = init_module["recent_files"]
			# Sessions
			self.stored_sessions = self._parse_sessions(init_module["sessions"])
			# Load custom context menu functions
			if "context_menu_functions" in init_module.keys():
				self.context_menu_functions = init_module["context_menu_functions"]
			else:
				self.context_menu_functions = {}
			# Return success
			return True
		except:
			# Set the default settings values
			self.main_window_side = data.MainWindowSide.LEFT
			self.theme = themes.Air
			self.recent_files = []
			self.stored_sessions = []
			self.context_menu_functions = {}
			# Set the error flag
			self.error_lock = True
			# Return error
			return False
	def add_session(self,
					session_name,
					session_group,
					main_files,
					upper_files,
					lower_files):
		"""Add a new session to the stored session list"""
		#Create the new session object
		session = Session(session_name)
		#Store the group name
		session.group = session_group
		#Add the files to the session
		session.main_files.extend(main_files)
		session.upper_files.extend(upper_files)
		session.lower_files.extend(lower_files)
		#Check if a session with the same name is already in the stored sessions list
		session_found = False
		for i, s in enumerate(self.stored_sessions):
			#Check if the session names and groups match
			if s.name == session_name and s.group == session_group:
				#Replace the session
				self.stored_sessions[i] = session
				#Save the new settings
				self.save_settings(
					self.main_window_side, self.theme
				)
				session_found = True
		#Check if the session was already found
		if session_found == False:
			#Add the session to the list
			self.stored_sessions.append(session)
			#Save the new settings
			self.save_settings(self.main_window_side, self.theme)
	def remove_session(self, session_name, session_group=None):
		"""
		Remove a session from the stored session list
		"""
		# Loop through the stored sessions
		for session in self.stored_sessions:
			# Check if the session names and groups match
			if session.name == session_name and session_group == session.group:
				# Remove the session from the stored session list
				self.stored_sessions.remove(session)
				# Save the new settings
				self.save_settings(self.main_window_side, self.theme)
				return True
		# Signal that the session was not removed
		return False
	def remove_group(self, remove_group):
		"""
		Remove an entire group from the stored session list
		"""
		found_group = False
		filtered_sessions = []
		for i, session in enumerate(self.stored_sessions):
			if session.group != remove_group:
				filtered_sessions.append(session)
			else:
				found_group = True
		if found_group == True:
			# Overwrite the old session list
			self.stored_sessions = filtered_sessions
			# Save the new settings
			self.save_settings(self.main_window_side, self.theme)
			# Signal that the session was not removed
		return found_group
	def get_session(self, session_name, session_group=None):
		"""Return the session from the stored sessions list if it exists"""
		for session in self.stored_sessions:
			#Check if the session names match
			if session.name == session_name and session.group == session_group:
				#Return the session
				return session
		#Return None if session was not found
		return None
	def sort_sessions(self):
		"""Sort the stored sessions alphabetically by name"""
		#Nested function for retrieving the sessions name attribute case insensitively
		def get_case_insensitive_name(item):
			name = item.name
			return name.lower()
		#Sort the stored sessions
		self.stored_sessions.sort(key=get_case_insensitive_name)
	def add_recent_file(self, new_file):
		"""Add a new file to the recent file list"""
		# Replace back-slashes to forward-slashes on Windows
		if data.platform == "Windows":
			new_file = new_file.replace("\\", "/")
		# Check recent files list length
		while len(self.recent_files) > self.max_number_of_recent_files:
			# The recent files list is to long
			self.recent_files.pop(0)
		# Check if he new file is already in the list
		if new_file in self.recent_files:
			# Check if the file is already at the top
			if self.recent_files.index(new_file) == (self.max_number_of_recent_files-1):
				return
			# Remove the old file with the same name as the new file from the list
			self.recent_files.pop(self.recent_files.index(new_file))
			# Add the new file to the end of the list
			self.recent_files.append(new_file)
		else:
			# The new file is not in the list, append it to the end of the list
			self.recent_files.append(new_file)
		# Save the new settings
		self.update_recent_files()
	"""
	Session group functionality
	"""
	class Group:
		def __init__(self, name, parent=None, reference=None):
			self.name = name
			self.reference = reference
			self.parent = parent
			self.items = {}
			self.subgroups = {}
		def subgroup_get(self, name):
			if name in self.subgroups.keys():
				return self.subgroups[name]
			else:
				return None
		def subgroup_get_recursive(self, group_list):
			name = group_list[0]
			if name in self.subgroups.keys():
				if len(group_list) > 1:
					return self.subgroups[name].subgroup_get_recursive(group_list[1:])
				else:
					return self.subgroups[name]
			else:
				return None
		def subgroup_create(self, name, reference):
			if not(name in self.subgroups.keys()):
				# Create an instance of the same class as self
				self.subgroups[name] = self.__class__(name, self, reference)
			return self.subgroups[name]
	def get_sorted_groups(self):
		groups = []
		# Sort the sessions
		self.sort_sessions()
		# Add the groups to the menu first
		for session in self.stored_sessions:
			if session.group != None:
				if isinstance(session.group, str):
					session.group = (session.group, )
				group_found = False
				for group in groups:
					if session.group == group:
						# Group found, it's already in the list
						group_found = True
						break
				if group_found == False:
					# Group is not in the list, add it as a tuple (name, reference)
					groups.append(session.group)
		# Sort the group list and add the groups to the session menu
		def sort_groups_func(arg=None):
			if isinstance(arg, tuple) and all([isinstance(x, str) for x in arg]):
				lowercase_group_tree = [x.lower() for x in arg]
				return " ".join(lowercase_group_tree)
			else:
				return arg.lower()
		groups.sort(key=sort_groups_func)
		return groups




"""
User settings/preference dialog
===============================
"""
import sys
import logging
from PyQt5.QtWidgets import (
	QWidget, QMainWindow, QComboBox, QCheckBox, QTabWidget,
	QToolBar, QAction, QStackedWidget, QVBoxLayout, QHBoxLayout,
	QFormLayout, QSizePolicy, QLineEdit, QLabel)
from PyQt5.QtCore import Qt, QEventLoop, QAbstractItemModel, QModelIndex
import config
from utils.propertybindings import AbstractBoundProperty, PropertyBinding, BindingManager
log = logging.getLogger(__name__)
def refresh_proxies():
	from Orange.canvas.__main__ import fix_set_proxy_env
	fix_set_proxy_env()
class UserDefaultsPropertyBinding(AbstractBoundProperty):
	"""
	A Property binding for a setting in a
	:class:`Orange.canvas.utility.settings.Settings` instance.
	"""
	def __init__(self, obj, propertyName, parent=None):
		AbstractBoundProperty.__init__(self, obj, propertyName, parent)
		obj.installEventFilter(self)
	def get(self):
		return self.obj.get(self.propertyName)
	def set(self, value):
		self.obj[self.propertyName] = value
	def eventFilter(self, obj, event):
		if event.type() == SettingChangedEvent.SettingChanged and \
				event.key() == self.propertyName:
			self.notifyChanged()
		return AbstractBoundProperty.eventFilter(self, obj, event)
class UserSettingsModel(QAbstractItemModel):
	"""
	An Item Model for user settings presenting a list of
	key, setting value entries along with it's status and type.
	"""
	def __init__(self, parent=None, settings=None):
		QAbstractItemModel.__init__(self, parent)
		self.__settings = settings
		self.__headers = ["Name", "Status", "Type", "Value"]
	def setSettings(self, settings):
		if self.__settings != settings:
			self.__settings = settings
			self.reset()
	def settings(self):
		return self.__settings
	def rowCount(self, parent=QModelIndex()):
		if parent.isValid():
			return 0
		elif self.__settings:
			return len(self.__settings)
		else:
			return 0
	def columnCount(self, parent=QModelIndex()):
		if parent.isValid():
			return 0
		else:
			return len(self.__headers)
	def parent(self, index):
		return QModelIndex()
	def index(self, row, column=0, parent=QModelIndex()):
		if parent.isValid() or \
				column < 0 or column >= self.columnCount() or \
				row < 0 or row >= self.rowCount():
			return QModelIndex()
		return self.createIndex(row, column, row)
	def headerData(self, section, orientation, role=Qt.DisplayRole):
		if section >= 0 and section < 4 and orientation == Qt.Horizontal:
			if role == Qt.DisplayRole:
				return self.__headers[section]
		return QAbstractItemModel.headerData(self, section, orientation, role)
	def data(self, index, role=Qt.DisplayRole):
		if self._valid(index):
			key = self._keyFromIndex(index)
			column = index.column()
			if role == Qt.DisplayRole:
				if column == 0:
					return key
				elif column == 1:
					default = self.__settings.isdefault(key)
					return "Default" if default else "User"
				elif column == 2:
					return type(self.__settings.get(key)).__name__
				elif column == 3:
					return self.__settings.get(key)
				return self
		return None
	def flags(self, index):
		if self._valid(index):
			flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
			if index.column() == 3:
				return Qt.ItemIsEditable | flags
			else:
				return flags
		return Qt.NoItemFlags
	def setData(self, index, value, role=Qt.EditRole):
		if self._valid(index) and index.column() == 3:
			key = self._keyFromIndex(index)
			try:
				self.__settings[key] = value
			except (TypeError, ValueError) as ex:
				log.error("Failed to set value (%r) for key %r", value, key,
						  exc_info=True)
			else:
				self.dataChanged.emit(index, index)
				return True
		return False
	def _valid(self, index):
		row = index.row()
		return row >= 0 and row < self.rowCount()
	def _keyFromIndex(self, index):
		row = index.row()
		return list(self.__settings.keys())[row]
def container_widget_helper(orientation=Qt.Vertical, spacing=None, margin=0):
	widget = QWidget()
	if orientation == Qt.Vertical:
		layout = QVBoxLayout()
		widget.setSizePolicy(QSizePolicy.Fixed,
							 QSizePolicy.MinimumExpanding)
	else:
		layout = QHBoxLayout()
	if spacing is not None:
		layout.setSpacing(spacing)
	if margin is not None:
		layout.setContentsMargins(0, 0, 0, 0)
	widget.setLayout(layout)
	return widget
class UserSettingsDialog(QMainWindow):
	"""
	A User Settings/Defaults dialog.
	"""
	MAC_UNIFIED = True
	def __init__(self, parent=None, **kwargs):
		QMainWindow.__init__(self, parent, **kwargs)
		self.setWindowFlags(Qt.Dialog)
		self.setWindowModality(Qt.ApplicationModal)
		self.layout().setSizeConstraint(QVBoxLayout.SetFixedSize)
		self.__macUnified = sys.platform == "darwin" and self.MAC_UNIFIED
		self._manager = BindingManager(self,
									   submitPolicy=BindingManager.AutoSubmit)
		self.__loop = None
		self.__settings = config.settings()
		self.__setupUi()
	def __setupUi(self):
		"""Set up the UI.
		"""
		if self.__macUnified:
			self.tab = QToolBar()
			self.addToolBar(Qt.TopToolBarArea, self.tab)
			self.setUnifiedTitleAndToolBarOnMac(True)
			# This does not seem to work
			self.setWindowFlags(self.windowFlags() & \
								~Qt.MacWindowToolBarButtonHint)
			self.tab.actionTriggered[QAction].connect(
				self.__macOnToolBarAction
			)
			central = QStackedWidget()
			central.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		else:
			self.tab = central = QTabWidget(self)
		self.stack = central
		self.setCentralWidget(central)
		# General Tab
		tab = QWidget()
		self.addTab(tab, self.tr("General"),
					toolTip=self.tr("General Options"))
		form = QFormLayout()
		tab.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		nodes = QWidget(self, objectName="nodes")
		nodes.setLayout(QVBoxLayout())
		nodes.layout().setContentsMargins(0, 0, 0, 0)
		cb_anim = QCheckBox(
			self.tr("Enable node animations"),
			objectName="enable-node-animations",
			toolTip=self.tr("Enable shadow and ping animations for nodes "
							"in the workflow.")
		)
		self.bind(cb_anim, "checked", "schemeedit/enable-node-animations")
		nodes.layout().addWidget(cb_anim)
		form.addRow(self.tr("Nodes"), nodes)
		links = QWidget(self, objectName="links")
		links.setLayout(QVBoxLayout())
		links.layout().setContentsMargins(0, 0, 0, 0)
		cb_show = QCheckBox(
			self.tr("Show channel names between widgets"),
			objectName="show-channel-names",
			toolTip=self.tr("Show source and sink channel names "
							"over the links.")
		)
		self.bind(cb_show, "checked", "schemeedit/show-channel-names")
		links.layout().addWidget(cb_show)
		form.addRow(self.tr("Links"), links)
		quickmenu = QWidget(self, objectName="quickmenu-options")
		quickmenu.setLayout(QVBoxLayout())
		quickmenu.layout().setContentsMargins(0, 0, 0, 0)
		cb1 = QCheckBox(self.tr("On double click"),
						toolTip=self.tr("Open quick menu on a double click "
										"on an empty spot in the canvas"))
		cb2 = QCheckBox(self.tr("On right click"),
						toolTip=self.tr("Open quick menu on a right click "
										"on an empty spot in the canvas"))
		cb3 = QCheckBox(self.tr("On space key press"),
						toolTip=self.tr("On Space key press while the mouse"
										"is hovering over the canvas."))
		cb4 = QCheckBox(self.tr("On any key press"),
						toolTip=self.tr("On any key press while the mouse"
										"is hovering over the canvas."))
		self.bind(cb1, "checked", "quickmenu/trigger-on-double-click")
		self.bind(cb2, "checked", "quickmenu/trigger-on-right-click")
		self.bind(cb3, "checked", "quickmenu/trigger-on-space-key")
		self.bind(cb4, "checked", "quickmenu/trigger-on-any-key")
		quickmenu.layout().addWidget(cb1)
		quickmenu.layout().addWidget(cb2)
		quickmenu.layout().addWidget(cb3)
		quickmenu.layout().addWidget(cb4)
		form.addRow(self.tr("Open quick menu on"), quickmenu)
		startup = QWidget(self, objectName="startup-group")
		startup.setLayout(QVBoxLayout())
		startup.layout().setContentsMargins(0, 0, 0, 0)
		cb_splash = QCheckBox(self.tr("Show splash screen"), self,
							  objectName="show-splash-screen")
		cb_welcome = QCheckBox(self.tr("Show welcome screen"), self,
							   objectName="show-welcome-screen")
		cb_updates = QCheckBox(self.tr("Check for updates"), self,
							   objectName="check-updates")
		self.bind(cb_splash, "checked", "startup/show-splash-screen")
		self.bind(cb_welcome, "checked", "startup/show-welcome-screen")
		self.bind(cb_updates, "checked", "startup/check-updates")
		startup.layout().addWidget(cb_splash)
		startup.layout().addWidget(cb_welcome)
		startup.layout().addWidget(cb_updates)
		form.addRow(self.tr("On startup"), startup)
		toolbox = QWidget(self, objectName="toolbox-group")
		toolbox.setLayout(QVBoxLayout())
		toolbox.layout().setContentsMargins(0, 0, 0, 0)
		exclusive = QCheckBox(self.tr("Only one tab can be open at a time"))
		self.bind(exclusive, "checked", "mainwindow/toolbox-dock-exclusive")
		toolbox.layout().addWidget(exclusive)
		form.addRow(self.tr("Tool box"), toolbox)
		tab.setLayout(form)
		# Output Tab
		tab = QWidget()
		self.addTab(tab, self.tr("Output"),
					toolTip="Output Redirection")
		form = QFormLayout()
		box = QWidget()
		layout = QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		combo = QComboBox()
		combo.addItems([self.tr("Critical"),
						self.tr("Error"),
						self.tr("Warn"),
						self.tr("Info"),
						self.tr("Debug")])
		self.bind(combo, "currentIndex", "logging/level")
		layout.addWidget(combo)
		box.setLayout(layout)
		form.addRow(self.tr("Logging"), box)
		box = QWidget()
		layout = QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		cb1 = QCheckBox(self.tr("Open in external browser"),
						objectName="open-in-external-browser")
		self.bind(cb1, "checked", "help/open-in-external-browser")
		layout.addWidget(cb1)
		box.setLayout(layout)
		form.addRow(self.tr("Help window"), box)
		tab.setLayout(form)
		# Error Reporting Tab
		tab = QWidget()
		self.addTab(tab, self.tr("Error Reporting"),
					toolTip="Settings related to error reporting")
		form = QFormLayout()
		line_edit_mid = QLineEdit()
		self.bind(line_edit_mid, "text", "error-reporting/machine-id")
		form.addRow("Machine ID:", line_edit_mid)
		box = QWidget()
		layout = QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		cb1 = QCheckBox(self.tr(""),
						toolTip=self.tr("Share anonymous usage statistics to improve Orange"))
		self.bind(cb1, "checked", "error-reporting/send-statistics")
		layout.addWidget(cb1)
		box.setLayout(layout)
		form.addRow(self.tr("Share Anonymous Statistics"), box)
		tab.setLayout(form)
		# Add-ons Tab
		tab = QWidget()
		self.addTab(tab, self.tr("Add-ons"),
					toolTip="Settings related to add-on installation")
		form = QFormLayout()
		conda = QWidget(self, objectName="conda-group")
		conda.setLayout(QVBoxLayout())
		conda.layout().setContentsMargins(0, 0, 0, 0)
		cb_conda_install = QCheckBox(self.tr("Install add-ons with conda"), self,
									 objectName="allow-conda")
		self.bind(cb_conda_install, "checked", "add-ons/allow-conda")
		conda.layout().addWidget(cb_conda_install)
		form.addRow(self.tr("Conda"), conda)
		form.addRow(self.tr("Pip"), QLabel("Pip install arguments:"))
		line_edit_pip = QLineEdit()
		self.bind(line_edit_pip, "text", "add-ons/pip-install-arguments")
		form.addRow("", line_edit_pip)
		tab.setLayout(form)
		# Network Tab
		tab = QWidget()
		self.addTab(tab, self.tr("Network"),
					toolTip="Settings related to networking")
		form = QFormLayout()
		line_edit_http_proxy = QLineEdit()
		self.bind(line_edit_http_proxy, "text", "network/http-proxy")
		form.addRow("HTTP proxy:", line_edit_http_proxy)
		line_edit_https_proxy = QLineEdit()
		self.bind(line_edit_https_proxy, "text", "network/https-proxy")
		form.addRow("HTTPS proxy:", line_edit_https_proxy)
		tab.setLayout(form)
		if self.__macUnified:
			# Need some sensible size otherwise mac unified toolbar 'takes'
			# the space that should be used for layout of the contents
			self.adjustSize()
	def addTab(self, widget, text, toolTip=None, icon=None):
		if self.__macUnified:
			action = QAction(text, self)
			if toolTip:
				action.setToolTip(toolTip)
			if icon:
				action.setIcon(toolTip)
			action.setData(len(self.tab.actions()))
			self.tab.addAction(action)
			self.stack.addWidget(widget)
		else:
			i = self.tab.addTab(widget, text)
			if toolTip:
				self.tab.setTabToolTip(i, toolTip)
			if icon:
				self.tab.setTabIcon(i, icon)
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.hide()
			self.deleteLater()
	def bind(self, source, source_property, key, transformer=None):
		target = UserDefaultsPropertyBinding(self.__settings, key)
		source = PropertyBinding(source, source_property)
		source.set(target.get())
		self._manager.bind(target, source)
	def commit(self):
		self._manager.commit()
	def revert(self):
		self._manager.revert()
	def reset(self):
		for target, source in self._manager.bindings():
			try:
				source.reset()
			except NotImplementedError:
				# Cannot reset.
				pass
			except Exception:
				log.error("Error reseting %r", source.propertyName,
						  exc_info=True)
	def exec_(self):
		self.__loop = QEventLoop()
		self.show()
		status = self.__loop.exec_()
		self.__loop = None
		refresh_proxies()
		return status
	def hideEvent(self, event):
		QMainWindow.hideEvent(self, event)
		if self.__loop is not None:
			self.__loop.exit(0)
			self.__loop = None
	def __macOnToolBarAction(self, action):
		self.stack.setCurrentIndex(action.data())


def QSettings_readArray(settings, key, scheme):
	"""
	Read the whole array from a QSettings instance
	Parameters
	----------
	settings : QSettings
	key : str
	scheme : Dict[str, type]
	Example
	-------
	>>> s = QSettings("./login.ini")
	>>> QSettings_readArray(s, "array", {"username": str, "password": str})
	[{"username": "darkhelmet", "password": "1234"}}
	"""
	from collections import Mapping
	items = []
	if not isinstance(scheme, Mapping):
		scheme = {key: None for key in scheme}
	count = settings.beginReadArray(key)
	for i in range(count):
		settings.setArrayIndex(i)
		keys = settings.allKeys()
		item = {}
		for key in keys:
			if key in scheme:
				vtype = scheme.get(key, None)
				if vtype is not None:
					value = settings.value(key, type=vtype)
				else:
					value = settings.value(key)
				item[key] = value
		items.append(item)
	settings.endArray()
	return items
def QSettings_writeArray(settings, key, values):
	# type: (QSettings, str, List[Dict[str, Any]]) -> None
	"""
	Write an array of values to a QSettings instance.
	Parameters
	----------
	settings : QSettings
	key : str
	values : List[Dict[str, Any]]
	Examples
	--------
	>>> s = QSettings("./login.ini")
	>>> QSettings_writeArray(
	...	 s, "array", [{"username": "darkhelmet", "password": "1234"}]
	... )
	"""
	settings.beginWriteArray(key, len(values))
	for i in range(len(values)):
		settings.setArrayIndex(i)
		for key_, val in values[i].items():
			settings.setValue(key_, val)
	settings.endArray()




#!/usr/bin/env python
# for linux install: "python setup.py install --prefix=/usr -f"
# for windows exe creation: "python setup.py py2exe"
from distutils.core import setup
from distutils.dist import Distribution
from distutils.cmd import Command
from distutils.command.install_data import install_data
from distutils.command.install import install
from distutils.command.build import build
from distutils.dep_util import newer
from distutils.log import warn, info, error
from distutils.errors import DistutilsFileError
try: import py2exe
except: pass
import os, glob, sys, subprocess
import __builtin__
def _(transl_str):
	return transl_str
__builtin__._ = _
__builtin__.SHARE_PATH = ""
sys.path.append(os.path.join(os.getcwd(), "modules"))
import cons
PO_DIR = 'locale'
MO_DIR = os.path.join('build', 'mo')
class CherryTreeDist(Distribution):
	global_options = Distribution.global_options + [
	   ("without-gettext", None, "Don't build/install gettext .mo files")]
	def __init__ (self, *args):
		self.without_gettext = False
		Distribution.__init__(self, *args)
class BuildData(build):
	def run(self):
		build.run(self)
		cherrytree_man_file = "linux/cherrytree.1"
		cherrytree_man_file_gz = cherrytree_man_file + ".gz"
		if newer(cherrytree_man_file, cherrytree_man_file_gz):
			if os.path.isfile(cherrytree_man_file_gz): os.remove(cherrytree_man_file_gz)
			import gzip
			f_in = open(cherrytree_man_file, 'rb')
			f_out = gzip.open(cherrytree_man_file_gz, 'wb')
			f_out.writelines(f_in)
			f_out.close()
			f_in.close()
		if self.distribution.without_gettext: return
		for po in glob.glob(os.path.join (PO_DIR, '*.po')):
			lang = os.path.basename(po[:-3])
			mo = os.path.join(MO_DIR, lang, 'cherrytree.mo')
			directory = os.path.dirname(mo)
			if not os.path.exists(directory):
				info('creating %s' % directory)
				os.makedirs(directory)
			if newer(po, mo):
				info('compiling %s -> %s' % (po, mo))
				try:
					rc = subprocess.call(['msgfmt', '-o', mo, po])
					if rc != 0: raise Warning, "msgfmt returned %d" % rc
				except Exception, e:
					error("Building gettext files failed. Try setup.py --without-gettext [build|install]")
					error("Error: %s" % str(e))
					sys.exit(1)
class Uninstall(Command):
	description = "Attempt an uninstall from an install --record file"
	user_options = [('manifest=', None, 'Installation record filename')]
	def initialize_options(self):
		self.manifest = None
	def finalize_options(self):
		pass
	def get_command_name(self):
		return 'uninstall'
	def run(self):
		f = None
		self.ensure_filename('manifest')
		try:
			try:
				if not self.manifest:
					raise DistutilsFileError("Pass manifest with --manifest=file")
				f = open(self.manifest)
				files = [file.strip() for file in f]
			except IOError, e:
				raise DistutilsFileError("unable to open install manifest: %s", str(e))
		finally:
			if f: f.close()
		for file in files:
			if os.path.isfile(file) or os.path.islink(file):
				info("removing %s" % repr(file))
				if not self.dry_run:
					try: os.unlink(file)
					except OSError, e:
						warn("could not delete: %s" % repr(file))
			elif not os.path.isdir(file):
				info("skipping %s" % repr(file))
		dirs = set()
		for file in reversed(sorted(files)):
			dir = os.path.dirname(file)
			if dir not in dirs and os.path.isdir(dir) and len(os.listdir(dir)) == 0:
				dirs.add(dir)
				# Only nuke empty Python library directories, else we could destroy
				# e.g. locale directories we're the only app with a .mo installed for.
				if dir.find("site-packages/") > 0:
					info("removing %s" % repr(dir))
					if not self.dry_run:
						try: os.rmdir(dir)
						except OSError, e:
							warn("could not remove directory: %s" % str(e))
				else: info("skipping empty directory %s" % repr(dir))
class Install(install):
	def run(self):
		self.distribution.scripts=['cherrytree']
		install.run(self)
class InstallData(install_data):
	def run(self):
		self.data_files.extend(self._find_mo_files())
		self.data_files.extend(self._find_desktop_file())
		install_data.run(self)
	def _find_desktop_file(self):
		return [("share/applications", ["linux/cherrytree.desktop"] )]
	def _find_mo_files (self):
		data_files = []
		if not self.distribution.without_gettext:
			for mo in glob.glob(os.path.join(MO_DIR, '*', 'cherrytree.mo')):
				lang = os.path.basename(os.path.dirname(mo))
				dest = os.path.join('share', 'locale', lang, 'LC_MESSAGES')
				data_files.append((dest, [mo]))
		return data_files
if "py2exe" in sys.argv:
	data_files = [("glade", glob.glob("glade/*.*") ), ("language-specs", glob.glob("language-specs/*.lang") )]
	import enchant
	data_files.extend(enchant.utils.win32_data_files())
	for lang in cons.AVAILABLE_LANGS:
		if lang in ["default", "en"]: continue
		data_files.append( ("locale/%s/LC_MESSAGES" % lang, ["locale/%s/LC_MESSAGES/cherrytree.mo" % lang] ) )
	setup(
	   name = "CherryTree",
	   description = "Hierarchical Note Taking",
	   long_description = "A Hierarchical Note Taking Application, featuring Rich Text and Syntax Highlighting",
	   version = cons.VERSION,
	   author = "Giuseppe Penone",
	   author_email = "giuspen@gmail.com",
	   url = "http://www.giuspen.com/cherrytree/",
	   license = "GPL",
	   windows = [{"script": "cherrytree",
				   "icon_resources": [(1, "glade/cherrytree.ico")]
				   }],
	   options={"py2exe": {
				   "includes": "pango,cairo,pangocairo,atk,gobject,gtk,gtksourceview2,gio,enchant",
				   "dll_excludes": [
								 "libgdk-win32-2.0-0.dll",
								 "libgtk-win32-2.0-0.dll",
								 "libpangowin32-1.0-0.dll"],
						  }
				},
	   data_files = data_files,
	)
	print "remember to copy 7za.exe to the dist folder and relocate lib/enchant and share/enchant"
else:
	setup(
	   name = "CherryTree",
	   description = "Hierarchical Note Taking",
	   long_description = "A Hierarchical Note Taking Application, featuring Rich Text and Syntax Highlighting",
	   version = cons.VERSION,
	   author = "Giuseppe Penone",
	   author_email = "giuspen@gmail.com",
	   url = "http://www.giuspen.com/cherrytree/",
	   license = "GPL",
	   data_files = [
					  ("share/icons/hicolor/scalable/apps", ["glade/svg/cherrytree.svg"] ),
					  ("share/cherrytree/glade", glob.glob("glade/*.*") ),
					  ("share/cherrytree/language-specs", glob.glob("language-specs/*.lang") ),
					  ("share/cherrytree/modules", glob.glob("modules/*.py") ),
					  ("share/mime/packages", ["linux/cherrytree.xml"]),
					  ("share/mime-info", ["linux/cherrytree.mime", "linux/cherrytree.keys"]),
					  ("share/application-registry", ["linux/cherrytree.applications"]),
					  ("share/appdata", ["linux/cherrytree.appdata.xml"]),
					  ("share/man/man1", ["linux/cherrytree.1.gz"])
				   ],
	   cmdclass={
			'build': BuildData,
			'install_data': InstallData,
			'install': Install,
			'uninstall': Uninstall
		  },
	   distclass=CherryTreeDist
	)
	subprocess.call("update-desktop-database")

from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install
# For post-install script running using CustomInstallCommand, see:
# https://stackoverflow.com/a/45021666/3592884
import subprocess
def install_jupyter_extensions():
	print('About to run install_jupyter_extensions')
	process = subprocess.Popen(["./install_jupyter_extensions.sh"], stdout=subprocess.PIPE)
	for line in process.stdout:
		print(line.decode('utf8'))
	print('install_jupyter_extensions completed')
class CustomInstallCommand(install):
	def run(self):
		install.run(self)
#		install_jupyter_extensions()
with open('README.md') as f:
		long_description = f.read()
setup(
	name='viewscad',
	version='0.2.0',
	description='Jupyter renderer for the OpenSCAD & SolidPython constructive solid geometry systems',
	author='Nick Choly',
	author_email="nickcholy@gmail.com",
	url='https://github.com/nickc92/ViewSCAD',
	long_description=long_description,
	long_description_content_type='text/markdown',
	py_modules=['viewscad'],
	classifiers=[
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Development Status :: 4 - Beta",
		"Environment :: Other Environment",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Topic :: Scientific/Engineering :: Mathematics",
	],
	cmdclass={
		'install': CustomInstallCommand,
	},
	packages=find_packages(),
	install_requires=['jupyter', 'jupyterlab', 'ipywidgets', 'pythreejs', 'solidpython'],
	setup_requires=['jupyter', 'jupyterlab', 'ipywidgets', 'pythreejs', 'solidpython'],
)
