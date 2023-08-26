#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: 'b78558a7-2fde-4ae2-8b7e-c56b61af3239'
	name:
	description: >
	expirary: <[expiration]>
	version: <[version]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================Core Modules====================================||
from os.path import abspath, dirname, join
#===============================================================================||
from condor import condor, thing#												||
from nchantrs.libraries import pyqt
from nchantrs.widgets.charts import baseCharts
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/financialCharts.yaml')

class NchantdRSI(baseCharts.NchantdTimeSeriesChart):
	'''Relative Strength Index Chart'''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdRSIChart')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdRSI, self).__init__(parent)


class NchantdPriceHistoryChart(baseCharts.NchantdTimeSeriesChart):
	'''Price History over Time Chart'''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdPriceHistoryChart')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdPriceHistoryChart, self).__init__(parent)

	def bollinger_bands(self):
		pass

class NchantdVolumeChart(baseCharts.NchantdTimeSeriesChart):
	'''Volume Bar Chart'''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdVolumeChart')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)

class NchantdMACDChart(baseCharts.NchantdTimeSeriesChart):
	''' '''

	def __init__(self):
		''' '''


#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
