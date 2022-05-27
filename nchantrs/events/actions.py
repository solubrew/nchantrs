#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid: <^(UUID)^>
	name:
	description: >
	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
from os.path import abspath, dirname, exists, join
#=======================================================================||

#=======================================================================||
here = join(dirname(__file__),'')#						||
there = abspath(join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
qss = f'{here}_data_/style.qss'
#=======================================================================||
def about():
	'''Launch dialog with information about application'''
	return
def admin():
	'''General administration menu for dedicated applications '''
	return
def close(app):
	'''Close workbook'''
	app.close()
	return
def exit(app, ce):
	''' '''
	app.fileQuit()
def file():
	''''''
	return
def help():
	'''Launch dialog with connections to help information'''
	return
def insert():
	'''Insert objects such as images into rich text documents'''
	return
def newFile(path):
	'''Create a new workbook'''
	yonql.doc(path).touch()
	return
def newRecord():
	''' '''

	return
def open(path):
	'''Launch dialog to select document from file system and then open selected
		document'''
	return next(yonql.doc(path).read()).dikt
def paste(app):
	''' '''
	return
def preferences(app, cfg: dict={}):
	'''Launch dialog for editing application prefrences'''
	dlog = Preferences(app, cfg)
	return
def redo():
	'''Advance document by running foward in the log'''
	return
def save():
	'''Get active widget and save'''
	return
def saveall():
	'''Build a list of all widgets within application, cycle through and save as
		needed'''
	return
def saveas(path, data):
	'''Open dialog to provide a new file name and path for saving current
		document then write data to new location.  Check for overwrite. Then
		make new document the current document'''
	return
def savecopy():
	'''Open dialog to provide a new file name and path for saving current
		document then write data to new location.  Check for overwrite. Then
		keep the current document'''
	return
def undo():
	'''Move document back in time by running the log in reverse'''
	return
	def createActions(self):
		self.newAct = QAction(QIcon.fromTheme('document-new'), "&Neu", self,
				shortcut=QKeySequence.New, statusTip="neue Datei erstellen",
				triggered=self.newFile)
		self.openAct = QAction(QIcon.fromTheme('document-open'), "Öffnen.",
				self, shortcut=QKeySequence.Open,
				statusTip="Datei öffnen", triggered=self.open)
		self.saveAct = QAction(QIcon.fromTheme('document-save'), "Speichern", self,
				shortcut=QKeySequence.Save,
				statusTip="Dokument speichern", triggered=self.save)
		self.saveAsAct = QAction(QIcon.fromTheme('document-save-as'),"Speichern als...", self,
				shortcut=QKeySequence.SaveAs,
				statusTip="Dokument unter neuem Namen speichern",
				triggered=self.saveAs)
		self.exitAct = QAction(QIcon.fromTheme('application-exit'),"Beenden", self, shortcut="Ctrl+Q",
				statusTip="Programm beenden", triggered=self.close)
		self.cutAct = QAction(QIcon.fromTheme('edit-cut'), "Ausschneiden", self,
				shortcut=QKeySequence.Cut,
				statusTip="Ausschneiden",
				triggered=self.myeditor.cut)
		self.copyAct = QAction(QIcon.fromTheme('edit-copy'), "Kopieren", self,
				shortcut=QKeySequence.Copy,
				statusTip="Kopieren",
				triggered=self.myeditor.copy)
		self.pasteAct = QAction(QIcon.fromTheme('edit-paste'), "Einfügen",
				self, shortcut=QKeySequence.Paste,
				statusTip="Einfügen",
				triggered=self.myeditor.paste)
		self.undoAct = QAction(QIcon.fromTheme('edit-undo'), "Rückgängig",
				self, shortcut=QKeySequence.Undo,
				statusTip="Rückgängig",
				triggered=self.myeditor.undo)
		self.redoAct = QAction(QIcon.fromTheme('edit-redo'), "Wiederholen",
				self, shortcut=QKeySequence.Redo,
				statusTip="Wiederholen",
				triggered=self.myeditor.redo)
		self.aboutAct = QAction(QIcon.fromTheme('help-about'),"Info", self,
				statusTip="über QTextEdit",
				triggered=self.about)
		self.aboutQtAct = QAction(QIcon.fromTheme('help-about'),"über Qt", self,
				statusTip="über Qt",
				triggered=QApplication.instance().aboutQt)
		self.repAllAct = QPushButton("alles ersetzen")
		self.repAllAct.setIcon(QIcon.fromTheme("edit-find-and-replace"))
		self.repAllAct.setStatusTip("alles ersetzen")
		self.repAllAct.clicked.connect(self.replaceAll)
		self.cutAct.setEnabled(False)
		self.copyAct.setEnabled(False)
		self.myeditor.copyAvailable.connect(self.cutAct.setEnabled)
		self.myeditor.copyAvailable.connect(self.copyAct.setEnabled)
		self.undoAct.setEnabled(False)
		self.redoAct.setEnabled(False)
		self.myeditor.undoAvailable.connect(self.undoAct.setEnabled)
		self.myeditor.redoAvailable.connect(self.redoAct.setEnabled)
		### print preview
		self.printPreviewAct = QAction("Druckvorschau", self, shortcut=QKeySequence.Print,statusTip="Druckvorschau", triggered=self.handlePrintPreview)
		self.printPreviewAct.setIcon(QIcon.fromTheme("document-print-preview"))
		### print
		self.printAct = QAction("Drucken", self, shortcut=QKeySequence.Print,statusTip="Dokument drucken", triggered=self.handlePrint)
		self.printAct.setIcon(QIcon.fromTheme("document-print"))
		for i in range(self.MaxRecentFiles):
			self.recentFileActs.append(
				   QAction(self, visible=False,
							triggered=self.openRecentFile))
class actionBuilder():
	def __init__(self, cfg=None):
		self.config = cfg
	def aboutApplication(self):
		''
		text = 'For Help Contact: Joe Brewer at joebrewer@solutionsbrewer.com'
		return text
	def addBookmark(self):
		''
		linenumber = self.getLineNumber()
		linetext = self.editor.textCursor().block().text().strip()
		self.bookmarks.addItem(linetext, linenumber)
		return self
	def bookmarks(self):
		''
		return self
	def closeEvent(self, ce):
		self.fileQuit()
	def copySelection(self):
		''
		return self
	def createTabDocument(self):
		''
		return self
	def cutSelection(self):
		''
		return self
	def exitAccess(self):
		''
		return self
	def exitCherryTree(self):
		''
		return self
	def exitCSV(self):
		''
		return self
	def exitExcel(self):
		''
		return self
	def exitGui(self):
		''
		return self
	def expCSV(self):
		''
		return self
	def fileQuit(self):
		self.close()
	def findData(self):
		''
		return self
	def linkData(self):
		''
		return self
	def loadData(self):
		''
		return self
	def loadDevMode(self):
		''
		return self
	def load_scheme(self, filename):
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
	def load_scheme_xml(self, xml):
		new_scheme = widgetsscheme.WidgetsScheme(parent=self)
		scheme_load(new_scheme, StringIO(xml))
		self.set_new_scheme(new_scheme)
		return QDialog.Accepted
	def mngBookmarks(self):
		''
		return self
	def create_new_window(self):
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
	def newFile(self):
		''
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
	def new_workflow_window(self):
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
	def newAppContainer(self, cfgs=None):
		''
		self.nodes.append(appContainer, cfgs)
		return self
	def newCanvas(self):
		''
		self.nodes.append(canvasContainer, cfgs)
		return self
	def newChart(self):
		''
		self.nodes.append(chartContainer, cfgs)
		return self
	def newDashboard(self):
		''
		self.nodes.append(dashContainer, cfgs)
		return self
	def newEditor(self):
		''
		self.nodes.append(editorContainer, cfgs)
		return self
	def newSheet(self):
		''
		self.nodes.append(sheetContainer, cfgs)
		return self
