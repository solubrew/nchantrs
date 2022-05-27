#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: 'e49e63fd-aad8-4ae3-b176-8ca67718fac6'
	name:
	description: >
		leverage visualizer to generate charts to displayed
		through nchantrs or warlock via an integrated nchantrs browser
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
import matplotlib
from numpy import arange, sin, pi
import matplotlib.pyplot as plt, seaborn as sns
try:
	matplotlib.use("Qt5Agg")
	from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
	from matplotlib.figure import Figure
except:
	pass#need other plotting options for non pyQT-guis and cmdline style programs
#===============================================================================||
from condor import condor, thing#												||
from nchantrs.libraries import pyqt
from nchantrs import utils
from nchantrs.models import tablemodels
from nchantrs.views import tableviews
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
#===============================================================================||
pxcfg = join(abspath(here), '_data_/charts.yaml')
class NchantdChart(FigureCanvas):
	"""A canvas that updates itself every second with a new plot."""
	def __init__(self, parent=None, cfg={}, fig=None, df=None):
		''' '''
		width, height, dpi, = 600, 4, 100
		self.fig = fig
		if self.fig == None:
			self.fig = Figure(figsize=(width, height), dpi=dpi)
		#plt.figure(figsize = (600, 4))
		#self.axes = self.fig.add_subplot(111)
		try:
			self.axes.hold(False)		# We want the axes cleared every time plot() is called
		except:
			pass
		sns.set_theme(style="darkgrid")
		plt.style.use('dark_background')
		FigureCanvas.__init__(self, self.fig)
		FigureCanvas.setSizePolicy(self, pyqt.QSizePolicy.Expanding,
												   pyqt.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		self.setParent(parent)

	def initWidget(self):
		''' '''
		self.compute_initial_figure()
		self.update_figure()
		return self

	def compute_initial_figure(self):
		''' '''
		pass

	def update_figure(self):
		''' '''
		pass


class NchantdTimeSeriesChart(NchantdChart):
	''' '''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdTimeSeriesChart')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdTimeSeriesChart, self).__init__(parent)

	def initWidget(self):
		''' '''
		return self


class NchantdRSI(NchantdTimeSeriesChart):
	'''Relative Strength Index Chart'''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdRSIChart')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdRSI, self).__init__(parent)


class NchantdPriceHistoryChart(NchantdTimeSeriesChart):
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


class NchantdVolumeChart(NchantdChart):
	'''Volume Bar Chart'''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdVolumeChart')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)


class NchantdSMAChart(NchantdTimeSeriesChart):
	'''Simple Moving Average Chart'''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdSMAChart')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)


class NchantdWMAChart(NchantdTimeSeriesChart):
	'''Weighted Moving Average Chart '''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdWMAChart')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)


class NchantdParetoChart(NchantdChart):
	''' '''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdParetoChart')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdParetoChart, self).__init__(parent)


class NchantdCountChart(NchantdChart):
	''' '''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdCountChart')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdCountChart, self).__init__(parent)


class NchantdPercentageChart(NchantdChart):
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
