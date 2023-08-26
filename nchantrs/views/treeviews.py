#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid: 'a4955210-9422-43dd-8a94-6f9f90568004'  #							||
	name:	#																	||
	description: >  #															||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
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
from nchantrs.logr import tree
from subtrix import subtrix
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/treeviews.yaml')
class NchantdTreeView(pyqt.QTreeView):
	''' '''
	def __init__(self, parent):
		''' '''
		self.parent = parent
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('NchantdTreeView')
		self.config.override(cfg)
		super(NchantdTreeView, self).__init__()

	def initView(self):
		self.layout = pyqt.QVBoxLayout()

		# path = join(abspath(dirname(__file__)), '..')
		# url = self.config.dikt['url'].format(path)
		# load = [self.config.dikt['stylesheet'], {'url': url}]
		# stylesheet = subtrix.mechanism(*load).run()[0]
		# self.setStyleSheet(stylesheet)

		self.layout.addWidget(self)
		self.model = self.parent.model
		self.setModel(self.model)
		self.initUI()
		self.initContextMenu()
		self.initTriggers()
		return self

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
		cfgview = self.config.dikt
		self.setFixedWidth(cfgview['FixedWidth'])
		self.setAnimated(cfgview['Animated'])
		self.setIndentation(cfgview['IndentSize'])
		return self

	def mousePressEvent(self, event):
		''' '''
		#tree.mousePressEventLog(event, 1)
		if event.button() == pyqt.Qt.RightButton:
			pass
		else:
			pass
			#self.setNodeFocus(event.data)
		super().mousePressEvent(event)

	def onExpand(self):
		''' '''
		return self

	def onRightClick(self):
		''' '''

	def onLeftDoubleClick(self, signal):
		'''launch a dialog that allows for modification of parameters
				of the tree node if node is marked as editable:
				- font/style/color of text
				- icon
				- position
				- readonly
				'''
		print('Tested Double Click')
		node = self.model.getNodeData(signal.data())
		if node['editable']:
			dialog = self.config.dikt['nodeeditordialog']['widget']
			launchDialog(dialog, node)
		return self

	def onLeftClick(self, signal):
		'''Need to send signal to load center widget with correct tabset and
		populate those tabs with data based on the node selected

		will need to run the pane building function from the nchantrs.Cloak

		'''
		tree.leftClickSignalLog(signal)
		if log: print('Tree View Model\n', self.model, '\n', self.model.__dir__())
		node = self.model.itemFromIndex(signal)

		self.parent.updateTabs(node)
		#print('Node', node.__dir__())
		#self.model.updateStatus(signal.data())
		#self.loadTabData(signal.data())
		#use this to store the active node in a application level variable
		#and setup a listner to trigger the tabset rebuild on change
		#self.emit(NodeSelection(signal.data()))
		return self

	def onMiddleClick(self):
		''' '''
		return self
	def onRightClick(self, position=0):
		''' '''
		#need to replace with build menu
		#here is where context will be introduced to the action decision tree
		indexes = self.treeView.selectedIndexes()
		if len(indexes) > 0:
			level = 0
			index = indexes[0]
			while index.parent().isValid():
				index = index.parent()
				level += 1
		menu = pyqt.QMenu()
		if level == 0:
			menu.addAction(self.tr("Edit Node Options"))
		elif level == 1:
			menu.addAction(self.tr("Edit Workbook Options"))
		elif level == 2:
			menu.addAction(self.tr("Edit object"))
		menu.exec_(self.treeView.viewport().mapToGlobal(position))
	def onNodeSelection(self, fx, mod=None):
		'''On selection of tree node load data for tabs in center widget'''
		event.on_clickleft_press(fx)

		return

	def onNodeDeselection(self, fx, mod=None):
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


class NchantdTimeTreeView(NchantdTreeView):
	''' '''
	def __init__(self, parent):
		''' '''
		pxcfg = f'{here}_data_/treeviews.yaml'
		self.parent = parent
		self.model = parent.model
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).override(cfg)
		super(NchantdTimeTreeView, self).__init__(parent)


class NchantdCustomTreeview(NchantdTreeView):
	''' '''
	def __init__(self, parent):
		''' '''
		pxcfg = f'{here}_data_/treeviews.yaml'
		self.parent = parent
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).override(cfg)
		super(NchantdCustomTreeView, self).__init__(parent)

class NchantdFileSystemView(NchantdTreeView):
	''' '''
	def __init__(self, parent):
		''' '''
		pxcfg = f'{here}_data_/treeviews.yaml'
		self.parent = parent
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).override(cfg)
		super(NchantdFileSystemView, self).__init__(parent)

#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
