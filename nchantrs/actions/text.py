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
from os.path import abspath, dirname, join
import datetime as dt
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from typing import Optional, Dict, List, Any, Tuple
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
DEFAULT_STATUS_MESSAGE_TIMEOUT = 3000
DEFAULT_FIND_TIMEOUT = 2000
pxcfg = join(here, '_data_', '.yaml')

def bold() -> None:
    logma.info(f'bold called')
    return self

def capitalize() -> None:
    logma.info(f'capitalize called')
    return self

def copy() -> None:
    logma.info(f'copy called')
    return self

def cut() -> None:
    logma.info(f'cut called')
    return self

def edit() -> None:
    logma.info(f'edit called')
    return self

def findinapplication() -> None:
    logma.info(f'findinapplication called')
    return self

def findinsheet() -> None:
    logma.info(f'findinsheet called')
    return self

def findinworkbook() -> None:
    logma.info(f'findinworkbook called')
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
    logma.info(f'findreplaceinapplication called')
    return self

def findreplaceinsheet() -> None:
    logma.info(f'findreplaceinsheet called')
    return self

def findreplaceinworkbook() -> None:
    logma.info(f'findreplaceinworkbook called')
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
    logma.info(f'format called')
    return self

def italic() -> None:
    logma.info(f'italic called')
    return self

def line_spacing_1_0() -> None:
    logma.info(f'line_spacing_1_0 called')
    return self

def line_spacing_1_5() -> None:
    logma.info(f'line_spacing_1_5 called')
    return self

def line_spacing_2_0() -> None:
    logma.info(f'line_spacing_2_0 called')
    return self

def line_spacing_custom() -> None:
    logma.info(f'line_spacing_custom called')
    return self

def lowercase() -> None:
    logma.info(f'lowercase called')
    return self

def paste() -> None:
    logma.info(f'paste called')
    return self

def pasteunformattedtext() -> None:
    logma.info(f'pasteunformattedtext called')
    return self

def pastespecial() -> None:
    logma.info(f'pastespecial called')
    return self

def paragraphspacingincrease() -> None:
    logma.info(f'paragraphspacingincrease called')
    return self

def paragraphspacingdecrease() -> None:
    logma.info(f'paragraphspacingdecrease called')
    return self

def propercase() -> None:
    logma.info(f'propercase called')
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
    logma.info(f'selectall called')
    return self

def select() -> None:
    logma.info(f'select called')
    return self

def sentencecase() -> None:
    logma.info(f'sentencecase called')
    return self

def shadow() -> None:
    logma.info(f'shadow called')
    return self

def spacing() -> None:
    logma.info(f'spacing called')
    return self

def strikethrough() -> None:
    logma.info(f'strikethrough called')
    return self

def superscript() -> None:
    logma.info(f'superscript called')
    return self

def subscript() -> None:
    logma.info(f'subscript called')
    return self

def styles() -> None:
    logma.info(f'styles called')
    return self

def text() -> None:
    logma.info(f'text called')
    return self

def textwrap() -> None:
    logma.info(f'textwrap called')
    return self

def togglecase() -> None:
    logma.info(f'togglecase called')
    return self

def trackchanges() -> None:
    logma.info(f'trackchanges called')
    return self

def underline() -> None:
    logma.info(f'underline called')
    return self

def underlinedouble() -> None:
    logma.info(f'underlinedouble called')
    return self

def uppercase() -> None:
    logma.info(f'uppercase called')
    return self