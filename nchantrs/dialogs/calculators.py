#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Nchantrs@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:   #																	||
	name: #				||
	description: >  #															||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	path: <[LEXIvrs]>  #														||
	outline: <[outline]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#================================Core Modules===================================||
from os.path import abspath, dirname, exists, join
#===============================================================================||
from nchantrs.libraries import pyqt
from nchantrs.widgets.buttons import Button
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
#===============================================================================||
class Calculator(pyqt.QWidget):
	''' '''
	NumDigitButtons = 10
	def __init__(self, app, cfg: dict={}, parent=None):
		''' '''
		super(Calculator, self).__init__(parent)
		self.pendingAdditiveOperator = ''
		self.pendingMultiplicativeOperator = ''
		self.sumInMemory = 0.0
		self.sumSoFar = 0.0
		self.factorSoFar = 0.0
		self.waitingForOperand = True
		self.setDisplay()
		self.buildKeyBoard()

		mainLayout = pyqt.QGridLayout()
		mainLayout.setSizeConstraint(pyqt.QLayout.SetFixedSize)
		mainLayout.addWidget(self.display, 0, 0, 1, 6)
		mainLayout.addWidget(self.backspaceButton, 1, 0, 1, 2)
		mainLayout.addWidget(self.clearButton, 1, 2, 1, 2)
		mainLayout.addWidget(self.clearAllButton, 1, 4, 1, 2)
		mainLayout.addWidget(self.clearMemoryButton, 2, 0)
		mainLayout.addWidget(self.readMemoryButton, 3, 0)
		mainLayout.addWidget(self.setMemoryButton, 4, 0)
		mainLayout.addWidget(self.addToMemoryButton, 5, 0)

		for i in range(1, Calculator.NumDigitButtons):
			row = ((9 - i) / 3) + 2
			column = ((i - 1) % 3) + 1
			mainLayout.addWidget(self.digitButtons[i], row, column)

		mainLayout.addWidget(self.digitButtons[0], 5, 1)
		mainLayout.addWidget(self.pointButton, 5, 2)
		mainLayout.addWidget(self.changeSignButton, 5, 3)
		mainLayout.addWidget(self.divisionButton, 2, 4)
		mainLayout.addWidget(self.timesButton, 3, 4)
		mainLayout.addWidget(self.minusButton, 4, 4)
		mainLayout.addWidget(self.plusButton, 5, 4)
		mainLayout.addWidget(self.squareRootButton, 2, 5)
		mainLayout.addWidget(self.powerButton, 3, 5)
		mainLayout.addWidget(self.reciprocalButton, 4, 5)
		mainLayout.addWidget(self.equalButton, 5, 5)
		self.setLayout(mainLayout)
	def setDisplay(self):
		''' '''
		self.display = pyqt.QLineEdit('0')
		self.display.setReadOnly(True)
		self.display.setAlignment(pyqt.Qt.AlignRight)
		self.display.setMaxLength(15)
		font = self.display.font()
		font.setPointSize(font.pointSize() + 8)
		self.display.setFont(font)
		return self
	def buildKeyBoard(self):
		''' '''
		self.digitButtons = []
		for i in range(Calculator.NumDigitButtons):
			self.digitButtons.append(self.createButton(str(i), self.digitClicked))
		self.pointButton = self.createButton(".", self.pointClicked)
		self.changeSignButton = self.createButton(u"\N{PLUS-MINUS SIGN}", self.changeSignClicked)
		self.backspaceButton = self.createButton("Backspace", self.backspaceClicked)
		self.clearButton = self.createButton("Clear", self.clear)
		self.clearAllButton = self.createButton("Clear All", self.clearAll)
		self.clearMemoryButton = self.createButton("MC", self.clearMemory)
		self.readMemoryButton = self.createButton("MR", self.readMemory)
		self.setMemoryButton = self.createButton("MS", self.setMemory)
		self.addToMemoryButton = self.createButton("M+", self.addToMemory)
		self.divisionButton = self.createButton(u"\N{DIVISION SIGN}", self.multiplicativeOperatorClicked)
		self.timesButton = self.createButton(u"\N{MULTIPLICATION SIGN}", self.multiplicativeOperatorClicked)
		self.minusButton = self.createButton("-", self.additiveOperatorClicked)
		self.plusButton = self.createButton("+", self.additiveOperatorClicked)
		self.squareRootButton = self.createButton("Sqrt", self.unaryOperatorClicked)
		self.powerButton = self.createButton(u"x\N{SUPERSCRIPT TWO}", self.unaryOperatorClicked)
		self.reciprocalButton = self.createButton("1/x", self.unaryOperatorClicked)
		self.equalButton = self.createButton("=", self.equalClicked)
		return self
	def digitClicked(self):
		clickedButton = self.sender()
		digitValue = int(clickedButton.text())
		if self.display.text() == '0' and digitValue == 0.0:
			return
		if self.waitingForOperand:
			self.display.clear()
			self.waitingForOperand = False
		self.display.setText(self.display.text() + str(digitValue))
	def unaryOperatorClicked(self):
		clickedButton = self.sender()
		clickedOperator = clickedButton.text()
		operand = float(self.display.text())
		if clickedOperator == "Sqrt":
			if operand < 0.0:
				self.abortOperation()
				return
			result = math.sqrt(operand)
		elif clickedOperator == u"x\N{SUPERSCRIPT TWO}":
			result = math.pow(operand, 2.0)
		elif clickedOperator == "1/x":
			if operand == 0.0:
				self.abortOperation()
				return
			result = 1.0 / operand
		self.display.setText(str(result))
		self.waitingForOperand = True
	def additiveOperatorClicked(self):
		clickedButton = self.sender()
		clickedOperator = clickedButton.text()
		operand = float(self.display.text())
		if self.pendingMultiplicativeOperator:
			if not self.calculate(operand, self.pendingMultiplicativeOperator):
				self.abortOperation()
				return
			self.display.setText(str(self.factorSoFar))
			operand = self.factorSoFar
			self.factorSoFar = 0.0
			self.pendingMultiplicativeOperator = ''
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
		clickedButton = self.sender()
		clickedOperator = clickedButton.text()
		operand = float(self.display.text())
		if self.pendingMultiplicativeOperator:
			if not self.calculate(operand, self.pendingMultiplicativeOperator):
				self.abortOperation()
				return
			self.display.setText(str(self.factorSoFar))
		else:
			self.factorSoFar = operand
		self.pendingMultiplicativeOperator = clickedOperator
		self.waitingForOperand = True
	def equalClicked(self):
		operand = float(self.display.text())
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
		self.display.setText(str(self.sumSoFar))
		self.sumSoFar = 0.0
		self.waitingForOperand = True
	def pointClicked(self):
		if self.waitingForOperand:
			self.display.setText('0')
		if "." not in self.display.text():
			self.display.setText(self.display.text() + ".")
		self.waitingForOperand = False
	def changeSignClicked(self):
		text = self.display.text()
		value = float(text)
		if value > 0.0:
			text = "-" + text
		elif value < 0.0:
			text = text[1:]
		self.display.setText(text)
	def backspaceClicked(self):
		if self.waitingForOperand:
			return
		text = self.display.text()[:-1]
		if not text:
			text = '0'
			self.waitingForOperand = True
		self.display.setText(text)
	def clear(self):
		if self.waitingForOperand:
			return
		self.display.setText('0')
		self.waitingForOperand = True
	def clearAll(self):
		self.sumSoFar = 0.0
		self.factorSoFar = 0.0
		self.pendingAdditiveOperator = ''
		self.pendingMultiplicativeOperator = ''
		self.display.setText('0')
		self.waitingForOperand = True
	def clearMemory(self):
		self.sumInMemory = 0.0
	def readMemory(self):
		self.display.setText(str(self.sumInMemory))
		self.waitingForOperand = True
	def setMemory(self):
		self.equalClicked()
		self.sumInMemory = float(self.display.text())
	def addToMemory(self):
		self.equalClicked()
		self.sumInMemory += float(self.display.text())
	def createButton(self, text, member):
		button = Button(text)
		button.clicked.connect(member)
		return button
	def abortOperation(self):
		self.clearAll()
		self.display.setText("####")
	def calculate(self, rightOperand, pendingOperator):
		if pendingOperator == "+":
			self.sumSoFar += rightOperand
		elif pendingOperator == "-":
			self.sumSoFar -= rightOperand
		elif pendingOperator == u"\N{MULTIPLICATION SIGN}":
			self.factorSoFar *= rightOperand
		elif pendingOperator == u"\N{DIVISION SIGN}":
			if rightOperand == 0.0:
				return False
			self.factorSoFar /= rightOperand
		return True
class FinancialCalculator(Calculator):
	'''Financial Graphing Calculator for use in adhoc calculations allowing data
	 	to be accessed by variable substitution using a syntax like
		TRADE.price, ETH.volume, ETH.202010011700.price'''
	def __init__(self, app, cfg: dict={}, parent=None):
		''' '''
		super(FinancialCalculator, self).__init__(parent)
	def setDisplay(self):
		self.display = QLineEdit('0')
		self.display.setReadOnly(True)
		self.display.setAlignment(Qt.AlignRight)
		self.display.setAlignment(Qt.AlignBottom)
		font = self.display.font()
		font.setPointSize(font.pointSize() + 8)
		self.display.setFont(font)
		return self
	def updateKeyboard(self):
		''' '''
class GraphingCalculator(Calculator):
	''' '''
	def __init__(self, parent=None):
		''' '''
