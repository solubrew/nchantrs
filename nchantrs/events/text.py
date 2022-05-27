#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid: ad51c0fb-cf03-4f75-8850-ee720fac479b
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
def bold():
	'''Set selected text to a bold font'''
	return
def capitalize():
	'''Change selected to a capitalized text'''
	return
def copy():
	'''Add selected text to clipboard'''
	return
def cut():
	'''Add selected text to clipboard and remove selected text from selected
		area '''
	return
def edit():
	''''''
	return
def findinapplication():
	'''Search through all connected workbooks for selected text '''
def findinsheet():
	'''Search through active sheet for selected text'''
	return
def findinworkbook():
	'''Search through active workbook for selected text'''
	return
def findText(self, word):
	if self.myeditor.find(word):
		self.statusBar().showMessage("'" + word + "' gefunden", 2000)
	else:
		self.myeditor.moveCursor(QTextCursor.Start)
		if self.myeditor.find(word):
			return
		else:
			 self.statusBar().showMessage("nichts gefunden", 3000)

def findreplaceinapplication():
	'''Search through all connected workbooks for selected text and replace with
	 	other text'''
	return
def findreplaceinsheet():
	'''Search through sheet for selected text and replace with other text'''
	return
def findreplaceinworkbook():
	'''Search through active workbook for selected text and replace with
	 	other text'''
	return
	def replaceAll(self):
		oldtext = self.findfield.text()
		newtext = self.replacefield.text()
		if not oldtext == "":
			h = self.myeditor.toHtml().replace(oldtext, newtext)
			self.myeditor.setText(h)
			self.setModified(True)
			self.statusBar().showMessage("alles ersetzt", 3000)
		else:
			self.statusBar().showMessage("nichts zu ersetzen", 3000)
	def replaceOne(self):
		oldtext = self.findfield.text()
		newtext = self.replacefield.text()
		if not oldtext == "":
			h = self.myeditor.toHtml().replace(oldtext, newtext, 1)
			self.myeditor.setText(h)
			self.setModified(True)
			self.statusBar().showMessage("1 ersetzt", 3000)
		else:
			self.statusBar().showMessage("nichts zu ersetzen", 3000)


def format():
	''' '''
	return
def italic():
	''' '''
	return
def linespacing1():
	'''Set the line spacing of selected text to 1'''
	return
def linespacing1_5():
	'''Set the line spacing of selected text to 1.5'''
	return
def linespacing2():
	'''Set the line spacing of selected text to 2''''
	return
def lowercase():
	''' '''
	return
def paste():
	'''Add object from clipboard to document at cursor location'''
	return
def pasteunformattedtext():
	'''Add object from clipboard to document at cursor location removing all
		formating of object'''
	return
def pastespecial():
	'''Open dialog to select formatting options'''
	return
def paragraphspacingincrease():
	''' '''
	return
def paragraphspacingdecrease():
	''' '''
	return
def propercase():
	''' '''
	return
def replaceThis(self):
	if not self.myeditor.textCursor().selectedText() == "":
		rtext = self.myeditor.textCursor().selectedText()
		dlg = QInputDialog(self, Qt.Dialog)
		dlg.setOkButtonText("Replace")
		text = dlg.getText(self, "Ersetzen","ersetze '" + rtext + "' durch:", QLineEdit.Normal, "")
		oldtext = self.myeditor.document().toPlainText()
		if not (text[0] == ""):
			newtext = oldtext.replace(rtext, text[0])
			self.myeditor.setPlainText(newtext)
			self.myeditor.document().setModified(True)
def selectall():
	''' '''
	return
def select():
	''' '''
	return
def sentencecase():
	''' '''
	return
def shadow():
	''
	return
def spacing():
	''' '''
	return
def strikethrough():
	''' '''
	return
def superscript():
	''' '''
	return
def subscript():
	''' '''
	return
def styles():
	''' '''
	return
def text():
	''' '''
	return
def textwrap():
	''' '''
	return
def togglecase():
	''' '''
	return
def trackchanges():
	''' '''
	return
def underline():
	''' '''
	return
def underlinedouble():
	''' '''
	return
def uppercase():
	''' '''
	return
