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
from pandas import DataFrame

from condor import condor
from condor.thing import thingify
from fxsquirl import fxsquirl
from nchantrs.libraries import pyqt
from nchantrs.models import models
from nchantrs.widgets import nodes
#===============================================================================||

#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/tabsetmodels.yaml')
class NchantdTabSetModel(pyqt.QAbstractItemModel):
	'''Model class for a given tabset filled with data from both configuration
		files supplied and database sources configured in application'''
	def __init__(self, parent=None, src=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdTabSetModel')
		self.config.override(cfg)
		if log: print('Parent', parent)
		if parent != None:
#			if log: print('Nchantd TabSet Model Parent Config', self.parent.config.dikt.keys())
			self.config.override(parent.config)
#		if log: print('Nchantd TabSet Model Config', self.config.dikt.keys())
		super(NchantdTabSetModel, self).__init__()
		self.src = src

	def initModel(self, pos, node=None, newInstance=False):
		'''Load Data from Source to initialize or refresh the model '''
		cfg = self.config.dikt['gui']['desktop']['layout'][pos]
		if cfg['<(SOURCE)>'] == None:
			view = self.config.dikt['<(SOURCE)>']['view']
		else:
			view = cfg['<(SOURCE)>']['view']
		df = self.src.getModelSrc('pane', 'view', view)# need to move to an inmem db
		self.src.cache.store[view] = df
		if log: print(f'Tabset Model DF {df}')
		self.selectTabs(node, view)
		return self

	def selectTabs(self, node, view):
		''' '''
		if node == None:
			node = nodes.NchantdNode(1, 1)
		pid = node.nid
		self.node = node
		custom = False
		self.tabs = []
		df = self.src.cache.store[view]
		if log: print('Select Tabs', df[df['parentid'] == '1'])
		if df.empty:
			tabs =  DataFrame([])
		else:
			tabs = df.loc[df.index[df['parentid'] == str(pid)].tolist()]
		tabsd = tabs.to_dict(orient='records')
		if log: print('TABSD', tabsd)
		for tab in tabsd:
			#tabW = thingify(f"nchantrs.widgets.{tab['widget']}")
			#tabW = tabW(self, {'tab': tab}).initWidget()
			#if log: print('TABW', tabW)
			self.tabs.append(tab)
		if custom:
			tabW = NchantdSelectorTab().initWidget()
			self.tabs.append(tabW)
		return self

	def addData(self):
		''' '''
		self.src
		return self

	def columnCount(self, arg):
		''' '''
		return 0

	def rowCount(self, arg):
		''' '''
		return 0

	def addTab(self, nid, name, pid, pos, widget, base):
		''' '''
		self.tabs.append([nid, name, 'tab', pid, pos, widget] + base + [0])
		return nid + 1

	def deleteTab(self):
		''' '''
		return self

	def editTab(self):
		''' '''
		return self

	def saveTab(self):
		''' '''
		return self
#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
