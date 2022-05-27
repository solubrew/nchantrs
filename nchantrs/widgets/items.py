#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:   #																	||
	name:	#																	||
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
from os.path import abspath, dirname, join
#===============================================================================||
from pandas import DataFrame
#===============================================================================||
from condor import condor
from excalc import ts as calcts
from fxsquirl import fxsquirl
from fxsquirl import collector
from nchantrs.libraries import pyqt
from nchantrs.models.itemmodels import NchantdItemModel
from nchantrs.views.itemviews import NchantdItemView
#===============================================================================||

#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/items.yaml')
class NchantdItem(pyqt.QStandardItem):
	''' '''
	def __init__(self, item, nid, df=DataFrame(), parent=None):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdItem')
		if parent:
			self.config.override(parent.config)
		super(NchantdItem, self).__init__(parent)
		self.model = NchantdItemModel(self)
		self.view = NchantdItemView(self)
	def initModel(self):
		''' '''
		return self
	def initView(self):
		''' '''
		self.view.initView(self)
		self.setLayout(self.view.layout)
		return self
	def initWidget(self):
		''' '''
		self.model()
		self.view()
		return self
#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
