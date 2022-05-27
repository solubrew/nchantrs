#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: <^[uuid]^>
	name:
	description: >
	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#=======================================================================||
import sys, enum, types
from os.path import abspath, dirname, join
#=======================================================================||
from condor import condor
from nchantrs.libraries import pyqt
#================Common Globals=========================================||
here = join(dirname(__file__),'')#						||
there = abspath(join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
#=======================================================================||
pxcfg = f'{here}_data_/annotations.yaml'#									||assign default config
class NchantdLabel(pyqt.QLabel):
	'''Standard Nchantd Label'''
	def __init__(self, text=None, parent=None, cfg={}):
		''' '''
		self.parent = parent
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('NchantdJournalEditorView')
		self.config.override(cfg)
		super(NchantdLabel, self).__init__()
		self.setText(text)
	def buildWidget(self, cfg):
		''' '''
		self.setText(cfg['text'])
		font = pyqt.QFont(cfg['font'], cfg['size'], pyqt.QFont.Bold)
		self.setFont(font)
	def initModel(self):
		''' '''
		self.model.data = self.parent.labeltext
		return self
	def initView(self):
		''' '''
		self.setText(self.model.data)
		self.setFixedHeight(25)
		return self
	def initWidget(self):
		''' '''
		return self
class NchantdEntryBox(pyqt.QLineEdit):
	'''Standard Nchantd Entry Box'''
	def __init__(self, parent=None, value=None, cfg={}):
		''' '''
		self.parent = parent
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('NchantdEntryBox')
		self.config.override(cfg)
		super(NchantdEntryBox, self).__init__(value)
	def initWidget(self):
		self.returnPressed.connect(self.enteredText)
		return self
	def enteredText(self):
		'''on text entered it needs to be added to a data structure for
			assemblying an update record
			manually it would be easy wire the returnPressed event to an in
			class function but how to access it on selection of a submit button'''
		print('Text Entered')
		return self
class NchantdDisplayBox():
	''' '''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('NchantdEntryBox')
		self.config.override(cfg)
		super(NchantdEntryBox, self).__init__()
		self.model = annotationmodels.NchantdDisplayBoxModel(self)
		self.view = annotationviews.NchantdDisplayBoxView(self)
	def initModel(self):
		''' '''
		self.model.initModel()
		return self
	def initView(self):
		''' '''
		self.view.initView()
		return self
	def initWidget(self):
		''' '''
		self.initModel()
		self.initView()
		return self
class NchantdProgressBar(pyqt.QProgressBar):
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('NchantdEntryBox')
		self.config.override(cfg)
		super(NchantdProgressBar, self).__init__(cfg, parent)
		widget.setValue(0)
	def updateProgress(self):
		''' '''
		return self
	def initModel(self):
		''' '''
		self.model.initModel()
		return self
	def initView(self):
		''' '''
		self.view.initView()
		return self
	def initWidget(self):
		''' '''
		self.initModel()
		self.initView()
		return self
