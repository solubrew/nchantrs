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
import datetime as dt

import logging
# ======================================3rd Party Library Modules=====================================================||

logger = logging.getLogger(__name__)

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from typing import Optional, Dict, List, Any, Tuple
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), '')  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, """_data_""", """.yaml""")


class ActionBuilder():
	def __init__(self, cfg=None) -> None:
		self.config = cfg

	def buildAction(self, cfg) -> None:
		"""Dynamically build action to be triggered from menu item"""  # ||
		icon = pyqt.QIcon(cfg['icon_txt'])
		kwargs = {}
		if 'shortcut_txt' in cfg.keys() and cfg['shortcut_txt'] != None:  # ||
			kwargs['shortcut'] = cfg['shortcut_txt']
		if 'tip_txt' in cfg.keys() and cfg['tip_txt'] != None:  # ||
			kwargs['statusTip'] = cfg['tip_txt']
		if 'fx_txt' in cfg.keys() and cfg['fx_txt'] != None and cfg['fx_txt'] not in ['', ]:
			if log: logma.info(f"Function {cfg['fx_txt']}")
			try:
				kwargs['triggered'] = thingify(cfg['fx_txt'])
			except Exception as e:
				kwargs['triggered'] = None

		return pyqt.QAction(icon, cfg['name_txt'], self.parent, **kwargs)  # ||



	def load_scheme(self, filename) -> None:
		"""
		Load a scheme from a file (`filename`) into the current
		document, updates the recent scheme list and the loaded scheme path
		property.
		"""
		new_scheme = self.new_scheme_from(filename)
		if new_scheme is not None:
			self.set_new_scheme(new_scheme)
			scheme_doc_widget = self.current_document()
			scheme_doc_widget.setPath(filename)
			self.add_recent_scheme(new_scheme.title, filename)
			if not self.freeze_action.isChecked():
				# activate the default window group.
				scheme_doc_widget.activateDefaultWindowGroup()
	def load_scheme_xml(self, xml) -> None:
		new_scheme = widgetsscheme.WidgetsScheme(parent=self)
		scheme_load(new_scheme, StringIO(xml))
		self.set_new_scheme(new_scheme)
		return QDialog.Accepted

	def create_new_window(self) -> None:
		# type: () -> CanvasMainWindow
		"""Create a new top level CanvasMainWindow instance.
		The window is positioned slightly offset to the originating window
		(`self`).
		Note
		----
		The window has `Qt.WA_DeleteOnClose` flag set. If this flag is unset
		it is the callers responsibility to explicitly delete the widget (via
		`deleteLater` or `sip.delete`).
		Returns
		-------
		window: CanvasMainWindow"""
		window = CanvasMainWindow()
		window.setAttribute(Qt.WA_DeleteOnClose)
		window.setGeometry(self.geometry().translated(20, 20))
		window.setStyleSheet(self.styleSheet())
		window.set_widget_registry(self.widget_registry)
		window.restoreState(self.saveState(self.SETTINGS_VERSION), self.SETTINGS_VERSION)
		window.set_tool_dock_expanded(self.dock_widget.expanded())
		window.set_float_widgets_on_top_enabled(self.float_widgets_on_top_action.isChecked())
		logview = window.log_view()  # type: OutputView
		te = logview.findChild(QPlainTextEdit)
		doc = self.log_view().findChild(QPlainTextEdit).document()
		# first clone the existing document and set it on the new instance
		doc = doc.clone(parent=te)  # type: QTextDocument
		doc.setDocumentLayout(QPlainTextDocumentLayout(doc))
		te.setDocument(doc)
		# route the stdout/err if possible
		stdout, stderr = sys.stdout, sys.stderr
		if isinstance(stdout, TextStream):
			stdout.stream.connect(logview.write)
		if isinstance(stderr, TextStream):
			err_formater = logview.formated(color=Qt.red)
			stderr.stream.connect(err_formater.write)
		CanvasMainWindow._instances.append(window)
		window.destroyed.connect(
			lambda: CanvasMainWindow._instances.remove(window))
		return window



def about(app, cfg) -> None:
	"""Launch dialog with information about application"""
	launch = NchantdDialog(app, cfg).initWidget()
	return

def add_tab(app, cfg) -> None:
	""""""
	app.model.add_tab()
	return

def mngBookmarks(self) -> None:
	""""""
	return self

def admin() -> None:
	"""General administration menu for dedicated applications """
	return

