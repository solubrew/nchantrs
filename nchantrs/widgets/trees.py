#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:   #																	||
	name:	#																	||
	description: >  #															||
		Develop Qt5TreeModel module and leverage it instead of adhoc
		building it here  #			||
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
from os.path import abspath, dirname, join
#===============================================================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.views.treeviews import NchantdTreeView, NchantdTimeTreeView
from nchantrs.views.treeviews import NchantdFileSystemView
from nchantrs.models.treemodels import NchantdFileSystemModel, NchantdTreeModel
from nchantrs.models.treemodels import NchantdTimeTreeModel
from nchantrs.widgets import tabsets
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = False
#===============================================================================||
pxcfg = f'{here}_data_/trees.yaml'

class NchantdTree(pyqt.QWidget):
	'''Generic Tree Widget built to integrate Nchantd models and views'''
	def __init__(self, parent=None, cfg={}, root=None):
		''' '''
#		if log: print('NchantdTreeParent', parent)
		self.parent = parent
		self.config = condor.instruct(pxcfg).override(cfg)
		if parent:
			self.config.override(self.parent.config)
#		if log: print('Nchantd Tree Config', self.config.dikt.keys())
		super(NchantdTree, self).__init__()
		self.src = self.parent.src
		self.newInstance = self.parent.newInstance
		self.model = NchantdTreeModel(self, root, self.src)
		self.view = NchantdTreeView(self)

	def addNode(self):
		''' '''

	def initModel(self):
		''' '''
		self.model.initModel()
		return self

	def initView(self):
		''' '''
		self.view.initView()
		print('Set Layout')
		self.setLayout(self.view.layout)
		print('Layout Set')
		return self

	def initWidget(self, pos=None):
		''' '''
		self.initModel()
		print('InitTreeView')
		self.initView()
		print('TreeViewInitated')
		return self

	def canFetchMore(self, index):
		''' '''
		node = self.getNode(index)
		if node.is_dir and not node.is_traversed:
			return True
		return False
		# called if canFetchMore returns True, then dynamically inserts nodes required for
		# directory contents

	def updateTabs(self, node, view='center'):
		''' '''
		self.parent.pane[view].updateTabSet(node, 'tabs')
		return self


class NchantdCustomTree(NchantdTree):
	''' '''
	def __init__(self, parent=None, cfg={}, root=None):
		''' '''
		self.src = parent.src
		self.config = condor.instruct(pxcfg).select('NchantdCustomTree')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdCustomTree, self).__init__(parent, cfg, root)

class NchantdFileSystemTree(NchantdTree):
	''' '''
	def __init__(self, parent=None, cfg={}, root=None):
		''' '''
		self.src = parent.src
		self.config = condor.instruct(pxcfg).select('NchantdFileSystemTree')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdFileSystemTree, self).__init__(parent, cfg, root)
		self.model = NchantdFileSystemModel(self)
		self.view = NchantdFileSystemView(self)

class NchantdMindTree(NchantdTree):
	'''Provide a Basic Mind Map Widget'''
	def __init__(self, parent=None, cfg={}, root=None):
		''' '''
		self.src = src
		self.config = condor.instruct(pxcfg).select('NchantdConnector')
		self.config.override(cfg)
		if parent:
			self.config.override(self.parent.config)
		self.model = NchantdNodeConnectorModel(self)
		self.view = NchantdNodeConnectorView(self)

	def initModel(self):
		''' '''
		return self

	def initView(self):
		''' '''

		return self

	def initWidget(self):
		''' '''
		self.model()
		self.view()
		return self

	def addMultiParentNode(self):
		'''Add a child node with the capability of identifying multiple parents
			The multiparent data is used to direct connector nodes combined with
			the nodes meta data
		'''
		return self

	def addFreeNode(self):
		'''This actually will have its parent as the document but in the view
			it will appear to have no parent '''

	def addConnectorNode(self):
		'''Allow for various types of connectors for children this is more of a
		metadata for the node relationship to other nodes....could also allow
		for labeling of the connection and other complex iconographic
		information '''
		return self

	def attachParent(self):
		''' '''
		return self

	def attachChild(self):
		''' '''
		return self

	def detachParent(self):
		''' '''
		return self

	def detachParents(self):
		''' '''
		return self

	def detachChild(self):
		''' '''
		return self

	def detachChildren(self):
		''' '''
		self.getChildren()
		return self

	def getChild(self):
		''' '''
		return self

	def getChildren(self):
		''' '''
		return self

	def getParent(self):
		''' '''
		return self

	def getParents(self):
		''' '''
		return self

	def removeNode(self):
		''' '''
		self.detachParents(self)
		self.detachChildren(self)
		return self


class NchantdTimeTree(NchantdTree):
	''' '''
	def __init__(self, parent=None, cfg={}, root=None):
		if log: print('NchantdTimeTreeParent', parent)
		self.parent = parent
		self.src = parent.model.src
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).override(cfg)
		print('CFG', self.config)
		print('Time Root', root)
		super(NchantdTimeTree, self).__init__(parent, self.config, root)
		self.model = NchantdTimeTreeModel(self, root)
		self.view = NchantdTimeTreeView(self)
#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
