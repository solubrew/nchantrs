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
#===============================================================================||
from condor import condor
from condor.thing import thingify
from fxsquirl import fxsquirl
#===============================================================================||
from nchantrs.libraries import pyqt
from nchantrs.models import models
from nchantrs.widgets import nodes
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_', 'tabsetmodels.yaml')

class NchantdTabSetModel(pyqt.QAbstractItemModel):
	'''Model class for a given tabset filled with data from both configuration
		files supplied and database sources configured in application'''
	version = '0.0.0.0.0.0'#														||
	def __init__(self, parent=None, src=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdTabSetModel')
		self.config.override(cfg)
		if log: print('Parent', parent)
		if parent != None:
			self.config.override(parent.config)
		super(NchantdTabSetModel, self).__init__()
		self.src = src
		self.tabsets = self.config.dikt['gui']['desktop']['tabsets']

	def initModel(self, pos, node=None, newInstance=False):
		'''Load Data from Source to initialize or refresh the model

		prior to initating this model the tabs table needs to be populated
		the configuration for generic tabsets is going to point it to the
		source view of tabs

		in some cases everything uses the same tabs and only the data gets changed

		'''


		cfg = self.parent.config.dikt['dstruct']['store']['config']
		tables = {'tabs': self.tabs}#key to functioning tree in current configuration
		for table, rows in tables.items():
			cols = cfg['table'][table]['columns']
			self.src.wrtr({table: DataFrame(rows, columns=cols)})#what is happening here...i think this is writing to the db?


		cfg = self.config.dikt['gui']['desktop']['layout'][pos]
		if cfg['<(SOURCE)>'] == None:
			view = self.config.dikt['<(SOURCE)>']['view']
		else:
			view = cfg['<(SOURCE)>']['view']
		print('View', view)
		df = self.src.getModelSrc('pane', 'view', view)# need to move to an inmem db
		self.src.cache.store[view] = df
		self.selectTabs(node, view)

		return self

	def addData(self):
		''' '''
		self.src
		return self

	def buildTabSet(self, pid, name, base, datatabs=[], i=0):
		''' '''
		tabset = self.config.dikt['gui']['desktop']['tabsets'][name]
		if log: print(f'Tabset Name {name}')
		if not tabset['tabs']:
			tab = ['Generic', 'apptab', 'nchantdmoonabs.widgets.NMBTab', '{}', pid, 0]
			if 'dtabs' in tabset.keys():
				if not tabset['dtabs']:
					self.tabs.append(tab + base)
					return self
		if tabset['tabs']:
			for i in range(len(tabset['tabs'])):
				data = tabset['tabs'][i][2]
				tabpath = tabset['tabs'][i][1]
				tab = [tabset['tabs'][i][0], 'apptab', tabpath, data, pid, i]
				self.tabs.append(tab + base)
			i += 1
		if isinstance(datatabs, list):
			for dtab in datatabs:
				if 'dtabs' not in tabset.keys():
					continue
				if not tabset['dtabs']:
					continue
				for name, tab in tabset['dtabs'].items():
					#if log: print('Make Tab', name.format(dtab), tab)
					load = [name.format(dtab), 'datatab', tab[0], tab[1], pid, i]
					self.tabs.append(load + base)
					i += 1
		elif isinstance(datatabs, dict):
			for dname, dtab in datatabs.items():
				if 'dtabs' not in tabset.keys():
					continue
				if not tabset['dtabs']:
					continue
				for name, tab in tabset['dtabs'].items():
#					if log: print('Make DTab\n', name.format(dname), dtab)
					dtab = j.dumps(dtab)
					load = [name.format(dname), 'datatab', tab[0], dtab, pid, i]
					self.tabs.append(load + base)
					i += 1
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

	def selectTabs(self, node, view):
		''' '''
		if node == None:
			node = nodes.NchantdNode(1, 1)
		pid = node.nid
		self.node = node
		custom = False
		self.tabs = []
		df = self.src.cache.store[view]
		if df.empty:
			tabs =  DataFrame([])
		else:
			tabs = df.loc[df.index[df['parentid'] == str(pid)].tolist()]
		tabsd = tabs.to_dict(orient='records')
		for tab in tabsd:
			#tabW = thingify(f"nchantrs.widgets.{tab['widget']}")
			#tabW = tabW(self, {'tab': tab}).initWidget()
			#if log: print('TABW', tabW)
			self.tabs.append(tab)
		if custom:
			tabW = NchantdSelectorTab().initWidget()# what is this for?
			self.tabs.append(tabW)
		return self
#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
