
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																	||
---  #																	||
<(META)>:  #															||
	docid:   #															||
	name:	#														||
	description: >  #													||

	expirary: <[expiration]>  #											||
	version: <[version]>  #												||
	path: <[LEXIvrs]>  #												||
	outline: <[outline]>  #												||
	authority: document|this  #											||
	security: sec|lvl2  #												||
	<(WT)>: -32  #														||
''' #																	||
# -*- coding: utf-8 -*-#												||
#===========================Core Modules================================||
from os.path import abspath, dirname, join
#=======================================================================||
from condor import condor
from fxsquirl import fxsquirl
from nchantrs.libraries import pyqt, qpandas
#=======================================================================||
here = join(dirname(__file__),'')#										||
there = abspath(join('../../..'))#										||set path at pheonix level
log = False
#=======================================================================||
pxcfg = f'{here}/_data_/tablemodels.yaml'

class NchantdTableModel(qpandas.DataFrameModel):
	''' '''

	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		if parent:
			cfg = self.parent.config
		self.config = condor.instruct(pxcfg).select('NchantdTable')
		self.config.override(cfg)
		super(NchantdTableModel, self).__init__()

	def initModel(self):
		''' '''
		return self

	def createRecord(self, rid, data):
		''' '''
		self.parent.model.insertRecord()
		return self

	def editRecord(self, rid, data):
		''' '''
		self.parent.model.updateRecord()
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
