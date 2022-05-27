



	def file_open(self):
		path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "HTML documents (*.html);Text documents (*.txt);All files (*.*)")
		try:
			with open(path, 'rU') as f:
				text = f.read()
		except Exception as e:
			self.dialog_critical(str(e))
		else:
			self.path = path
			# Qt will automatically try and guess the format as txt/html
			self.editor.setText(text)
			self.update_title()
	def file_save(self):
		if self.path is None:
			# If we do not have a path, we need to use Save As.
			return self.file_saveas()
		text = self.editor.toHtml() if splitext(self.path) in HTML_EXTENSIONS else self.editor.toPlainText()
		try:
			with open(self.path, 'w') as f:
				f.write(text)
		except Exception as e:
			self.dialog_critical(str(e))
	def file_saveas(self):
		path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "HTML documents (*.html);Text documents (*.txt);All files (*.*)")
		if not path:
			# If dialog is cancelled, will return ''
			return
		text = self.editor.toHtml() if splitext(path) in HTML_EXTENSIONS else self.editor.toPlainText()
		try:
			with open(path, 'w') as f:
				f.write(text)
		except Exception as e:
			self.dialog_critical(str(e))
		else:
			self.path = path
			self.update_title()
	def file_print(self):
		dlg = QPrintDialog()
		if dlg.exec_():
			self.editor.print_(dlg.printer())
	def newFile(self):
		if self.maybeSave():
			self.myeditor.clear()
			self.setCurrentFile('')
	def open(self):
		if self.maybeSave():
			fileName, _ = QFileDialog.getOpenFileName(self, "Datei öffnen", QDir.homePath() + "/Dokumente", "Text Dateien (*.txt *.csv *.sh *.py) ;; alle Dateien (*.*)")
			if fileName:
				self.loadFile(fileName)
			else:
				self.statusBar().showMessage("abgebrochen", 3000)
	def save(self):
		if not self.myeditor.toPlainText() == "":
			if self.myeditor.document().isModified():
				if self.curFile:
					return self.saveFile(self.curFile)
					self.setCurrentFile(fileName)
				else:
					return self.saveAs()
			else:
				self.statusBar().showMessage("Datei '" + self.curFile + "' bereits gespeichert", 3000)
		else:
			self.statusBar().showMessage("kein Text")
	def saveAs(self):
		if not self.myeditor.toPlainText() == "":
			if self.curFile:
				fileName, _ = QFileDialog.getSaveFileName(self, "Speichern als...", self.curFile, "Text Dateien (*.txt)")
			else:
				fileName, _ = QFileDialog.getSaveFileName(self, "Speichern als...", QDir.homePath() + "/Dokumente/Unbenannt.txt", "Text Dateien (*.txt)" )
			if fileName:
				return self.saveFile(fileName)
			return False
		else:
			self.statusBar().showMessage("kein Text")

	def openRecentFile(self):
		action = self.sender()
		if action:
			if (self.maybeSave()):
				self.loadFile(action.data())
	def maybeSave(self):
		if self.myeditor.document().isModified():
			ret = QMessageBox.warning(self, "QTextEdit Meldung",
					"Das Dokument wurde geändert.\nSollen die Änderungen gespeichert werden?",
					QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, defaultButton = QMessageBox.Save)
			if ret == QMessageBox.Save:
				return self.save()
			if ret == QMessageBox.Cancel:
				return False
		return True
	def loadFile(self, fileName):
		file = QFile(fileName)
		if not file.open(QFile.ReadOnly | QFile.Text):
			QMessageBox.warning(self, "Meldung",
					"Cannot read file %s:\n%s." % (fileName, file.errorString()))
			return
		infile = QTextStream(file)
		QApplication.setOverrideCursor(Qt.WaitCursor)
		self.myeditor.setPlainText(infile.readAll())
		QApplication.restoreOverrideCursor()
		self.setCurrentFile(fileName)
		self.statusBar().showMessage("Datei '" +  fileName + "' geladen", 3000)
	def saveFile(self, fileName):
		file = QFile(fileName)
		if not file.open(QFile.WriteOnly | QFile.Text):
			QMessageBox.warning(self, "Message",
					"Cannot write file %s:\n%s." % (fileName, file.errorString()))
			return False
		outfile = QTextStream(file)
		QApplication.setOverrideCursor(Qt.WaitCursor)
		outfile << self.myeditor.toPlainText()
		QApplication.restoreOverrideCursor()
		self.setCurrentFile(fileName);
		self.statusBar().showMessage("Datei '" +  fileName + "' gespeichert", 3000)
		return True
	def setCurrentFile(self, fileName):
		self.curFile = fileName
		self.myeditor.document().setModified(False)
		self.setWindowModified(False)
		if self.curFile:
			self.setWindowTitle(self.strippedName(self.curFile) + "[*]")
		else:
			self.setWindowTitle('Unbenannt.txt' + "[*]")
		files = self.settings.value('recentFileList', [])
		if not files == "":
			try:
				files.remove(fileName)
			except ValueError:
				pass
			if fileName:
				files.insert(0, fileName)
				del files[self.MaxRecentFiles:]
				self.settings.setValue('recentFileList', files)
				self.updateRecentFileActions()
	def updateRecentFileActions(self):
		mytext = ""
		files = self.settings.value('recentFileList', [])
		numRecentFiles = min(len(files), self.MaxRecentFiles)
#		if not files == "":
		for i in range(numRecentFiles):
			text = "&%d %s" % (i + 1, self.strippedName(files[i]))
			self.recentFileActs[i].setText(text)
			self.recentFileActs[i].setData(files[i])
			self.recentFileActs[i].setVisible(True)
			self.recentFileActs[i].setIcon(QIcon.fromTheme("text-x-generic"))
		for j in range(numRecentFiles, self.MaxRecentFiles):
			self.recentFileActs[j].setVisible(False)
		self.separatorAct.setVisible((numRecentFiles > 0))
	def clearRecentFiles(self, fileName):
		self.settings.clear()
		self.updateRecentFileActions()
