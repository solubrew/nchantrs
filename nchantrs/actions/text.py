# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid: ad51c0fb-cf03-4f75-8850-ee720fac479b
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
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from typing import Optional, Dict, List, Any, Tuple
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), '')  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, '_data_', '.yaml')

def bold() -> None:
	"""Set selected text to a bold font"""
	return

def capitalize() -> None:
	"""Change selected to a capitalized text"""
	return

def copy() -> None:
	"""Add selected text to clipboard"""
	return

def cut() -> None:
	"""Add selected text to clipboard and remove selected text from selected
		area """
	return

def edit() -> None:
	""""""
	return

def findinapplication() -> None:
	"""Search through all connected workbooks for selected text """

def findinsheet() -> None:
	"""Search through active sheet for selected text"""
	return

def findinworkbook() -> None:
	"""Search through active workbook for selected text"""
	return

def findText(self, word) -> None:
	if self.myeditor.find(word):
		self.statusBar().showMessage("'" + word + "' gefunden", 2000)
	else:
		self.myeditor.moveCursor(QTextCursor.Start)
		if self.myeditor.find(word):
			return
		else:
			 self.statusBar().showMessage("nichts gefunden", 3000)

def findreplaceinapplication() -> None:
	"""Search through all connected workbooks for selected text and replace with
	 	other text"""
	return

def findreplaceinsheet() -> None:
	"""Search through sheet for selected text and replace with other text"""
	return

def findreplaceinworkbook() -> None:
	"""Search through active workbook for selected text and replace with
	 	other text"""
	return

def replaceAll(self) -> None:
	oldtext = self.findfield.text()
	newtext = self.replacefield.text()
	if not oldtext == "":
		h = self.myeditor.toHtml().replace(oldtext, newtext)
		self.myeditor.setText(h)
		self.setModified(True)
		self.statusBar().showMessage("alles ersetzt", 3000)
	else:
		self.statusBar().showMessage("nichts zu ersetzen", 3000)
def replaceOne(self) -> None:
	oldtext = self.findfield.text()
	newtext = self.replacefield.text()
	if not oldtext == "":
		h = self.myeditor.toHtml().replace(oldtext, newtext, 1)
		self.myeditor.setText(h)
		self.setModified(True)
		self.statusBar().showMessage("1 ersetzt", 3000)
	else:
		self.statusBar().showMessage("nichts zu ersetzen", 3000)

def format() -> None:
	""" """
	return

def italic() -> None:
	""" """
	return

def line_spacing_1_0() -> None:
	"""Set the line spacing of selected text to 1"""
	return

def line_spacing_1_5() -> None:
	"""Set the line spacing of selected text to 1.5"""
	return

def line_spacing_2_0() -> None:
	"""Set the line spacing of selected text to 2"""
	return

def line_spacing_custom() -> None:
	"""Set the line spacing of selected text to 2"""
	return

def lowercase() -> None:
	""" """
	return

def paste() -> None:
	"""Add object from clipboard to document at cursor location"""
	return

def pasteunformattedtext() -> None:
	"""Add object from clipboard to document at cursor location removing all
		formating of object"""
	return

def pastespecial() -> None:
	"""Open dialog to select formatting options"""
	return

def paragraphspacingincrease() -> None:
	""" """
	return

def paragraphspacingdecrease() -> None:
	""" """
	return

def propercase() -> None:
	""" """
	return

def replaceThis(self) -> None:
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

def selectall() -> None:
	""" """
	return

def select() -> None:
	""" """
	return

def sentencecase() -> None:
	""" """
	return

def shadow() -> None:
	''
	return

def spacing() -> None:
	""" """
	return

def strikethrough() -> None:
	""" """
	return

def superscript() -> None:
	""" """
	return

def subscript() -> None:
	""" """
	return

def styles() -> None:
	""" """
	return

def text() -> None:
	""" """
	return

def textwrap() -> None:
	""" """
	return

def togglecase() -> None:
	""" """
	return

def trackchanges() -> None:
	""" """
	return

def underline() -> None:
	""" """
	return

def underlinedouble() -> None:
	""" """
	return

def uppercase() -> None:
	""" """
	return


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
