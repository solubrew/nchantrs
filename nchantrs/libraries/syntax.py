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
from os.path import dirname, join
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
HERE = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
if not log:
    logma.off()
PXCFG = join(HERE, '_data_', '.yaml')

def format(color, style='') -> None:
    """Return a QTextCharFormat with the given attributes.
    """
    _color = pyqt.QColor()
    _color.setNamedColor(color)
    _format = pyqt.QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(pyqt.QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)
    if 'italicbold' in style:
        _format.setFontItalic(True)
        _format.setFontWeight(Qpyqt.Font.Bold)
    return _format
mybrawn = '#7E5916'
STYLES = {'keyword': format('#2C2CC8', 'bold'), 'operator': format('darkred'), 'brace': format('darkred'), 'defclass': format('#cc0000', 'bold'), 'classes': format('#cc0000', 'bold'), 'Qtclass': format('black', 'bold'), 'string': format(mybrawn), 'string2': format('#42923b', 'italic'), 'comment': format('#42923b', 'italic'), 'self': format('#D63030', 'italicbold'), 'selfnext': format('#2e3436', 'bold'), 'Qnext': format('#2e3436', 'bold'), 'numbers': format('#C82C2C')}
NOT_FOUND = -1

class Highlighter(pyqt.QSyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """
    keywords = ['and', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'exec', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'not', 'or', 'pass', 'print', 'raise', 'return', 'super', 'try', 'while', 'yield', 'None', 'True', 'False']
    operators = ['=', '==', '!=', '<', '<=', '>', '>=', '\\+', '-', '\\*', '/', '//', '\\%', '\\*\\*', '\\+=', '-=', '\\*=', '/=', '\\%=', '\\^', '\\|', '\\&', '\\~', '>>', '<<']
    braces = ['\\{', '\\}', '\\(', '\\)', '\\[', '\\]']

    def __init__(self, document) -> None:
        pyqt.QSyntaxHighlighter.__init__(self, document)
        self.tri_single = (pyqt.QRegExp("'''"), 1, STYLES['string2'])
        self.tri_double = (pyqt.QRegExp('"""'), 2, STYLES['string2'])
        rules = []
        rules += [('\\b%s\\b' % w, 0, STYLES['keyword']) for w in Highlighter.keywords]
        rules += [('%s' % o, 0, STYLES['operator']) for o in Highlighter.operators]
        rules += [('%s' % b, 0, STYLES['brace']) for b in Highlighter.braces]
        rules += [('\\b[+-]?[0-9]+[lL]?\\b', 0, STYLES['numbers']), ('\\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\\b', 0, STYLES['numbers']), ('\\b[+-]?[0-9]+(?:\\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\\b', 0, STYLES['numbers']), ('\\bself\\b', 0, STYLES['self']), ('"[^"\\\\]*(\\\\.[^"\\\\]*)*"', 0, STYLES['string']), ("'[^'\\\\]*(\\\\.[^'\\\\]*)*'", 0, STYLES['string']), ('\\bdef\\b\\s*(\\w+)', 1, STYLES['defclass']), ('\\bself\\b)', 1, STYLES['selfnext']), ('\\b[Q.]\\b\\s*(\\w+)', 1, STYLES['Qnext']), ('\\bclass\\b\\s*(\\w+)', 1, STYLES['classes']), ('#[^\\n]*', 0, STYLES['comment'])]
        self.rules = [(pyqt.QRegExp(pat), index, fmt) for pat, index, fmt in rules]

    def highlightBlock(self, text) -> None:
        """Apply syntax highlighting to the given block of text.
        """
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)
            while index >= 0:
                index = expression.pos(nth)
                if index == NOT_FOUND:
                    break
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style) -> None:
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        else:
            start = delimiter.indexIn(text)
            add = delimiter.matchedLength()
        while start >= 0:
            end = delimiter.indexIn(text, start + add)
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            self.setFormat(start, length, style)
            start = delimiter.indexIn(text, start + length)
        if self.currentBlockState() == in_state:
            return True
        else:
            return False