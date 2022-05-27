#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid: '57bb5386-14fd-484c-853e-1c06762434c1'  #							||
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
from pandas import DataFrame
#===============================================================================||
from condor import condor
from excalc import ts as calcts
from fxsquirl import fxsquirl
from fxsquirl import collector
from nchantrs.libraries import pyqt
from nchantrs.models.nodemodels import NchantdConnectorNodeModel
from nchantrs.views.nodeviews import NchantdConnectorNodeView
from nchantrs.widgets.items import NchantdItem
#===============================================================================||

#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/nodes.yaml')
class NchantdNode(NchantdItem):
	''' '''
	def __init__(self, item, nid, df=DataFrame(), parent=None):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdNode')
		if parent:
			self.config.override(parent.config)
		super(NchantdNode, self).__init__(item, nid, df, parent)
		self.parentItem = parent
		self.df = df
		self.item = item#data displayed in the tree node
		self.itemData = [item, nid]
		self.nid = nid
		#self.loadChildren(df, self, nid)
		self.model = NchantdConnectorNodeModel(self)
		self.view = NchantdConnectorNodeView(self)
	def addChildNode(self):
		''' '''
		return self
	def addSibilingNode(self):
		''' '''
		return self
	def initModel(self):
		''' '''
		self.model.initModel()
		return self
	def initView(self):
		''' '''
		self.view.initView()
		return self
	def initWidget(self):
		''' '''
		self.initModel()
		self.initView()
		return self
	def data(self, column):
		try:
			return self.itemData[column]
		except IndexError:
			return None
	def loadChildren(self, df, node, nid):
		''' '''
		children = df.loc[df.index[df['parentid'] == str(nid)].tolist()]
		for index, child in children.iterrows():
			item = NchantdNode(child['name'], child['nid'], df, node)
			node.appendRow(item)
			self.loadChildren(df, item, child['nid'])
			item.hasChildren(child['nid'])
		self.is_loaded = True
		return self
	def hasChildren(self, nid):
		''' '''
		self.is_expandable = True
		return self
class NchantdConnectorMultiNode(NchantdNode):
	''' '''
	def __init__(self):
		''' '''
		self.parent = parent
		if parent:
			cfg = self.parent.config
		self.src = src
		self.config = condor.instruct(pxcfg).select('NchantdMultiConnectorNode')
		self.config.override(cfg)
		self.model = NchantdMultiNodeConnectorModel(self)
		self.view = NchantdMultiNodeConnectorView(self)
	def addLeg(self):
		''' '''
	def updateConnectorEnd(self):
		''' '''
	def updateConnectorText(self):
		''' '''
class NchantdConnectorNode(NchantdNode):
	'''Allow for the connector itself to be an item with metadata about the
	relationship between nodes'''
	def __init__(self):
		''' '''
		self.parent = parent
		if parent:
			cfg = self.parent.config
		self.src = src
		self.config = condor.instruct(pxcfg).select('NchantdConnectorNode')
		self.config.override(cfg)
		self.model = NchantdNodeConnectorModel(self)
		self.view = NchantdNodeConnectorView(self)
class NchantdMultiParentNode(NchantdNode):
	''' '''
	def __init__(self, item, nid, df=DataFrame(), parent=None):
		''' '''
		self.parent = parent
		if parent:
			cfg = self.parent.config
		self.src = src
		self.config = condor.instruct(pxcfg).select('NchantdMultiParentNode')
		self.config.override(cfg)
		super(NchantdTreeNode, self).__init__()
		self.model = NchantdMultiParentNodeModel(self)
		self.view = NchantdMultiParentNodeView(self)
class NchantdRootNode(NchantdNode):
	''' '''
	def __init__(self, item, nid, df=DataFrame(), parent=None):
		''' '''
		self.parent = parent
		if parent:
			cfg = self.parent.config
		self.src = src
		self.config = condor.instruct(pxcfg).select('NchantdRootNode')
		self.config.override(cfg)
		super(NchantdTreeNode, self).__init__()
		self.model = NchantdRootNodeModel(self)
		self.view = NchantRootNodeView(self)
