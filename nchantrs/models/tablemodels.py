
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

#=======================================================================||
here = join(dirname(__file__),'')#										||
there = abspath(join('../../..'))#										||set path at pheonix level
version = '0.0.0.0.0.0'#														||
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
	def initModel(self):
		''' '''
		return self
#		qpandas.DataFrameModel.__init__(self)
	# 	if log: print('CFG', cfg)
	#
	# 	self.loadData(app.src.getModelSrc('table', cfg))
	# def loadData(self, getter):
	# 	''' '''
	# 	while True:
	# 		data = next(getter, None)
	# 		if data == None:
	# 			break
	# 		self.data = DataFrame()
	#
	# 		yield self
	# 	yield None
	def nextRecord(self):
		''' '''
		return self
	def prevRecord(self):
		''' '''

		return self
	def refresh(self):
		''' '''
		return self
	def createRecord(self):
		''' '''
	def deleteRecord(self):
		''' '''
	def submitRecord(self):
		''' '''
