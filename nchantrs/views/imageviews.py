#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:   #																	||
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
from nchantrs.libraries import pyqt
from nchantrs.libraries import pandas_profiling, pandasgui
from nchantrs.libraries import sweetviz
from nchantrs.widgets import widgets
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
#===============================================================================||
class NchantdImageView(pyqt.QImageView):
	''' '''
	def __init__(self, app, cfg, parent=None):
		'''Create a Tab Layout View'''
		super(NchantdPaneView, self).__init__()
		pxcfg = f'{here}_data_/views.yaml'
		self.config = config.instruct(pxcfg).select('paneviews').override(cfg)
		self.configView()
	def configView(self, cols: dict={}):
		''' '''
		cfgview = self.config.dikt['image']['view']
		return self
