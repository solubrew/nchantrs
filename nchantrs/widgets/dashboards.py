#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	DOCid:   #																	||
	name:   #																	||
	description: >  #															||
		  #			||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	path: <[LEXIvrs]>  #														||
	outline: <[outline]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#===============================Core Modules====================================||
from os.path import abspath, dirname, exists, join
#===============================================================================||
from condor import condor
from condor.thing import thingify
from nchantrs.libraries import pyqt
from nchantrs.libraries import pandas_profiling, pandasgui
from nchantrs.libraries import sweetviz
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
#===============================================================================||
class NchantdDashboard(pyqt.QWidget):
	''' '''
	def __init__(self, app, cfg):
		''' '''
		pyqt.QWidget.__init__(self)
		self.view = NchantdDashboardView(app, cfg)
		self.model = NchantdDashboardModel(app, cfg)
		self.view.setModel(self.model)
		self.layout = pyqt.QVBoxLayout()
		self.layout.addWidget(self.view)
		self.setLayout(self.layout)

	def initModel(self):
		''' '''
		return self

	def initView(self):
		''' '''
		return self

	def initWidget(self):
		''' '''
		return self

	def onRefresh(self):
		''' '''
		return self

	def refresh(self):
		''' '''
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
