#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>: 'b0383757-eb6b-4d01-a5af-f0b4bc6b3b44' #								||
	docid:   #																	||
	name: Nchantrs Module Widgets Forms Python Excecution Document  #			||
	description: >  #															||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#================================Core Modules===================================||
from os.path import abspath, dirname, exists, join
from sys import argv, exit
#===============================================================================||
from condor import condor, thing#												||
from nchantrs.libraries import pyqt
from nchantrs.models.tablemodels import NchantdTableModel
from nchantrs.widgets.controls import NchantdSubmissionButtons
from nchantrs.widgets.editors import NchantdEntryEditor
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/forms.yaml')#								||assign default config

class NchantdDynamicRecordEntryForm(pyqt.QWidget):
	'''A single pane widget for building a simple top down entry form with a
		submission button at the end of the form '''

	def __init__(self, parent=None, cfg={}):
		''' '''
		self.config = condor.instruct(pxcfg).override(cfg)#		||
		if parent:
			self.config.override(parent.config)
		if log: print('Nchantd Dynamic Record Entry Form Config', self.config.dikt)
		super(NchantdDynamicRecordEntryForm, self).__init__()
		self.model = NchantdTableModel(self)
		self.layout = pyqt.QVBoxLayout()
		self.buildPane()
		self.setLayout(self.layout)

	def initModel(self):
		''' '''
		return self

	def initWidget(self):
		''' '''
		self.initModel()
		return self

	def buildPane(self):
		'''
			The pane is built with fields not sure how to abstract this
		'''
		cnt, self.fieldWDGTs = 0, {}
		self.loadFields()
		self.entryBTNs = NchantdSubmissionButtons(self).initWidget()
		self.layout.addWidget(self.entryBTNs)
		return self

	def configView(self, cols: dict={}):
		''' '''
		if log: print('CONFIG', self.config.dikt)
		cfgview = self.config.dikt['pane']['view']
		if cols != {}:
			for col, vals in cols.items():
				if vals['hidden']:
					self.setColumnHidden(vals['id'], True)
				else:
					self.setColumnWidth(vals['id'], vals['width'])
		self.setFixedWidth(cfgview['FixedWidth'])
		return self

	def deleteEntry(self, record):
		''' '''
		self.model.deleteRecord(record)
		return self

	def loadControls(self):
		''' '''
		if log: print('New Button\n', self.entryBTNs.newbutton.__dir__())
		if self.entryBTNs.newbutton.isEnabled:
			self.entryBTNs.newbutton.clicked.connect(self.newEntry)
		if self.entryBTNs.submitbutton.isEnabled:
			self.entryBTNs.submitbutton.clicked.connect(self.submitEntry)
		if self.entryBTNs.deletebutton.isEnabled:
			self.entryBTNs.deletebutton.clicked.connect(self.deleteEntry)
		return self

	def loadFields(self):
		''' '''
		if log: print('Fields Config', self.config.dikt)
		for field in self.config.dikt['params']['fields'].keys():
			cfg = self.config.dikt['params']['fields'][field]
			self.fieldWDGTs[field] = NchantdEntryEditor(self, cfg).initWidget()
			self.layout.addWidget(self.fieldWDGTs[field])
		return self

	def newEntry(self, record, action=None):
		''' '''
		if log: print('New Entry')
		record = []
		for field, wdgt in self.fieldWDGTs.items():
			if log: print('Field',field,'Text', wdgt.textbox.text())
			record.append(wdgt.textbox.text())
			#thingify action...allow action to be override by the config...or
			#should it be required? this is a question of integration with
			#FxSQuiRL vs full abstraction to the config layer
		self.model.createRecord(record)
		return self

	def submitEntry(self, record):
		''' '''
		self.model.submitRecord(record)
		return self


class NchantdAPIEntryForm(NchantdDynamicRecordEntryForm):
	''' '''

	def __init__(self, parent=None, cfg={}):
		''' '''
		self.config = condor.instruct(pxcfg).select('NchantdAPIEntryForm')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		self.src = parent.src
		super(NchantdAPIEntryForm, self).__init__(parent)
		self.buildPane()


class NchantdMultiPageTableEditorForm():
	'''A single pane widget with multiple tabs for each page of the form '''

	def __init__(self):
		''' '''


class NchantdTableEditorForm(pyqt.QWidget):
	'''A single pane widget with the ability to navigate forward and back within
		a given view/table and edit or create entries with a table view of the
		entries at the bottom of the pane '''

	def __init__(self):
		''' '''
		pyqt.QWidget.__init__(self)
		self.view = NchantdFormView()
		self.model = NchantdTableModel()
		self.layout = pyqt.QVBoxLayout()


class NchantdTaskEntryForm(pyqt.QWidget):
	''' '''

	def __init__(self):
		''' '''


class NchantdSolidityContractForm(NchantdDynamicRecordEntryForm):
	''' '''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg)
		self.config.select('NchantdSolidityContractForm').override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdSolidityContractForm, self).__init__(parent)

	def loadABI(self):
		''' '''
		return self

	def loadContract(self):
		'''Load contract from database or get it from rpc endpoint if not
			already stored localally '''
		return self

	def extractContractCMDs(self):
		''' '''
		return self


#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
