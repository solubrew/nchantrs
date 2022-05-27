#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Nchantrs@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:   #																	||
	name: Nchantrs Python Excecution Document  #				||
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
import time
from os.path import abspath, dirname, exists, join, expanduser
from sys import argv, exit
#===============================================================================||
from condor import condor
from condor.thing import thingify, getName
from nchantrs.libraries import pyqt
from nchantrs.themes.themes import importTheme
from nchantrs.utils import lookup, search
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = False
#===============================================================================||
class NchantdCloakView():
	''' '''
	def __init__(self, parent=None):
		''' '''
		pxcfg = f'{here}_data_/applicaitonviews.yaml'
		self.parent = parent
		self.config = condor.instruct(pxcfg).override(parent.config)
	def initView(self):#															||
		'''Initialize UI setting the main application layout and building
		 	landing widgets'''
		dtop = self.config.dikt['gui']['desktop']#										||
		self.parent.main.setWindowTitle(dtop['title'])#								||
		self.parent.main.setGeometry(dtop['size']['left'], dtop['size']['top'],#		||
							dtop['size']['width'], dtop['size']['height'])#		||
		#self.parent.main.setMaximumSize(1000, 1000)
		importTheme(self.parent.main)#								||
		self.mainWDGT = pyqt.QWidget(self.parent.main)#							||
		self.layout = pyqt.QHBoxLayout(self.mainWDGT)#									||
		#self.layout = pyqt.QGridLayout(self.mainWDGT)
		self.parent.main.setCentralWidget(self.mainWDGT)#						||
		#url = f'{here}/data/img/worldofnfts.png'
		#self.parent.main.setStyleSheet(f"background-image: url({url});")
		self.parent.main.setAttribute(pyqt.Qt.WA_DeleteOnClose)#							||
		self.parent.main.setAutoFillBackground(True)#										||
		self.parent.main.MaxRecentFiles = 10#												||
		self.parent.main.windowList = []#													||
		self.parent.main.recentFileActs = []#												||
		if dtop['menubar']:
			self.initMenuBar(dtop['menubar'])
		if dtop.get('toolbars'):
			self.initToolBars(dtop['toolbars'])
		return self
	def initMenuBar(self, menubar):
		''' '''
		menu = buildMenuBar(self.parent.main, menubar)#					||
		for k, mobj in menu.items():#											||
			self.parent.main.menuBar().addMenu(mobj)#										||
		return self
	def initToolBars(self, toolbars):
		''' '''
		for toolbar in toolbars.keys():
			print('Toolbar',toolbar)
			if toolbars[toolbar]:
				self.parent.main.addToolBar(buildToolbar(self.parent, toolbars[toolbar]))#		||
		return self
	def on_click_tree_node(self):
		'''On click of a tree node the tabs for that node need to be loaded'''
		loadPane(cfg)
	def showSplashScreen(self):
		''' '''
		cfg = self.config.dikt['dialogs']['splash']
		screen = dialogs.Sigil(cfg)
		screen.show()
		time.sleep(cfg['time'])
		screen.close()
		return self
def buildAction(app, cfg):
	'''Dynamically build action to be triggered from menu item'''#				||
	if not isinstance(cfg, dict):
		cfg = lookup(cfg)
	icon = pyqt.QIcon(cfg['Icon'])
	kwargs = {}
	if 'Shortcut' in cfg.keys() and cfg['Shortcut'] != None:#					||
		kwargs['shortcut'] = cfg['Shortcut']
	if 'statusTip' in cfg.keys() and cfg['statusTip'] != None:#					||
		kwargs['statusTip'] = cfg['Tip']
	if 'Fx' in cfg.keys() and cfg['Fx'] != None:
		kwargs['triggered'] = thingify(cfg['Fx'])
	return pyqt.QAction(icon, cfg['Name'], app, **kwargs)#						||
def buildMenuBar(app, cfg=None, menu={}):#, menuBLD={}, name=None, level=0):
	'''Build menu bar from menu configuration tree'''
	for seq, code in cfg.items():#												||process build sequence
		menus = buildMenu(app, code, menu)#										||recurse menu
	return menus
def buildMenu(app, cfg, menu={}):
	'''Build menu from menu configuration tree'''
	for code, seq in cfg.items():#												||Menubar Code
		name = lookup(code)['Name']
		menu[code] = pyqt.QMenu('&{0}'.format(name), app)#							||
		for n, subcode in seq.items():
			#remove this and instead preload all application level actions
			if isinstance(subcode, dict):
				action = menu[code].addAction(list(subcode.keys())[0])
				submenus = buildMenu(app, subcode)
				for entry, submenu in submenus.items():
					action.setMenu(submenu)
			else:
				action = buildAction(app, subcode)
				menu[code].addAction(action)
	return menu
def buildToolbar(app, cfg, pxcfg={}):
	'''Build toolbar from toolbar configuration tree'''
	toolbar = pyqt.QToolBar()
	toolbar.setMovable(True)
	toolbar.setFloatable(True)
	toolbar.setOrientation(pyqt.Qt.Vertical)
	for tbar in cfg.items():
		for name, btns in tbar.items():
			for seq, code in btns.items():
				btn = pyqt.QToolButton()
				name = lookup(code)['Name']
				btn.setText(name)
				btn.setCheckable(True)
				btn.setAutoExclusive(True)
				toolbar.addWidget(btn)
	return toolbar
