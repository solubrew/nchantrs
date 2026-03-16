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
from os.path import dirname, join
import math

import logging


logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.widgets.controls.button_groups import NchantdMathPad, NchantdNumberPad
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.media.editors.editors import NchantdEntryBox
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.widgets.tabsets import NchantdTab
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "calculators.yaml")
pxcfg = {}


class NchantdCalculator(NchantdTab):
    """"""

    NumDigitButtons = 10

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdCalculator")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(parent, cfg)
        self.config.override(cfg)
        self.pendingAdditiveOperator = ""
        self.pendingMultiplicativeOperator = ""
        self.sumInMemory = 0.0
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.waitingForOperand = True
        self.pointButton = None
        self.changeSignButton = None
        self.backspaceButton = None
        self.clearButton = None
        self.clearAllButton = None
        self.clearMemoryButton = None
        self.readMemoryButton = None
        self.setMemoryButton = None
        self.addToMemoryButton = None
        self.divisionButton = None
        self.timesButton = None
        self.minusButton = None
        self.plusButton = None
        self.squareRootButton = None
        self.powerButton = None
        self.reciprocalButton = None
        self.equalButton = None
        self.digitButtons = []

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView({"layout": "grid"})
        self.setDisplay()
        self.buildKeyBoard()

        # Set uniform stretching for columns and rows to fill space evenly
        for col in range(6):
            self.layout.setColumnStretch(col, 1)
        for row in range(6):
            self.layout.setRowStretch(row, 1)

        self.layout.addWidget(self.display, 0, 0, 1, 6)
        self.layout.addWidget(self.backspaceButton, 1, 0, 1, 2)
        self.layout.addWidget(self.clearButton, 1, 2, 1, 2)
        self.layout.addWidget(self.clearAllButton, 1, 4, 1, 2)
        self.layout.addWidget(self.clearMemoryButton, 2, 0)
        self.layout.addWidget(self.readMemoryButton, 3, 0)
        self.layout.addWidget(self.setMemoryButton, 4, 0)
        self.layout.addWidget(self.addToMemoryButton, 5, 0)

        for i in range(1, self.NumDigitButtons):
            row = int(((9 - i) / 3) + 2)
            column = int(((i - 1) % 3) + 1)
            self.layout.addWidget(self.digitButtons[i], row, column)

        self.layout.addWidget(self.digitButtons[0], 5, 1)
        self.layout.addWidget(self.pointButton, 5, 2)
        self.layout.addWidget(self.changeSignButton, 5, 3)
        self.layout.addWidget(self.divisionButton, 2, 4)
        self.layout.addWidget(self.timesButton, 3, 4)
        self.layout.addWidget(self.minusButton, 4, 4)
        self.layout.addWidget(self.plusButton, 5, 4)
        self.layout.addWidget(self.squareRootButton, 2, 5)
        self.layout.addWidget(self.powerButton, 3, 5)
        self.layout.addWidget(self.reciprocalButton, 4, 5)
        self.layout.addWidget(self.equalButton, 5, 5)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def additiveOperatorClicked(self):
        """Handle additive operations: + and -"""
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()

        try:
            operand = float(self.display.text())
        except ValueError:
            self.abortOperation()
            return

        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            self.display.setText(str(self.factorSoFar))
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ""

        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return
            self.display.setText(str(self.sumSoFar))
        else:
            self.sumSoFar = operand

        self.pendingAdditiveOperator = clickedOperator
        self.waitingForOperand = True

    def multiplicativeOperatorClicked(self):
        """Handle multiplicative operations: × and ÷"""
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()

        try:
            operand = float(self.display.text())
        except ValueError:
            self.abortOperation()
            return

        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            self.display.setText(str(self.factorSoFar))
        else:
            self.factorSoFar = operand

        self.pendingMultiplicativeOperator = clickedOperator
        self.waitingForOperand = True

    def unaryOperatorClicked(self):
        """Handle unary operations: Sqrt, Square, Reciprocal"""
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()

        try:
            operand = float(self.display.text())
        except ValueError:
            self.abortOperation()
            return

        try:
            if clickedOperator == "Sqrt":
                if operand < 0.0:
                    self.abortOperation()
                    return
                result = math.sqrt(operand)
            elif clickedOperator == "x\N{SUPERSCRIPT TWO}":
                result = math.pow(operand, 2.0)
            elif clickedOperator == "1/x":
                if operand == 0.0:
                    self.abortOperation()
                    return
                result = 1.0 / operand
            else:
                logma.warning(f"Unknown unary operator: {clickedOperator}")
                return

            self.display.setText(str(result))
            self.waitingForOperand = True
        except Exception as e:
            logma.error(f"Error in unary operation: {e}")
            self.abortOperation()

    def digitClicked(self):
        """Handle digit button clicks (0-9)"""
        clickedButton = self.sender()

        try:
            digitValue = int(clickedButton.text())
        except ValueError:
            return

        if self.display.text() == "0" and digitValue == 0:
            return

        if self.waitingForOperand:
            self.display.clear()
            self.waitingForOperand = False

        self.display.setText(self.display.text() + str(digitValue))

    def pointClicked(self):
        """Handle decimal point entry"""
        if self.waitingForOperand:
            self.display.setText("0")

        current_text = self.display.text()
        if current_text and "." not in current_text:
            self.display.setText(current_text + ".")

        self.waitingForOperand = False

    def changeSignClicked(self):
        """Toggle sign of current number (+/-)"""
        try:
            text = self.display.text()
            value = float(text)
            if value > 0.0:
                text = "-" + text
            elif value < 0.0:
                text = text[1:]
            self.display.setText(text)
        except ValueError:
            self.abortOperation()

    def backspaceClicked(self):
        """Remove last digit from display"""
        if self.waitingForOperand:
            return
        text = self.display.text()[:-1]
        if not text:
            text = "0"
            self.waitingForOperand = True
        self.display.setText(text)

    def clear(self):
        """Clear current entry"""
        if self.waitingForOperand:
            return
        self.display.setText("0")
        self.waitingForOperand = True

    def clearAll(self):
        """Clear all calculations"""
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.pendingAdditiveOperator = ""
        self.pendingMultiplicativeOperator = ""
        self.display.setText("0")
        self.waitingForOperand = True

    def clearMemory(self):
        """Clear memory (MC button)"""
        self.sumInMemory = 0.0

    def readMemory(self):
        """Read memory value (MR button)"""
        self.display.setText(str(self.sumInMemory))
        self.waitingForOperand = True

    def setMemory(self):
        """Set memory to current display value (MS button)"""
        try:
            self.equalClicked()
            self.sumInMemory = float(self.display.text())
        except ValueError:
            self.sumInMemory = 0.0

    def addToMemory(self):
        """Add current display value to memory (M+ button)"""
        try:
            self.equalClicked()
            self.sumInMemory += float(self.display.text())
        except ValueError:
            pass

    def equalClicked(self):
        """Compute result of pending calculations (= button)"""
        try:
            operand = float(self.display.text())
        except ValueError:
            self.abortOperation()
            return

        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ""

        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return
            self.pendingAdditiveOperator = ""
        else:
            self.sumSoFar = operand

        self.display.setText(str(self.sumSoFar))
        self.sumSoFar = 0.0
        self.waitingForOperand = True

    def abortOperation(self):
        """Abort operation and display error state"""
        self.clearAll()
        self.display.setText("Error")

    def buildKeyBoard(self):
        """Build all calculator buttons"""
        self.digitButtons = []
        for i in range(self.NumDigitButtons):
            self.digitButtons.append(self.createButton(str(i), self.digitClicked))

        self.pointButton = self.createButton(".", self.pointClicked)
        self.changeSignButton = self.createButton("\N{PLUS-MINUS SIGN}", self.changeSignClicked)
        self.backspaceButton = self.createButton("Backspace", self.backspaceClicked)
        self.clearButton = self.createButton("Clear", self.clear)
        self.clearAllButton = self.createButton("Clear All", self.clearAll)
        self.clearMemoryButton = self.createButton("MC", self.clearMemory)
        self.readMemoryButton = self.createButton("MR", self.readMemory)
        self.setMemoryButton = self.createButton("MS", self.setMemory)
        self.addToMemoryButton = self.createButton("M+", self.addToMemory)
        self.divisionButton = self.createButton("\N{DIVISION SIGN}", self.multiplicativeOperatorClicked)
        self.timesButton = self.createButton("\N{MULTIPLICATION SIGN}", self.multiplicativeOperatorClicked)
        self.minusButton = self.createButton("-", self.additiveOperatorClicked)
        self.plusButton = self.createButton("+", self.additiveOperatorClicked)
        self.squareRootButton = self.createButton("Sqrt", self.unaryOperatorClicked)
        self.powerButton = self.createButton("x\N{SUPERSCRIPT TWO}", self.unaryOperatorClicked)
        self.reciprocalButton = self.createButton("1/x", self.unaryOperatorClicked)
        self.equalButton = self.createButton("=", self.equalClicked)
        return self

    def calculate(self, rightOperand, pendingOperator):
        """Perform calculation based on operator"""
        if pendingOperator == "+":
            self.sumSoFar += rightOperand
        elif pendingOperator == "-":
            self.sumSoFar -= rightOperand
        elif pendingOperator == "\N{MULTIPLICATION SIGN}":
            self.factorSoFar *= rightOperand
        elif pendingOperator == "\N{DIVISION SIGN}":
            if rightOperand == 0.0:
                return False
            self.factorSoFar /= rightOperand
        return True

    def createButton(self, text, member):
        """Create and configure a button"""
        cfg = {"text": text}
        button = NchantdButton(self, cfg).initWidget()
        button.clicked.connect(member)
        return button

    def setDisplay(self):
        """Initialize the display widget"""
        cfg = {"text": "0"}
        self.config.dikt["width"] = None
        self.config.dikt["height"] = None
        self.config.dikt["size"] = None
        self.display = NchantdEntryBox(self, cfg).initWidget()
        self.display.setReadOnly(True)
        self.display.setAlignment(pyqt.Qt.AlignmentFlag.AlignRight | pyqt.Qt.AlignmentFlag.AlignBottom)
        self.display.setMaxLength(24)

        width = 300
        height = 800
        self.display.set_size(None, None, width, int(height * 0.1))

        font = self.display.font()
        font.setPointSize(font.pointSize() + 8)
        self.display.setFont(font)
        self.display.set_background(color="black")
        self.display.setFocusPolicy(pyqt.Qt.FocusPolicy.NoFocus)
        self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignCenter | pyqt.Qt.AlignmentFlag.AlignTop)
        self.display.setText(str(0.0))
        return self


class NchantdAdvancedCalculator(NchantdCalculator):
    """A Calculator Widget with the ability to enter equations and an output log"""

    def __init__(self, parent=None):
        """ """
        super(NchantdAdvancedCalculator, self).__init__(parent)

    def initUI(self):
        """ """
        return self

    def initModel(self):
        """ """
        return self

    def initView(self):
        """ """
        return self

    def initWidget(self):
        """ """
        return self


class NchantdFinancialCalculator(NchantdCalculator):
    """Financial Calculator for adhoc calculations"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdFinancialCalculator")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(parent, cfg)
        self.config.override(cfg)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdGraphingCalculator(NchantdAdvancedCalculator):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdGraphingCalculator")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdGraphingCalculator, self).__init__(parent)

    def initModel(self):
        """"""
        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
