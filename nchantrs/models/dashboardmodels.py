#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid: 30e23520-3e11-414b-8394-5c0e09df32b6  #								||
	name:	#																	||
	description: >  #															||

	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#================================Core Modules===================================||
from os.path import abspath, dirname, join
#===============================================================================||
from condor import condor
from fxsquirl import fxsquirl
from nchantrs.libraries import pyqt
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
#===============================================================================||
pxcfg = join(abspath(here), '_data_/dashboardmodels.yaml')

class NchantdDashboardModel(pyqt.QAbstractItemModel):
	''' '''

	def __init__(self, parent=None, cfg: dict={}):
		''' '''
		self.parent = parent
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('NchantdDashboardModel')
		self.config.override(cfg)
		super(NchantdDashboardModel, self).__init__(parent)
		self.src = None

	def initModel(self):
		''' '''
		return self

	def data(self):
		''' '''
		self.addItems(self.src, parent)
		return self

	def mapItems(self):
		''' '''
		return self


#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
