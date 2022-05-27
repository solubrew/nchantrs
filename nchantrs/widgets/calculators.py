#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	DOCid:   #																	||
	name:   #																	||
	description: >  #															||
		  #			||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	path: <[LEXIvrs]>  #														||
	outline: <[outline]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#===============================Core Modules====================================||
#===============================Core Modules====================================||
from os.path import abspath, dirname, exists, join
from datetime import datetime as dt
#===============================================================================||
from nchantrs.libraries import pyqt
from nchantrs.dialogs.prefs import Preferences
from nchantrs.widgets.editors import NchantdScratchEditor
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
#===============================================================================||
class NchantdAdvancedCalculator(pyqt.QWidget):
	'''A Calculator Widget with the ability to enter equations and an output
		log'''
	def __init__(self, parent=None):
		''' '''
		pxcfg = '{here}_data_/controls.yaml'
		if parent:
			cfg = parent.config
		super(NchantdAdvancedCalculator, self).__init__(self)
	def initUI(self):
		''' '''
		self.display = NchantdTextBox(self)
		self.numberpad = NchantdNumberPad(self)
		self.mathpad = NchantdMathPad(self)

		return self
	def initModel(self):
		''' '''
		return self
	def initView(self):
		''' '''
		return self
	def initWidget(self):
		''' '''
		return self
class NchantdSimpleCalculator(pyqt.QWidget):
	'''A Calculator Widget with a simple serial entry and single output display
	'''
	def __init__(self, parent=None):
		''' '''
		pxcfg = '{here}_data_/controls.yaml'
		if parent:
			cfg = parent.config
		super(NchantdSimpleCalculator, self).__init__(self)
	def initModel(self):
		''' '''
		return self
	def initView(self):
		''' '''
		self.display = NchantdTextBox(self)
		self.numberpad = NchantdNumberPad(self)
		self.mathpad = NchantdMathPad(self)

		return self
	def initWidget(self):
		''' '''
		return self
class NchantdFinancialCalculator(pyqt.QWidget):
	'''A Calculator Widget with the ability to enter equations and an output
		log'''
	def __init__(self, parent=None):
		''' '''
		pxcfg = '{here}_data_/controls.yaml'
		if parent:
			cfg = parent.config
		super(NchantdAdvancedCalculator, self).__init__(self)
	def initUI(self):
		''' '''
		self.display = NchantdTextBox(self)
		self.numberpad = NchantdNumberPad(self)
		self.mathpad = NchantdMathPad(self)

		return self
	def initModel(self):
		''' '''
		return self
	def initView(self):
		''' '''
		return self
	def initWidget(self):
		''' '''
		return self
