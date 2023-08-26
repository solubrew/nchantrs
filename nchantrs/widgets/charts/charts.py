#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
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
from nchantrs.widgets.charts.baseCharts import *
from nchantrs.widgets.charts.engineeringCharts import *

from nchantrs.widgets.charts.statisticalCharts import *
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/charts.yaml')


#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
