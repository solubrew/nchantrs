#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:   #																	||
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
from os.path import abspath, dirname, join
#===============================================================================||
from condor import condor
from nchantrs.libraries import pyqt
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = f'{here}/_data_/toolbars.yaml'
class NchantdToolbar(pyqt.QToolBar):
	'''Standard Nchantd Toolbar '''
	def __init__(self, cfg: dict={}):
		''' '''
		self.config = condor.instruct(pxcfg).select('nchantdtoolbar')
		self.config.override(cfg)
		super(NchantdToolBar, self).__init__()
	def initModel(self):
		''' '''
		return self
	def initView(self):
		''' '''
		return self
	def initWidget(self):
		''' '''
		return self
class NchantdRecordNavigationToolbar(NchantdToolbar):
	'''Standard Nchantd Record Navigation Toolbar '''
	def __init__(self, cfg: dict={}):
		''' '''
		self.config = condor.instruct(pxcfg)
		self.config.select('nchantdrecordnavigationtoolbar').override(cfg)
		super(NchantdRecordNavigationToolbar, self).__init__()

		self.model = NchantdTableModel(app, self.config.dikt, parent)

		self.layout = pyqt.QHBoxLayout()
		self.config.dikt['text'] = 'Backward'
		self.backBTN = NchantdToolButton(self, self.config.dikt['text'])
		self.backBTN.clicked.connect(self.prevRecord())
		self.layout.addWidget(self.backBTN)
		self.config.dikt['Label'] = 'Go To:'
		self.gotoLineEditor = NchantdLineEditor()
		self.layout.addWidget(self.gotoLineEditor)
		self.goBTN = NchantdButton()
		self.goBTN.clicked.connect(self.findRecord())
		self.layout.addWidget(self.goBTN)
		self.config.dikt['text'] = 'Forward'
		self.foreBTN = NchantdToolButton(self, self.config.dikt['text'])
		self.foreBTN.clicked.connect(self.nextRecord)
		self.layout.addWidget(self.foreBTN)
		self.setLayout(self.layout)
	def nextRecord(self):
		''' '''
		return self
	def prevRecord(self):
		''' '''
		return self
	def findRecord(self):
		''' '''
		return self