def close(app) -> None:
	"""Close workbook"""
	return

def exit(app, ce) -> None:
	""" """
	app.fileQuit()

def file() -> None:
	""""""
	return

def help() -> None:
	"""Launch dialog with connections to help information"""
	return

def insert() -> None:
	"""Insert objects such as images into rich text documents"""
	return

def newFile(path) -> None:
	"""Create a new workbook"""
	return

def newRecord() -> None:
	""" """

	return

def open(path) -> None:
	"""Launch dialog to select document from file system and then open selected
		document"""
	return

def paste(app) -> None:
	""" """
	return

def preferences(app, cfg: dict={}) -> None:
	"""Launch dialog for editing application prefrences"""
	return

def redo() -> None:
	"""Advance document by running foward in the log"""
	return

def save() -> None:
	"""Get active widget and save"""
	return

def saveall() -> None:
	"""Build a list of all widgets within application, cycle through and save as
		needed"""
	return

def saveas(path, data) -> None:
	"""Open dialog to provide a new file name and path for saving current
		document then write data to new location.  Check for overwrite. Then
		make new document the current document"""
	return

def savecopy() -> None:
	"""Open dialog to provide a new file name and path for saving current
		document then write data to new location.  Check for overwrite. Then
		keep the current document"""
	return

def undo() -> None:
	"""Move document back in time by running the log in reverse"""
	return

def aboutApplication(self) -> None:
	""""""
	text = """For Help Contact: Joe Brewer at joebrewer@solutionsbrewer.com"""
	return text
def addBookmark(self) -> None:
	""""""
	linenumber = self.getLineNumber()
	linetext = self.editor.textCursor().block().text().strip()
	self.bookmarks.addItem(linetext, linenumber)
	return self
def bookmarks(self) -> None:
	""""""
	return self
def closeEvent(self, ce) -> None:
	self.fileQuit()
def copySelection(self) -> None:
	""""""
	return self
def createTabDocument(self) -> None:
	""""""
	return self
def cutSelection(self) -> None:
	""""""
	return self
def exitAccess(self) -> None:
	""""""
	return self
def exitCherryTree(self) -> None:
	""""""
	return self
def exitCSV(self) -> None:
	""""""
	return self
def exitExcel(self) -> None:
	""""""
	return self
def exitGui(self) -> None:
	""""""
	return self
def expCSV(self) -> None:
	""""""
	return self
def fileQuit(self) -> None:
	self.close()
def findData(self) -> None:
	""""""
	return self
def linkData(self) -> None:
	""""""
	return self
def loadData(self) -> None:
	""""""
	return self
def loadDevMode(self) -> None:
	""""""
	return self

def newFile(self) -> None:
	""""""
	self.newAct = QAction("&New", self, shortcut=QKeySequence.New, statusTip="new file", triggered=self.newFile)
	self.newAct.setIcon(QIcon.fromTheme(self.root + "/icons/new24"))
	#create a new databse file
	if self.maybeSave():
		self.editor.clear()
		self.editor.setPlainText(self.mainText)
		self.filename = ""
		self.setModified(False)
		self.editor.moveCursor(self.cursor.End)
		self.statusBar().showMessage("new File created.")
		self.editor.setFocus()
		self.bookmarks.clear()
		self.setWindowTitle("new File[*]")
	return self
def new_workflow_window(self) -> None:
	# type: () -> None
	"""Create and show a new CanvasMainWindow instance."""
	newwindow = self.create_new_window()
	newwindow.raise_()
	newwindow.show()
	newwindow.activateWindow()
	settings = QSettings()
	show = settings.value("schemeinfo/show-at-new-scheme", True, type=bool)
	if show:
		newwindow.show_scheme_properties()
def newAppContainer(self, cfgs=None) -> None:
	""""""
	self.nodes.append(appContainer, cfgs)
	return self
def newCanvas(self) -> None:
	""""""
	self.nodes.append(canvasContainer, cfgs)
	return self
def newChart(self) -> None:
	""""""
	self.nodes.append(chartContainer, cfgs)
	return self
def newDashboard(self) -> None:
	""""""
	self.nodes.append(dashContainer, cfgs)
	return self
def newEditor(self) -> None:
	""""""
	self.nodes.append(editorContainer, cfgs)
	return self
def newSheet(self) -> None:
	""""""
	self.nodes.append(sheetContainer, cfgs)
	return self

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
