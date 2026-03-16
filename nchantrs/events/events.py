# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Nchantrs@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""  #																			||
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
"""  # 																			||
# -*- coding: utf-8 -*-#														||
# ================================Core Modules===================================||
from os.path import abspath, dirname, exists, join, expanduser

# ===============================================================================||
from condor import condor
from condor.thing import thingify, getName
from fxsquirl.fxsquirl import Chunker

# ====================================================================================================================||
# Constants for magic number replacement
MIN_VALIDATOR_VALUE = -999.0
MAX_VALIDATOR_VALUE = 999.0
VALIDATOR_DECIMAL_PLACES = 2
DEFAULT_INPUT_MASK_INDEX = 0
# ===============================================================================||
here = join(dirname(__file__), "")  # 												||
there = abspath(join("../../.."))  # 												||set path at pheonix level
version = "0.0.0.0.0.0"  # 														||
log = False
# ===============================================================================||
pxcfg = f"{here}_data_/events.yaml"


class NchantdEventSet:
    """The EventSet is historical log of actions relative to an Nchantd
    Documnet"""

    def __init__(self, parent=None) -> None:
        """ """
        self.parent = parent
        if parent:
            cfg = parent.config
        self.config = condor.Instruct(pxcfg)
        self.config.select("NchantdEventSet").override(cfg)
        if not parent.newInstance:
            self.restoreEventSet()
        self.lastEvent = self.getLastEvent()

    def store(self, event) -> None:
        """ """
        return self

    def restoreEventSet(self) -> None:
        """ """
        return self

    def restoreEvent(self) -> None:
        """ """
        return self

    def getLastEvent(self) -> None:
        """ """
        return event


class NchantdEvent:
    """An Event provides data to listeners and storage of the event"""

    def __init__(self) -> None:
        """ """

    def store(self, event) -> None:
        """ """
        return self

    def currentCharFormatChanged(self, format) -> None:
        self.fontChanged(format.font())
        self.colorChanged(format.foreground().color())

    def cursorPositionChanged(self) -> None:
        self.alignmentChanged(self.textEdit.alignment())

    def clipboardDataChanged(self) -> None:
        self.actionPaste.setEnabled(len(QApplication.clipboard().text()) != 0)

    def about(self) -> None:
        QMessageBox.about(
            self,
            "About",
            "This example demonstrates Qt's rich text editing facilities "
            "in action, providing an example document for you to "
            "experiment with.",
        )

    def mergeFormatOnWordOrSelection(self, format) -> None:
        cursor = self.textEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        self.textEdit.mergeCurrentCharFormat(format)

    def fontChanged(self, font) -> None:
        self.comboFont.setCurrentIndex(self.comboFont.findText(QFontInfo(font).family()))
        self.comboSize.setCurrentIndex(self.comboSize.findText("%s" % font.pointSize()))
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
        if index == 0:
            self.echoLineEdit.setEchoMode(QLineEdit.Normal)
        elif index == 1:
            self.echoLineEdit.setEchoMode(QLineEdit.Password)
        elif index == 2:
            self.echoLineEdit.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        elif index == 3:
            self.echoLineEdit.setEchoMode(QLineEdit.NoEcho)

    def validatorChanged(self, index) -> None:
        if index == 0:
            self.validatorLineEdit.setValidator(0)
        elif index == 1:
            self.validatorLineEdit.setValidator(QIntValidator(self.validatorLineEdit))
        elif index == 2:
            self.validatorLineEdit.setValidator(QDoubleValidator(
                MIN_VALIDATOR_VALUE, MAX_VALIDATOR_VALUE, 
                VALIDATOR_DECIMAL_PLACES, self.validatorLineEdit))
        self.validatorLineEdit.clear()

    def alignmentChanged(self, index) -> None:
        if index == 0:
            self.alignmentLineEdit.setAlignment(Qt.AlignLeft)
        elif index == 1:
            self.alignmentLineEdit.setAlignment(Qt.AlignCenter)
        elif index == 2:
            self.alignmentLineEdit.setAlignment(Qt.AlignRight)

    def inputMaskChanged(self, index) -> None:
        if index == 0:
            self.inputMaskLineEdit.setInputMask("")
        elif index == 1:
            self.inputMaskLineEdit.setInputMask("+99 99 99 99 99;_")
        elif index == 2:
            self.inputMaskLineEdit.setInputMask("0000-00-00")
            self.inputMaskLineEdit.setText("00000000")
            self.inputMaskLineEdit.setCursorPosition(0)
        elif index == 3:
            self.inputMaskLineEdit.setInputMask(">AAAAA-AAAAA-AAAAA-AAAAA-AAAAA;#")

    def accessChanged(self, index) -> None:
        if index == 0:
            self.accessLineEdit.setReadOnly(False)
        elif index == 1:
            self.accessLineEdit.setReadOnly(True)

    def update_format(self) -> None:
        """
        Update the font format toolbar/actions when a new text selection is made. This is neccessary to keep
        toolbars/etc. in sync with the current edit state.
        :return:
        """
        # Disable signals for all format widgets, so changing values here does not trigger further formatting.
        self.block_signals(self._format_actions, True)
        self.fonts.setCurrentFont(self.editor.currentFont())
        # Nasty, but we get the font-size as a float but want it was an int
        self.fontsize.setCurrentText(str(int(self.editor.fontPointSize())))
        self.italic_action.setChecked(self.editor.fontItalic())
        self.underline_action.setChecked(self.editor.fontUnderline())
        self.bold_action.setChecked(self.editor.fontWeight() == QFont.Bold)
        self.alignl_action.setChecked(self.editor.alignment() == Qt.AlignLeft)
        self.alignc_action.setChecked(self.editor.alignment() == Qt.AlignCenter)
        self.alignr_action.setChecked(self.editor.alignment() == Qt.AlignRight)
        self.alignj_action.setChecked(self.editor.alignment() == Qt.AlignJustify)
        self.block_signals(self._format_actions, False)
