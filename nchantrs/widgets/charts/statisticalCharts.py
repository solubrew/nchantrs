#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: '06b882c6-c2f2-4109-b062-da103c01b3bc'
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
pxcfg = join(abspath(here), '_data_/statisticalCharts.yaml')

class NchantdParetoChart(baseCharts.NchantdChart):
	''' '''

	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdParetoChart')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdParetoChart, self).__init__(parent)


class NchantdCountChart(baseCharts.NchantdChart):
	''' '''

	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdCountChart')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdCountChart, self).__init__(parent)


class NchantdPercentageChart(baseCharts.NchantdChart):
	''' '''

	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdPercentageChart')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdPercentageChart, self).__init__(parent)


#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
