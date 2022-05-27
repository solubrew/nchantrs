#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:   #																	||
	name:	#																	||
	description: >  #															||

	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	path: <[LEXIvrs]>  #														||
	outline: <[outline]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#================================Core Modules===================================||
from os.path import abspath, dirname, join
#===============================================================================||
from fxsquirl import fxsquirl
from nchantrs.libraries import pyqt
#===============================================================================||

#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
#===============================================================================||
class DashboardModel(pyqt.QAbstractItemModel):
	''' '''
	def __init__(self, app, cfg: dict={}, parent=None):
		''' '''
		super(DashboardModel, self).__init__(parent)
		self.app = app
		self.src = app.src.getModelSrc('entry', cfg['outline'])
		self.addItems(self.src, parent)
	def data(self):
		''' '''
		return self
	def mapItems(self):
		''' '''
		return self
