#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid: '3a578013-a3c0-4346-a526-20e4bc6510de'  #							||
	name:   #																	||
	description: >  #															||
		  #			||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#===============================Core Modules====================================||
from os.path import abspath, dirname, exists, join
#===============================================================================||
from condor import condor
from nchantrs.libraries import pyqt, pandas_profiling, pandasgui, sweetviz
from nchantrs.models.dashboardmodels import NchantdDashboardModel
from nchantrs.views.dashboardviews import NchantdDashboardView
from nchantrs.widgets import charts, tables
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/dashboard.yaml')

class NchantdDashboard(pyqt.QWidget):
	''' '''

	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('NchantdDashboard')
		self.config.override(cfg)
		super(NchantdDashboard, self).__init__()
		self.model = NchantdDashboardModel(self)
		self.view = NchantdDashboardView(self)

	def initModel(self):
		''' '''
		self.model.initModel()
		return self

	def initView(self):
		''' '''
		self.view.initView()
		return self

	def initWidget(self):
		''' '''
		self.initModel()
		self.initView()
		self.view.setModel(self.model)
		return self

	def onRefresh(self):
		''' '''
		return self

	def refresh(self):
		''' '''
		return self

class NchantdAnalysisDashboard(NchantdDashboard):
	''' '''

	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('NchantdDashboard')
		self.config.override(cfg)
		super(NchantdAnalysisDashboard, self).__init__(parent, self.config)
		self.buildDashboard()

	def buildDashboard(self):
		''' '''
		self.chart = charts.NchantdTimeSeriesChart(self, self.config)
		self.chart.initWidget()
		self.table = tables.NchantdTable(self).initWidget()
		return self


class NchantdNEWSDashboard():
	'''A standardized dashboard for displaying NEWS to the user where the
		specific NEWS content is pulled from various sources using a pluggable
		algorythm'''
	def __init__(self):
		''' '''


#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
