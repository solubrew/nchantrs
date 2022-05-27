#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	DOCid:   #																	||
	name:   #																	||
	description: >  #															||
		  #			||
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
from os.path import abspath, dirname, exists, join
#===============================================================================||
from condor import condor
from condor.thing import thingify
from nchantrs.libraries import pyqt
from nchantrs.models import tabsetmodels
from nchantrs.logr import tabset
from nchantrs.widgets import widgets
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/tabsets.yaml')
class NchantdTabSet(pyqt.QTabWidget):
	'''Nchantd Tab Set provides a widget to show multiple tabs pullig data from
		the Nchantd Tab Set Model and displaying it in the application using
		the Nchantd Tab Set View'''
	def __init__(self, parent=None, cfg={}):
		'''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdTabSet')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdTabSet, self).__init__()
		self.src = self.parent.src
		self.model = tabsetmodels.NchantdTabSetModel(self, self.src)
		self.currenttabn = 0

	def initModel(self, pos, pid, newInstance=False):
		''' '''
		self.model.initModel(pos, pid, newInstance)
		return self

	def initTriggers(self):
		self.currentChanged.connect(self.onTabFocus)

	def initWidget(self, pos, node=None, newInstance=False):
		''' '''
		self.setTabPosition(pyqt.QTabWidget.South)
		self.initModel(pos, node, newInstance)
		self.buildTabSet()
		self.initTriggers()
		self.initUI()
		return self

	def initUI(self):
		''' '''
		cfgview = self.config.dikt['size']
		self.setFixedWidth(cfgview['w'])
		return self

	def buildTabSet(self, tabn=0):
		'''Create a set of tabs'''
		cnt = 0
		if log: print('Start Build Tabset', self.model.tabs)
		for tab in self.model.tabs:
			if cnt == tabn:#this way we can limit the time spent rendering nonvisible tabs
				tabW = self.buildTab(tabn)# not sure why the model needs to be the parent but it works
				self.currenttabn = tabn
			else:
				tabW = pyqt.QWidget()
			self.addTab(tabW, tab['name'])
			cnt += 1
		if log: print('End Build')
		return self

	def buildTab(self, tabn):
		''' '''
		tab = self.model.tabs[tabn]
		if log: print('Build Tab', tabn, '\n', tab['widget'])
		tabW = thingify(f"{tab['widget']}")
		if not tabW:
			if log: print('Thingification of Tab Failed')
			tabW = thingify(f"nchantrs.widgets.{tab['widget']}")
		tabWDGT = tabW(self, {'tab': tab}).initWidget()
		tabWDGT.name = tab['name']
		return tabWDGT

	def onTabFocus(self, tabn):
		''''''
		if log: print('TABN', tabn)
		self.lasttabn = self.currenttabn
		self.currenttabn = tabn
		if tabn < 0:
			self.onTabSetDefocus(self.lasttabn)
			return self
		if self.lasttabn != tabn:
			tabW = self.buildTab(tabn)
			self.currentChanged.disconnect(self.onTabFocus)
			self.insertTab(tabn, tabW, tabW.name)
			self.removeTab(tabn+1)
			self.setCurrentIndex(tabn)
			self.update()
			self.currentChanged.connect(self.onTabFocus)
		return self

	def onTabSetDefocus(self, tabn):
		''' '''
		#save data changes from last tab
		self.model.tabs[tabn].updateData()

		return self

	def refreshTabSet(self):
		'''Get data from the model via the chunker by passing it various
		configurations given the selected node and tabset position
		ex. nodeid: 2, position: center -> tabset
		'''
		self.model.src.load()

	def updateTabSet(self, node, view):
		''' '''
		if log: print('Start Tabset update')
		try:
			self.currentChanged.disconnect(self.onTabFocus)
		except Exception as e:
			if log: print(f'Disconnect Failed due to {e}')
		self.clear()
		self.currentChanged.connect(self.onTabFocus)
		if log: print('Tabs cleared')
		self.model.selectTabs(node, view)
		if log: print('New model Initiated')
		self.buildTabSet()
		if log: print('End Tabset udpate')

	def focusInEvent(self, event):
		''' '''
		print('Tab has Focus')
		super().focusInEvent(event)

	def focusOutEvent(self, event):
		''' '''
		print('Tab lost Focus')
		super().focusOutEvent(event)

	def mousePressEvent(self, event):
		''' '''
		tabset.mousePressEventLog(event, 1)
		if event.button() == pyqt.Qt.RightButton:
			pass
		else:
			pass
			#self.setNodeFocus(event.data)
		super().mousePressEvent(event)

	def tabBarClicked(self, event):
		''' '''
		print('Tab Bar Clicked')
		super().tabBarClicked(event)

	def tabBarDoubleClicked(self, event):
		''' '''
		print('Tab Bar Double Clicked')
		super().tabBarDoubleClicked(event)

	def changeEvent(self, event):
		''' '''
		print('Change Event')

	def showEvent(self, event):
		print('Show Event')


class NchantdTab(pyqt.QWidget):
	'''A Widget integrating Application and User configurations with the
		standard NchantdTab widget'''
	def __init__(self, parent=None, cfg={}, singlepane=False):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdTab')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdTab, self).__init__()
		self.model = parent.model
		if not singlepane:
			self.tab = self.config.dikt['tab']
			self.node = self.parent.model.node
			self.item = self.node.item

	def buildPane(self):
		''' '''
		return self

	def initModel(self):
		''' '''

	def initView(self):
		''' '''
		self.buildPane()

	def initWidget(self, pos=0):
		''' '''
		self.initModel()
		self.initView()
		return self
#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
