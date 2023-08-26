#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>: '' #								||
	docid:   #																	||
	name: Nchantrs Module Views Forms Python Excecution Document  #			||
	description: >  #															||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#================================Core Modules===================================||
from os.path import abspath, dirname, exists, join
from sys import argv, exit
#===============================================================================||
from condor import condor, thing#												||
from nchantrs.libraries import pyqt
from nchantrs.models.tablemodels import NchantdTableModel
from nchantrs.widgets.controls import NchantdSubmissionButtons, NchantdNavigationButtons
from nchantrs.widgets.editors import NchantdEntryEditor
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/forms.yaml')#								||assign default config

class NchantdDynamicRecordEntryFormView():
	''' '''
	def __init__(self, parent):
		''' '''
		self.parent = parent
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('NchantdDynamicRecordEntryFormView')
		self.config.override(cfg)
		super(NchantdDynamicRecordEntryFormView, self).__init__()

	def initView(self):
		''' '''
		return self

	def initContextMenu(self):
		''' '''
		return self

	def initTriggers(self):
		''' '''
		return self

	def initUI(self):
		''' '''
		return self

	def onRightClick(self):
		''' '''
		return self

	def onLeftDoubleClick(self):
		''' '''
		return self

	def onLeftClick(self):
		''' '''
		return self

	def onMiddleClick(self):
		''' '''
		return self
