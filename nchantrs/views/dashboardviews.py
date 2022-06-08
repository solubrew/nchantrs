#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid: 48959256-db30-4525-9a64-ea6eb2fd2f7c  #								||
	name:   #																	||
	description: >  #															||
		  #			||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#===============================Core Modules====================================||
from os.path import abspath, dirname, exists, join
#===============================================================================||
from condor import condor
from nchantrs.libraries import pyqt, pandas_profiling, pandasgui, sweetviz
from nchantrs.widgets import widgets
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
#===============================================================================||
pxcfg = join(abspath(here), '_data_/dashboardviews.yaml')

class NchantdDashboardView(pyqt.QWidget):
	''' '''

	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('NchantdDashboardView')
		self.config.override(cfg)
		super(NchantdDashboardView, self).__init__()

	def initView(self):
		''' '''
		self.layout = pyqt.QVBoxLayout()
		self.layout.addWidget(self)
		self.model = self.parent.model
		self.setModel(self.model)
		self.initUI()
		self.initContextMenu()
		self.initTriggers()
		return self

	def initContextMenu(self):
		''' '''
		return self

	def initTriggers(self):
		''' '''
		return self

	def initUI(self):
		''' '''
		return self

	def setModel(self, model):
		''' '''
		return self


#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
