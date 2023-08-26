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
pxcfg = f'{here}/_data_/maps.yaml'
class NchantdMap():
	''' '''
	def __init__(self, item, nid, df=DataFrame(), parent=None):
		''' '''
		self.parent = parent
		if parent:
			cfg = self.parent.config
		self.config = condor.instruct(pxcfg).select('NchantdItem')
		self.config.override(cfg)
		super(NchantdItem, self).__init__(parent)
		self.model = NchantdMapModel(self)
		self.view = NchantdMapView(self)
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

class NchantdMindMap():
	'''Provide a Canvas area to place and arrange nodes for defining a mind map
		'''
	def __init__(self, item, nid, df=DataFrame(), parent=None):
		''' '''
		self.parent = parent
		if parent:
			cfg = self.parent.config
		self.config = condor.instruct(pxcfg).select('NchantdItem')
		self.config.override(cfg)
		super(NchantdItem, self).__init__(parent)
		self.model = NchantdMapModel(self)
		self.view = NchantdMapView(self)
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
