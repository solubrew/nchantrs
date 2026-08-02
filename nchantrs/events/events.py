"""#																			||
---  #																			||
<(META)>:  #																	||
        docid:   #																	||
        name: Nchantrs Python Excecution Document  #				||
        description: >  #															||

        expirary: <[expiration]>  #													||
        version: <[version]>  #														||
        path: <[LEXIvrs]>  #														||
        outline: <[outline]>  #														||
        authority: document|this  #													||
        security: sec|lvl2  #														||
        <(WT)>: -32  #																||
"""
from os.path import abspath, dirname, exists, join, expanduser
from kahndor import kahndor
import logging
from kahndor.thing import thingify, getName
logger = logging.getLogger(__name__)
from fxsquirl.fxsquirl import Chunker
ECHO_MODES = {0: QLineEdit.Normal, 1: QLineEdit.Password, 2: QLineEdit.PasswordEchoOnEdit, 3: QLineEdit.NoEcho}
VALIDATOR_TYPES = {0: None, 1: lambda: QIntValidator(self.validatorLineEdit), 2: lambda: QDoubleValidator(MIN_VALIDATOR_VALUE, MAX_VALIDATOR_VALUE, VALIDATOR_DECIMAL_PLACES, self.validatorLineEdit)}
ALIGNMENT_MODES = {0: Qt.AlignLeft, 1: Qt.AlignCenter, 2: Qt.AlignRight}
INPUT_MASKS = {0: '', 1: '+99 99 99 99 99;_', 2: '0000-00-00', 3: '>AAAAA-AAAAA-AAAAA-AAAAA-AAAAA;#'}
ACCESS_MODES = {0: False, 1: True}
MIN_VALIDATOR_VALUE = -999.0
MAX_VALIDATOR_VALUE = 999.0
VALIDATOR_DECIMAL_PLACES = 2
DEFAULT_INPUT_MASK_INDEX = 0
here = join(dirname(__file__), '')
there = abspath(join('../../..'))
version = '0.0.0.0.0.0'
log = False
pxcfg = f'{here}_data_/events.yaml'

class NchantdEventSet:
    """The EventSet is historical log of actions relative to an Nchantd
    Documnet"""

    def __init__(self, parent=None) -> None:
        """ """
        self.parent = parent
        if parent:
            cfg = parent.config
        self.config = kahndor.Instruct(pxcfg)
        self.config.select('NchantdEventSet').override(cfg)
        if not parent.newInstance:
            self.restoreEventSet()
        self.lastEvent = self.getLastEvent()
        logma.info(f'NchantdEventSet initialized')

    def store(self, event) -> None:
        logma.info(f'store called')
        return self

    def restoreEventSet(self) -> None:
        logma.info(f'restoreEventSet called')
        return self

    def restoreEvent(self) -> None:
        logma.info(f'restoreEvent called')
        return self

    def getLastEvent(self) -> None:
        """ """
        return event

class NchantdEvent:
    """An Event provides data to listeners and storage of the event"""

    def __init__(self) -> None:
        """ """
        logma.info(f'NchantdEvent initialized')

    def store(self, event) -> None:
        logma.info(f'store called')
        return self

    def currentCharFormatChanged(self, format) -> None:
        self.fontChanged(format.font())
        self.colorChanged(format.foreground().color())

    def cursorPositionChanged(self) -> None:
        self.alignmentChanged(self.textEdit.alignment())

    def clipboardDataChanged(self) -> None:
        self.actionPaste.setEnabled(len(QApplication.clipboard().text()) != 0)

    def about(self) -> None:
        QMessageBox.about(self, 'About', "This example demonstrates Qt's rich text editing facilities in action, providing an example document for you to experiment with.")

    def mergeFormatOnWordOrSelection(self, format) -> None:
        cursor = self.textEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        self.textEdit.mergeCurrentCharFormat(format)

    def fontChanged(self, font) -> None:
        self.comboFont.setCurrentIndex(self.comboFont.findText(QFontInfo(font).family()))
        self.comboSize.setCurrentIndex(self.comboSize.findText('%s' % font.pointSize()))
        self.actionTextBold.setChecked(font.bold())
        self.actionTextItalic.setChecked(font.italic())
        self.actionTextUnderline.setChecked(font.underline())

    def colorChanged(self, color) -> None:
        pix = QPixmap(16, 16)
        pix.fill(color)
        self.actionTextColor.setIcon(QIcon(pix))

    def alignmentChanged(self, alignment) -> None:
        if alignment & Qt.AlignLeft:
            self.actionAlignLeft.setChecked(True)
        elif alignment & Qt.AlignHCenter:
            self.actionAlignCenter.setChecked(True)
        elif alignment & Qt.AlignRight:
            self.actionAlignRight.setChecked(True)
        elif alignment & Qt.AlignJustify:
            self.actionAlignJustify.setChecked(True)

    def echoChanged(self, index) -> None:
        """Change echo mode based on index using dictionary lookup"""
        mode = ECHO_MODES.get(index, QLineEdit.Normal)
        self.echoLineEdit.setEchoMode(mode)

    def validatorChanged(self, index) -> None:
        """Change validator based on index using dictionary lookup"""
        validator_func = VALIDATOR_TYPES.get(index)
        if validator_func:
            self.validatorLineEdit.setValidator(validator_func())
        else:
            self.validatorLineEdit.setValidator(0)
        self.validatorLineEdit.clear()

    def alignmentChanged(self, index) -> None:
        """Change alignment based on index using dictionary lookup"""
        alignment = ALIGNMENT_MODES.get(index, Qt.AlignLeft)
        self.alignmentLineEdit.setAlignment(alignment)

    def inputMaskChanged(self, index) -> None:
        """Change input mask based on index using dictionary lookup"""
        mask = INPUT_MASKS.get(index, '')
        self.inputMaskLineEdit.setInputMask(mask)
        if index == 2:
            self.inputMaskLineEdit.setText('00000000')
            self.inputMaskLineEdit.setCursorPosition(0)

    def accessChanged(self, index) -> None:
        """Change access mode based on index using dictionary lookup"""
        read_only = ACCESS_MODES.get(index, False)
        self.accessLineEdit.setReadOnly(read_only)

    def update_format(self) -> None:
        """
        Update the font format toolbar/actions when a new text selection is made. This is neccessary to keep
        toolbars/etc. in sync with the current edit state.
        :return:
        """
        self.block_signals(self._format_actions, True)
        self.fonts.setCurrentFont(self.editor.currentFont())
        self.fontsize.setCurrentText(str(int(self.editor.fontPointSize())))
        self.italic_action.setChecked(self.editor.fontItalic())
        self.underline_action.setChecked(self.editor.fontUnderline())
        self.bold_action.setChecked(self.editor.fontWeight() == QFont.Bold)
        self.alignl_action.setChecked(self.editor.alignment() == Qt.AlignLeft)
        self.alignc_action.setChecked(self.editor.alignment() == Qt.AlignCenter)
        self.alignr_action.setChecked(self.editor.alignment() == Qt.AlignRight)
        self.alignj_action.setChecked(self.editor.alignment() == Qt.AlignJustify)
        self.block_signals(self._format_actions, False)