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
from pandas import DataFrame, to_numeric
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
class NchantdItemView():
	''' '''
	def __init__(self, parent):
		''' '''
		pxcfg = f'{here}_data_/treeviews.yaml'
		self.parent = parent
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).override(cfg)
		super(NchantdItemView, self).__init__()
	def initView(self):
		self.layout = pyqt.QVBoxLayout()

		self.setModel(self.parent.model)
		self.initUI()
		self.initContextMenu()
		self.initTriggers()
	def initContextMenu(self):
		''' '''
		self.setContextMenuPolicy(pyqt.Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.onRightClick)
		return self
	def initTriggers(self):
		''' '''
		self.doubleClicked.connect(self.onLeftDoubleClick)
		self.expanded.connect(self.onExpand)
		self.clicked.connect(self.onLeftClick)
		return self
	def initUI(self):
		''' '''
		return self
	def onExpand(self):
		''' '''
		return self
	def onRightClick(self):
		''' '''
	def onLeftDoubleClick(self, signal):
		return self
	def onLeftClick(self, signal):
		return self
	def onMiddleClick(self):
		''' '''
		return self
	def onSelection(self, fx, mod=None):
		'''On selection of tree node load data for tabs in center widget'''
		event.on_clickleft_press(fx)

		return
	def onDeselection(self, fx, mod=None):
		'''On deslection of tree node save any changes to node options'''
		event.on_clickleft_release(fx)
		return
	def onEnter(self, fx, mod=None):
		'''Need to build if a node was selected an enter create a new sibling
			node. shift-enter creates a new child node, ctrl-enter creates
			a new tab in the node'''
		event.on_enter_kp(fx, mod)
		return
	def onDelete(self, fx, mod=None):
		'''Launch Dialog to confirm deletion of node, which marks as deleted in database
			and is not removed until a database cleanup is run'''
		#expand this to allow for multiple connections to content and only delete
		#connections until no connections are left then remove content...this requires
		#the knowledge of parents by their children
