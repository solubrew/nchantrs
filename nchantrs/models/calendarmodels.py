#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Nchantrs@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid: ''  #																||
	name: Nchnated Calendar Python Document#									||
	description: >  #															||
	expirary: '<[expiration]>'  #												||
	version: '<[version]>'  #													||
	path: '<[LEXIvrs]>'  #														||
	outline: '<[outline]>'  #													||
	authority: 'document|this'  #												||
	security: 'sec|lvl2'  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#================================Core Modules===================================||
from os.path import abspath, dirname, exists, join
#===============================================================================||
from nchantrs.libraries import pyqt
#===============================================================================||
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
#===============================================================================||
class NchantdCalendarModel():
	''' '''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.src = parent.src
		self.config = condor.instruct(pxcfg).select('NchantdCalendarModel')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdCalendarModel, self).__init__(parent)
	def initModel(self):
		''' '''
		self.src.createTables(self.config.dikt['tables'])
		self.src.createViews(self.config.dikt['views'])
