#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	DOCid: <^(UUID)^>  #														||
	name:  #																	||
	description: >  #															||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
'''
# -*- coding: utf-8 -*-
#================================Core Modules===================================||
from os.path import abspath, dirname, exists, join
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||

class NchantdEntryBoxModel():
	''' '''
	def __init__(self, parent=None, value=None, cfg={}):
		''' '''
		self.parent = parent
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('NchantdEntryBoxModel')
		self.config.override(cfg)
		super(NchantdEntryBox, self).__init__()

	def initModel(self):
		''' '''

	def createRecord(self, rid, data):
		'''store an individual field entry '''
		self.parent.model.insertRecord()
		return self

	def editRecord(self, rid, data):
		''' '''
		self.parent.model.updateRecord()
		return self
