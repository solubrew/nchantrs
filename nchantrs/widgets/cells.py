#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:   #																	||
	name:	#																	||
	description: >  #															||
		Extendes the basic Item widget into the Nchantd Framework for cells
		with in a table...this will need to account for both data and metadata
		for the cell
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
from pandas import DataFrame
#===============================================================================||
from condor import condor
from excalc import ts as calcts
from fxsquirl import fxsquirl
from fxsquirl import collector
from nchantrs.libraries import pyqt
#===============================================================================||

#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = f'{here}/_data_/cells.yaml'
class NchantdCell(NchantdItem):
	''' '''
	def __init__(self):
		''' '''
		self.parent = parent
		if parent:
			cfg = self.parent.config
		self.src = src
		self.config = condor.instruct(pxcfg).select('NchantdCell')
		self.config.override(cfg)
		self.model = NchantdCellModel(self)
		self.view = NchantdCellView(self)
	def defineAttrs(self):
		''' '''
		self.text_color = ''
		self.bg_color = ''
		self.bg_focus_color = ''
		self.text_focus_color = ''
		self.row = ''
		self.column = ''
		self.tab = ''
		return self
