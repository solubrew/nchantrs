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
from pandas import DataFrame, to_numeric
#===============================================================================||
from condor import condor
from nchantrs.libraries import pyqt
#===============================================================================||

#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
class NchantdNodeModel():
	''' '''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		if parent:
			cfg = self.parent.config
		self.config = condor.instruct(pxcfg).override(cfg)
		super(NchantdNodeModel, self).__init__()
		self.name = 'NodeModel'
	def initModel(self):
		''' '''
		return self
class NchantdConnectorNodeModel(NchantdNodeModel):
	''' '''
	def __init__(self, parent=None, cfg={}):
		''' '''
	def initModel(self):
		''' '''
		return self
class NchantdMultiNodeConnectorModel(NchantdNodeModel):
	''' '''
	def __init__(self, parent=None, cfg={}):
		''' '''
	def countLegs(self):
		''' '''
		return self
	def addLeg(self):
		''' '''
		return self
	def editLegProportation(self):
		''' '''
		return self
	def setLegProporation(self):
		''' '''
		return self
