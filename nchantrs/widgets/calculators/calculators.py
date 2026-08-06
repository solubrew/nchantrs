from typing import Any
'\n---\n<(META)>:\n    docid:\n    name:\n    description: >\n    version: 0.0.0.0.0.0\n    authority: filesystem\n    security: seclvl2\n    <(WT)>: -32\n'
from os.path import dirname, join
import math
import logging
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.widgets.controls.button_groups import NchantdMathPad, NchantdNumberPad
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.media.editors.editors import NchantdEntryBox
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.widgets.tabsets import NchantdTab
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'calculators.yaml')

class NchantdCalculator(NchantdTab):
    """"""
    NumDigitButtons = 10

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdCalculator').override(cfg))
        self.pendingAdditiveOperator = ''
        self.pendingMultiplicativeOperator = ''
        # T-NEW-053: keyboard support on the base calculator so the
        # number row + numpad work without clicking on-screen buttons.
        self.setFocusPolicy(pyqt.Qt.FocusPolicy.StrongFocus)
        self._has_focus = False
        self.sumInMemory = 0.0
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.waitingForOperand = True
        self.calculation_history = []
        self.current_expression = ''
        self.pointButton = None
        self.changeSignButton = None
        self.backspaceButton = None
        self.clearButton = None
        self.clearAllButton = None
        self.clearMemoryButton = None
        self.readMemoryButton = None
        self.setMemoryButton = None
        self.divisionButton = None
        self.timesButton = None
        self.minusButton = None
        self.plusButton = None
        self.squareRootButton = None
        self.powerButton = None
        self.reciprocalButton = None
        self.equalButton = None
        self.digitButtons = []

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView({'layout': 'grid'})
        self.setDisplay()
        self.buildKeyBoard()
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
            row = int((9 - i) / 3 + 2)
            column = int((i - 1) % 3 + 1)
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

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def additiveOperatorClicked(self) -> None:
        """Handle additive operations: + and -"""
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        self._apply_additive_operator(clickedOperator)

    def _apply_additive_operator(self, clickedOperator: str) -> None:
        """Apply the additive operator ``+`` or ``-`` from a button click or key event.

        Extracted from ``additiveOperatorClicked`` so the key-routing
        path in ``NchantdAdvancedCalculator.keyPressEvent`` can drive
        the same logic without needing a button sender.
        """
        try:
            operand = float(self._get_current_line())
        except ValueError:
            self.abortOperation()
            return
        if not self.current_expression:
            self.current_expression = str(operand)
        else:
            self.current_expression += ' ' + str(operand)
        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            self._set_current_line(str(self.factorSoFar))
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ''
        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return
            self._set_current_line(str(self.sumSoFar))
        else:
            self.sumSoFar = operand
        self.current_expression += ' ' + clickedOperator
        self.pendingAdditiveOperator = clickedOperator
        self.waitingForOperand = True

    def multiplicativeOperatorClicked(self) -> None:
        """Handle multiplicative operations: × and ÷"""
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        self._apply_multiplicative_operator(clickedOperator)

    def _apply_multiplicative_operator(self, clickedOperator: str) -> None:
        """Apply the multiplicative operator ``×`` or ``÷`` from a button click or key event."""
        try:
            operand = float(self._get_current_line())
        except ValueError:
            self.abortOperation()
            return
        if not self.current_expression:
            self.current_expression = str(operand)
        else:
            self.current_expression += ' ' + str(operand)
        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            self._set_current_line(str(self.factorSoFar))
        else:
            self.factorSoFar = operand
        self.current_expression += ' ' + clickedOperator
        self.pendingMultiplicativeOperator = clickedOperator
        self.waitingForOperand = True

    def unaryOperatorClicked(self) -> None:
        """Handle unary operations: Sqrt, Square, Reciprocal"""
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        try:
            operand = float(self._get_current_line())
        except ValueError:
            self.abortOperation()
            return
        try:
            if clickedOperator == 'Sqrt':
                if operand < 0.0:
                    self.abortOperation()
                    return
                result = math.sqrt(operand)
            elif clickedOperator == 'x²':
                result = math.pow(operand, 2.0)
            elif clickedOperator == '1/x':
                if operand == 0.0:
                    self.abortOperation()
                    return
                result = 1.0 / operand
            else:
                logma.warning(f'Unknown unary operator: {clickedOperator}')
                return
            self._set_current_line(str(result))
            self.waitingForOperand = True
        except Exception as e:
            logma.error(f'Error in unary operation: {e}')
            self.abortOperation()

    def digitClicked(self) -> None:
        """Handle digit button clicks (0-9)"""
        clickedButton = self.sender()
        try:
            digitValue = int(clickedButton.text())
        except (ValueError, AttributeError):
            return
        self._press_digit(digitValue)

    def _press_digit(self, digitValue: int) -> None:
        """Press a digit (called from both button clicks and key events).

        Extracted from ``digitClicked`` so the key-routing path in
        ``NchantdAdvancedCalculator.keyPressEvent`` can drive the
        same entry logic without needing a button sender.
        """
        if digitValue < 0 or digitValue > 9:
            return
        current_text = self._get_current_line()
        if current_text == '0' and digitValue == 0:
            return
        if self.waitingForOperand:
            self._set_current_line('')
            self.waitingForOperand = False
            if not self.pendingAdditiveOperator and (not self.pendingMultiplicativeOperator) and self.calculation_history:
                self._update_display('\n'.join(self.calculation_history[-10:]) + '\n')
        self._set_current_line(self._get_current_line() + str(digitValue))

    def pointClicked(self) -> None:
        """Handle decimal point entry"""
        if self.waitingForOperand:
            self._set_current_line('0')
        current_text = self._get_current_line()
        if current_text and '.' not in current_text:
            self._set_current_line(current_text + '.')
        self.waitingForOperand = False

    def changeSignClicked(self) -> None:
        """Toggle sign of current number (+/-)"""
        try:
            text = self._get_current_line()
            value = float(text)
            if value > 0.0:
                text = '-' + text
            elif value < 0.0:
                text = text[1:]
            self._set_current_line(text)
        except ValueError:
            self.abortOperation()

    def backspaceClicked(self) -> None:
        """Remove last digit from display"""
        if self.waitingForOperand:
            return
        text = self._get_current_line()[:-1]
        if not text:
            text = '0'
            self.waitingForOperand = True
        self._set_current_line(text)

    def clear(self) -> None:
        """Clear current entry"""
        if self.waitingForOperand:
            return
        self._set_current_line('0')
        self.waitingForOperand = True

    def clearAll(self) -> None:
        """Clear all calculations and history"""
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.pendingAdditiveOperator = ''
        self.pendingMultiplicativeOperator = ''
        self.calculation_history = []
        self.current_expression = ''
        self._update_display('0')
        self.waitingForOperand = True

    def clearMemory(self) -> None:
        """Clear memory (MC button)"""
        self.sumInMemory = 0.0

    def readMemory(self) -> None:
        """Read memory value (MR button)"""
        self._set_current_line(str(self.sumInMemory))
        self.waitingForOperand = True

    def setMemory(self) -> None:
        """Set memory to current display value (MS button)"""
        try:
            self.equalClicked()
            self.sumInMemory = float(self._get_current_line())
        except ValueError:
            self.sumInMemory = 0.0

    def addToMemory(self) -> None:
        """Add current display value to memory (M+ button)"""
        try:
            self.equalClicked()
            self.sumInMemory += float(self._get_current_line())
        except ValueError:
            pass

    def equalClicked(self) -> None:
        """Compute result of pending calculations (= button)"""
        try:
            operand = float(self._get_current_line())
        except ValueError:
            self.abortOperation()
            return
        if not self.current_expression:
            expression = str(operand)
        else:
            expression = self.current_expression + ' ' + str(operand)
        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ''
        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return
            self.pendingAdditiveOperator = ''
        else:
            self.sumSoFar = operand
        result = str(self.sumSoFar)
        self._add_to_history(expression, result)
        self.current_expression = ''
        self.sumSoFar = 0.0
        self.waitingForOperand = True

    def abortOperation(self) -> None:
        """Abort operation and display error state"""
        self.clearAll()
        self._set_current_line('Error')

    def _get_current_line(self) -> Any:
        """Get the current line (last line) from the display"""
        text = self.display.toPlainText()
        lines = text.split('\n')
        return lines[-1] if lines else '0'

    def _set_current_line(self, value) -> None:
        """Set the current line (last line) in the display"""
        text = self.display.toPlainText()
        lines = text.split('\n')
        if len(lines) > 0:
            lines[-1] = value
        else:
            lines = [value]
        self._update_display('\n'.join(lines))

    def _update_display(self, text) -> None:
        """Update display with proper bottom alignment"""
        lines = text.split('\n')
        font_metrics = self.display.fontMetrics()
        line_height = font_metrics.lineSpacing()
        display_height = self.display.viewport().height()
        max_lines = max(1, display_height // line_height)
        current_lines = len(lines)
        padding_lines = max(0, max_lines - current_lines - 1)
        padded_text = '\n' * padding_lines + text
        html_text = padded_text.replace('\n', '<br>')
        self.display.setHtml(f'<div style="text-align: right;">{html_text}</div>')
        self.display.moveCursor(pyqt.QTextCursor.MoveOperation.End)
        scrollbar = self.display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def _add_to_history(self, expression, result) -> None:
        """Add a calculation to history and update display"""
        history_line = f'{expression} = {result}'
        self.calculation_history.append(history_line)
        display_text = '\n'.join(self.calculation_history[-10:])
        display_text += f'\n{result}'
        self._update_display(display_text)

    def buildKeyBoard(self) -> Any:
        """Build all calculator buttons"""
        self.digitButtons = []
        for i in range(self.NumDigitButtons):
            self.digitButtons.append(self.createButton(str(i), self.digitClicked))
        self.pointButton = self.createButton('.', self.pointClicked)
        self.changeSignButton = self.createButton('±', self.changeSignClicked)
        self.backspaceButton = self.createButton('Backspace', self.backspaceClicked)
        self.clearButton = self.createButton('Clear', self.clear)
        self.clearAllButton = self.createButton('Clear All', self.clearAll)
        self.clearMemoryButton = self.createButton('MC', self.clearMemory)
        self.readMemoryButton = self.createButton('MR', self.readMemory)
        self.setMemoryButton = self.createButton('MS', self.setMemory)
        self.addToMemoryButton = self.createButton('M+', self.addToMemory)
        self.divisionButton = self.createButton('÷', self.multiplicativeOperatorClicked)
        self.timesButton = self.createButton('×', self.multiplicativeOperatorClicked)
        self.minusButton = self.createButton('-', self.additiveOperatorClicked)
        self.plusButton = self.createButton('+', self.additiveOperatorClicked)
        self.squareRootButton = self.createButton('Sqrt', self.unaryOperatorClicked)
        self.powerButton = self.createButton('x²', self.unaryOperatorClicked)
        self.reciprocalButton = self.createButton('1/x', self.unaryOperatorClicked)
        self.equalButton = self.createButton('=', self.equalClicked)
        return self

    def calculate(self, rightOperand: float, pendingOperator: str) -> bool:
        """Perform calculation based on operator using dictionary lookup"""
        OPERATOR_METHODS = {'+': '_apply_add', '-': '_apply_subtract', '×': '_apply_multiply', '÷': '_apply_divide'}
        method_name = OPERATOR_METHODS.get(pendingOperator)
        if method_name and hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(rightOperand)
        return True

    def keyPressEvent(self, event) -> None:
        """Route digit/operator keys to the same logic as button clicks.

        T-NEW-053: keyboard support on the base ``NchantdCalculator``
        so the number row + numpad work without clicking on-screen
        buttons. Previously only ``NchantdAdvancedCalculator`` had this.
        """
        key = event.key()
        # 0-9 (top row + numpad)
        if pyqt.Qt.Key_0 <= key <= pyqt.Qt.Key_9:
            self._press_digit(key - pyqt.Qt.Key_0)
            event.accept()
            return
        # Decimal separators (both US and EU conventions)
        if key in (pyqt.Qt.Key_Period, pyqt.Qt.Key_Comma):
            self.pointClicked()
            event.accept()
            return
        # Operators
        if key == pyqt.Qt.Key_Plus:
            self._apply_additive_operator('+')
            event.accept()
            return
        if key == pyqt.Qt.Key_Minus:
            self._apply_additive_operator('-')
            event.accept()
            return
        if key == pyqt.Qt.Key_Asterisk:
            self._apply_multiplicative_operator('×')
            event.accept()
            return
        if key == pyqt.Qt.Key_Slash:
            self._apply_multiplicative_operator('÷')
            event.accept()
            return
        if key in (pyqt.Qt.Key_Return, pyqt.Qt.Key_Enter):
            self.equalClicked()
            event.accept()
            return
        if key == pyqt.Qt.Key_Backspace:
            self.backspaceClicked()
            event.accept()
            return
        if key == pyqt.Qt.Key_Escape:
            self.clearAll()
            event.accept()
            return
        super().keyPressEvent(event)

    def focusInEvent(self, event) -> None:
        """Mark the calculator as the active key-routing target."""
        super().focusInEvent(event)
        self._has_focus = True

    def focusOutEvent(self, event) -> None:
        """Drop the active-key-routing flag on focus loss."""
        super().focusOutEvent(event)
        self._has_focus = False

    def _apply_add(self, rightOperand: float) -> bool:
        self.sumSoFar += rightOperand
        return True

    def _apply_subtract(self, rightOperand: float) -> bool:
        self.sumSoFar -= rightOperand
        return True

    def _apply_multiply(self, rightOperand: float) -> bool:
        self.factorSoFar *= rightOperand
        return True

    def _apply_divide(self, rightOperand: float) -> bool:
        if rightOperand == 0.0:
            return False
        self.factorSoFar /= rightOperand
        return True

    def createButton(self, text, member) -> Any:
        """Create and configure a button"""
        cfg = {'text': text}
        button = NchantdButton(self, cfg).initWidget()
        button.clicked.connect(member)
        return button

    def setDisplay(self) -> Any:
        """Initialize the display widget as a multiline text area"""
        cfg = {'text': '0'}
        self.config.dikt['width'] = None
        self.config.dikt['height'] = None
        self.config.dikt['size'] = None
        self.display = pyqt.QTextEdit(self)
        self.display.setReadOnly(True)
        self.display.setAlignment(pyqt.Qt.AlignmentFlag.AlignRight | pyqt.Qt.AlignmentFlag.AlignBottom)
        width = 300
        height = 800
        self.display.setMinimumSize(width, int(height * 0.1))
        font = self.display.font()
        font.setPointSize(font.pointSize() + 8)
        self.display.setFont(font)
        self.display.setStyleSheet('QTextEdit { background-color: black; color: white; padding: 5px; }')
        self.display.setFocusPolicy(pyqt.Qt.FocusPolicy.NoFocus)
        self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignCenter | pyqt.Qt.AlignmentFlag.AlignTop)
        self.display.setVerticalScrollBarPolicy(pyqt.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.display.setHtml('<div style="text-align: right;">0</div>')
        return self

class NchantdAdvancedCalculator(NchantdCalculator):
    """A Calculator Widget with the ability to enter equations and an output log"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdAdvancedCalculator').override(cfg))
        self.setFocusPolicy(pyqt.Qt.FocusPolicy.StrongFocus)
        logma.info(f'NchantdAdvancedCalculator initialized')

    def initUI(self) -> Any:
        """Set up the equation log + output panel below the base calculator."""
        super().initUI()
        # Reserve rows 6+ for the advanced equation log (added by subclasses).
        logma.info(f'initUI {type(self).__name__}')
        return self

    def initModel(self) -> Any:
        super().initModel()
        logma.info(f'initModel {type(self).__name__}')
        return self

    def initView(self) -> Any:
        super().initView()
        logma.info(f'initView {type(self).__name__}')
        return self

    def initWidget(self) -> Any:
        super().initWidget()
        logma.info(f'initWidget {type(self).__name__}')
        return self

    def keyPressEvent(self, event) -> None:
        """Route digit/operator keys to the existing button handlers.

        Keeps the button-driven entry path untouched; only adds a
        keyboard-driven path so the calculator can be operated
        without clicking the on-screen buttons.
        """
        key = event.key()
        # 0-9 (top row + numpad)
        if pyqt.Qt.Key_0 <= key <= pyqt.Qt.Key_9:
            self._press_digit(key - pyqt.Qt.Key_0)
            event.accept()
            return
        # Decimal separators (both US and EU conventions)
        if key in (pyqt.Qt.Key_Period, pyqt.Qt.Key_Comma):
            self.pointClicked()
            event.accept()
            return
        # Operators — route to the additive/multiplicative handlers
        if key == pyqt.Qt.Key_Plus:
            self._apply_additive_operator('+')
            event.accept()
            return
        if key == pyqt.Qt.Key_Minus:
            self._apply_additive_operator('-')
            event.accept()
            return
        if key == pyqt.Qt.Key_Asterisk:
            self._apply_multiplicative_operator('×')
            event.accept()
            return
        if key == pyqt.Qt.Key_Slash:
            self._apply_multiplicative_operator('÷')
            event.accept()
            return
        if key in (pyqt.Qt.Key_Return, pyqt.Qt.Key_Enter):
            self.equalClicked()
            event.accept()
            return
        if key == pyqt.Qt.Key_Backspace:
            self.backspaceClicked()
            event.accept()
            return
        if key == pyqt.Qt.Key_Escape:
            self.clearAll()
            event.accept()
            return
        super().keyPressEvent(event)

    def focusInEvent(self, event) -> None:
        """Mark the calculator as the active key-routing target."""
        super().focusInEvent(event)
        logma.debug(f'{type(self).__name__} gained focus')
        self._has_focus = True

    def focusOutEvent(self, event) -> None:
        """Drop the active-key-routing flag on focus loss."""
        super().focusOutEvent(event)
        logma.debug(f'{type(self).__name__} lost focus')
        self._has_focus = False

class NchantdFinancialCalculator(NchantdCalculator):
    """Financial Calculator for adhoc calculations"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdAdvancedCalculator').override(cfg))

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdGraphingCalculator(NchantdAdvancedCalculator):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdAdvancedCalculator').override(cfg))

    def initModel(self) -> Any:
        super().initModel()
        logma.info(f'initModel {type(self).__name__}')
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self