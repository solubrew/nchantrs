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

from pandas import DataFrame
#===============================================================================||
from condor import condor#										||

from fxsquirl import collector

from worldbridger.source import etherscanSRC

from nchantrs import utils
from nchantrs.libraries import pyqt
from nchantrs.models.applicationmodels import NchantdCloakModel
from nchantrs.models import models, treemodels
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = f'{here}/_data_/models.yaml'

class NchantdDynamicRecordEntryFormModel():
	'''A model that consolidates the models of the entry fields '''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg)
		self.config.select('NchantdDynamicRecordEntryFormModel').override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdDynamicRecordEntryFormModel, self).__init__(parent)

	def initModel(self):
		''' '''
		for self.model.fieldWDGTs.keys():
			self.model.fieldWDGTs[]
		return self

	def createRecord(self, rid, data):
		'''Store an individual record of one or many fields '''
		self.parent.model.insertRecord()
		return self

	def editRecord(self, rid, data):
		''' '''
		self.parent.model.updateRecord()
		return self

	def entryFieldModels(self):
		'''Combine and connect to the dynamic entry fields and controls in
			the form '''
		return self

	def getRecord(self, rid):
		''' '''

	def removeRecord(self, rid):
		''' '''

	def nextRecord(self, id):
		''' '''
		return self

	def prevRecord(self, id):
		''' '''

		return self



class NchantdAPIEntryFormModel():
	''' '''
	def __init__(self):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg)
		self.config.select('NchantdAPIEntryFormModel').override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdAPIEntryFormModel, self).__init__(parent)
