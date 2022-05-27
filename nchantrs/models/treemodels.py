#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid: 'ce981f8c-de77-4054-ae2f-e30049bb318a'  #							||
	name:	#																	||
	description: >  #															||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#================================Core Modules===================================||
from os.path import abspath, dirname, join
#===============================================================================||
from pandas import DataFrame, to_numeric
#===============================================================================||
from condor import condor
from excalc import ts as calcts
from fxsquirl import fxsquirl
from fxsquirl import collector
from nchantrs.libraries import pyqt
from nchantrs.models import models
from nchantrs.widgets.nodes import NchantdNode
#===============================================================================||

#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/treemodels.yaml')
class NchantdTreeModel(pyqt.QStandardItemModel):
	''' '''
	def __init__(self, parent=None, root=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdTreeModel')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		self.src = parent.src
		self.nodecolumns = self.config.dikt['tables']['trnodes']['columns']
		self.nodetables = 'trnodes'
		self.nodes = []
		super(NchantdTreeModel, self).__init__()
		# self.root = root
		# if root == None:
		self.root = self.invisibleRootItem()#the entire tree is connected to this
		self.root.config = self.config
		self.newNodes = []

	def initModel(self, newInstance=False):
		''' '''
		if newInstance:
			tables = self.config.dikt['NchantdTreeModel']['tables']
			self.src.createTables(tables)
		position = 'left'
		cfg = self.config.dikt['gui']['desktop']['layout'][position]
		#if there is no source need to get the default source
		#which means pulling the dict walk from getModelSrc back here

		if cfg['<(SOURCE)>'] == None:
			view = self.config.dikt['<(SOURCE)>']['view']
		else:
			view = cfg['<(SOURCE)>']['view']
		df = self.src.getModelSrc('tree', 'view', view)
		multiroot = df.loc[df.index[df['parentid'] == str(0)].tolist()]
		multiroot.sort_values(by=['position'])
		if log: print('MultiRoot\n', multiroot)
		for index, root in multiroot.iterrows():
			if log: print('Name\n', root['name'])
			item = NchantdNode(root['name'], root['nid'], df, self.root)
			item.initWidget().loadChildren(df, item, item.nid)
			self.root.appendRow(item)
		return self

	def addModel(self):
		''' '''
		return self

	def addNode(self, nid, name, ntype, pid, pos, base, tabset, expandable=0):
		''' '''
		data = [nid, name, ntype, pid, pos, tabset] + base + [expandable,]
		self.nodes.append(data)
		nid += 1
		return nid

	def deleteNode(self):
		''' '''
		return self

	def insertColumns(self, position, columns, parent=pyqt.QModelIndex()):
		''' '''
		self.beginInsertColumns(parent, position, position + columns - 1)
		success = self.root.insertColumns(position, columns)
		self.endInsertColumns()
		return success

	def insertRows(self, position, rows, parent=pyqt.QModelIndex()):
		''' '''
		parentItem = self.getItem(parent)
		self.beginInsertRows(parent, position, position + rows - 1)
		success = parentItem.insertChildren(position, rows, self.root.columnCount())
		self.endInsertRows()#											||
		return success

	def updateStatus(self, status):
		'''Modifiy Application widgetStatus for driving global events in other \
			widget stacks'''
		#rerun the 2ndpane build sequence based on the tabaset of the node
		#self.app.updateStatus(self, status)
		return self


class NchantdMappedTreeModel(NchantdTreeModel):
	''' '''
	def __init__(self):
		''' '''


class NchantdTimeTreeModel(NchantdTreeModel):
	'''Nchantd Time Tree Model builds a dataset of year, month, week, day
		hiearchies with a few variations for how the nodes and tabs are created
		for each of the levels '''
	def __init__(self, parent=None, root=None, cfg={}):
		''' '''
		if log: print('NchantdTimeTreeModelParent', parent.config.dikt.keys())
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdTimeTreeModel')
		if parent:
			self.config.override(parent.config)
		root = None
		super(NchantdTimeTreeModel, self).__init__(parent, root, cfg)

	def initData(self, pos=0, pid=0, nid=None):
		'''Generate a table of date nodes for initilization of a timeline based
			tree widget
			need to get first data from data? or hand it the date?'''
		format = '%d/%m/%Y %H:%M:%S'
		if pid != 0 and nid == None:
			node = self.src.getNode(pid)
			nid = node.nid
		else:
			nid = 1
		startdate = calcts.getDateObject('01/01/2022 00:00:00', format)
		enddate = calcts.getTodayObject()
		base = [0, 1, 0, 1, 0, 0, 0]
		for year in range(int(enddate.year) - int(startdate.year)+5):
			year += startdate.year
			nid = self.addYearNode(nid, year, pid, pos, base, year)
			pos += 1
		df = DataFrame(self.nodes, columns=self.nodecolumns)
		self.src.wrtr({'trnodes': df})

	def addYearNode(self, nid, name, pid, pos, base, year):
		''' '''
		rnid = self.addNode(nid, name, 'node', pid, pos, base, 'yearsummary')
		pid = nid
		for month in range(1, 13):
			name = calcts.getMonthLabel(month)
			tabset = 'NchantdMonthOfDaysTabSet'
			rnid = self.addNode(rnid, name, 'node', pid, pos, base, tabset)
			pos += 1
		return rnid

	def addCenturyNode(self):
		''' '''
		return self

	def addDecadeNode():
		''' '''
		return self

	def addEpochNode(self):
		''' '''
		return self

	def addWeekNode(self):
		''' '''
		return self
#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
