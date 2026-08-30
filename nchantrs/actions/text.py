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
import datetime as dt
import logging
from os.path import abspath, dirname, join

logger = logging.getLogger(__name__)
from typing import Any, Dict, List, Optional, Tuple

from kahndor import kahndor
from kahndor.logma import Logma

here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
DEFAULT_STATUS_MESSAGE_TIMEOUT = 3000
DEFAULT_FIND_TIMEOUT = 2000
pxcfg = join(here, '_data_', '.yaml')

def bold() -> None:
    logma.info('bold called')
    return self

def capitalize() -> None:
    logma.info('capitalize called')
    return self

def copy() -> None:
    logma.info('copy called')
    return self

def cut() -> None:
    logma.info('cut called')
    return self

def edit() -> None:
    logma.info('edit called')
    return self

def findinapplication() -> None:
    logma.info('findinapplication called')
    return self

def findinsheet() -> None:
    logma.info('findinsheet called')
    return self

def findinworkbook() -> None:
    logma.info('findinworkbook called')
    return self

def findText(self, word) -> None:
    if self.myeditor.find(word):
        self.statusBar().showMessage("'" + word + "' gefunden", 2000)
    else:
        self.myeditor.moveCursor(QTextCursor.Start)
        if self.myeditor.find(word):
            return
        else:
            self.statusBar().showMessage('nichts gefunden', DEFAULT_STATUS_MESSAGE_TIMEOUT)

def findreplaceinapplication() -> None:
    logma.info('findreplaceinapplication called')
    return self

def findreplaceinsheet() -> None:
    logma.info('findreplaceinsheet called')
    return self

def findreplaceinworkbook() -> None:
    logma.info('findreplaceinworkbook called')
    return self

def replaceAll(self) -> None:
    oldtext = self.findfield.text()
    newtext = self.replacefield.text()
    if not oldtext == '':
        h = self.myeditor.toHtml().replace(oldtext, newtext)
        self.myeditor.setText(h)
        self.setModified(True)
        self.statusBar().showMessage('alles ersetzt', DEFAULT_STATUS_MESSAGE_TIMEOUT)
    else:
        self.statusBar().showMessage('nichts zu ersetzen', DEFAULT_STATUS_MESSAGE_TIMEOUT)

def replaceOne(self) -> None:
    oldtext = self.findfield.text()
    newtext = self.replacefield.text()
    if not oldtext == '':
        h = self.myeditor.toHtml().replace(oldtext, newtext, 1)
        self.myeditor.setText(h)
        self.setModified(True)
        self.statusBar().showMessage('1 ersetzt', DEFAULT_STATUS_MESSAGE_TIMEOUT)
    else:
        self.statusBar().showMessage('nichts zu ersetzen', DEFAULT_STATUS_MESSAGE_TIMEOUT)

def format() -> None:
    logma.info('format called')
    return self

def italic() -> None:
    logma.info('italic called')
    return self

def line_spacing_1_0() -> None:
    logma.info('line_spacing_1_0 called')
    return self

def line_spacing_1_5() -> None:
    logma.info('line_spacing_1_5 called')
    return self

def line_spacing_2_0() -> None:
    logma.info('line_spacing_2_0 called')
    return self

def line_spacing_custom() -> None:
    logma.info('line_spacing_custom called')
    return self

def lowercase() -> None:
    logma.info('lowercase called')
    return self

def paste() -> None:
    logma.info('paste called')
    return self

def pasteunformattedtext() -> None:
    logma.info('pasteunformattedtext called')
    return self

def pastespecial() -> None:
    logma.info('pastespecial called')
    return self

def paragraphspacingincrease() -> None:
    logma.info('paragraphspacingincrease called')
    return self

def paragraphspacingdecrease() -> None:
    logma.info('paragraphspacingdecrease called')
    return self

def propercase() -> None:
    logma.info('propercase called')
    return self

def replaceThis(self) -> None:
    if not self.myeditor.textCursor().selectedText() == '':
        rtext = self.myeditor.textCursor().selectedText()
        dlg = QInputDialog(self, Qt.Dialog)
        dlg.setOkButtonText('Replace')
        text = dlg.getText(self, 'Ersetzen', "ersetze '" + rtext + "' durch:", QLineEdit.Normal, '')
        oldtext = self.myeditor.document().toPlainText()
        if not text[0] == '':
            newtext = oldtext.replace(rtext, text[0])
            self.myeditor.setPlainText(newtext)
            self.myeditor.document().setModified(True)

def selectall() -> None:
    logma.info('selectall called')
    return self

def select() -> None:
    logma.info('select called')
    return self

def sentencecase() -> None:
    logma.info('sentencecase called')
    return self

def shadow() -> None:
    logma.info('shadow called')
    return self

def spacing() -> None:
    logma.info('spacing called')
    return self

def strikethrough() -> None:
    logma.info('strikethrough called')
    return self

def superscript() -> None:
    logma.info('superscript called')
    return self

def subscript() -> None:
    logma.info('subscript called')
    return self

def styles() -> None:
    logma.info('styles called')
    return self

def text() -> None:
    logma.info('text called')
    return self

def textwrap() -> None:
    logma.info('textwrap called')
    return self

def togglecase() -> None:
    logma.info('togglecase called')
    return self

def trackchanges() -> None:
    logma.info('trackchanges called')
    return self

def underline() -> None:
    logma.info('underline called')
    return self

def underlinedouble() -> None:
    logma.info('underlinedouble called')
    return self

def uppercase() -> None:
    logma.info('uppercase called')
    return self
