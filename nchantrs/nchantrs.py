#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Nchantrs@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:   #																	||
	name: Nchantrs Python Excecution Document  #				||
	description: >  #															||
		Nchantrs allows for the modular creation of a gui app via  #			||
		configuration files.  The main window holds a grid of widgets such  #	||
		that each application is its own singular document type saving, new,  #	||
		open etc refers to the data used to populate the widgets.  The  #		||
		default data format for nchantrs applications is yaml files with the  #	||
		ability to override with an sql storage method  #						||

		leverage PyQt5TableModels to integrate tables

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
from fxsquirl.orgnql import fonql
from nchantrs.dialogs import dialogs
from nchantrs.libraries import pyqt
from nchantrs.models.applicationmodels import NchantdCloakModel
from nchantrs.views.applicationviews import NchantdCloakView
from nchantrs.widgets import widgets, tabsets
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/nchantrs.yaml')#								||
class NchantdCloak(pyqt.QApplication):#											||
	'''The Nchantrs Cloak wraps a set of configurations, modules and data into
		a beautiful application '''#											||
	def __init__(self, name, parent=None, cfg=None):#							||
		'''Initialize the application and the database then update all sink
			data tables from the established source endpoints '''#				||
		self.parent = parent#													||
		appcfg = join(abspath(expanduser('~')), f'.config/{name}/{name}.yaml')#	||use to store persistent global configs for the user
		if not exists(appcfg):#													||
			fonql.touch(appcfg)#												||
		self.config = condor.instruct(pxcfg).override(self.config)#				||
		self.config.override(appcfg)#											||
		if self.parent:#														||
			self.config.override(parent.config)#								||
		super(pyqt.QApplication, self).__init__([])#							||
		self.main = pyqt.QMainWindow()#											||
		self.name = name
		self.newInstance = True
		self.dialogs = {}
		self.model = NchantdCloakModel(self)#									||
		self.view = NchantdCloakView(self).initView()#							||

	def initApp(self):#															||
		'''Initialize UI setting the main application layout and building
		 	landing widgets
			Load Pane based on the selection in the navigation tree '''
		self.src = self.model.src
		self.launch(self.config.dikt['sequence'], self.config.dikt['args'])#eventually this will need to be put into a seperate process
		dtop = self.config.dikt['gui']['desktop']# This builds the main window pane
		self.pane, cnt, style = {}, 0, dtop['layout']['style']
		for pos in self.config.dikt['styles'][style]['positions']:
			self.pane[pos] = widgets.loadWidget(self, dtop['layout'][pos], pos)
			self.model.registerListener(self.pane[pos])
			self.view.layout.addWidget(self.pane[pos], cnt)
			self.view.layout.setAlignment(self.pane[pos], pyqt.Qt.AlignLeft)
			cnt += 1
		self.main.showMaximized()
		self.exec_()# this is inherited from the pyqt.QApplication class
		return self

	def launch(self, seq, args):
		'''Launch dialogs and splash screens using a sequence dictionary '''
		runload = False
		for step in seq.keys():
			method = seq[step]['method']
			if log: print(f'Initialize Launch Step {step} - {method}')
			if seq[step]['active'] != 1:#provides control of the launch sequence to the yaml configuration
				if log: print(f'Step not currently active')
				continue
			if method in ('setup','initData') and 'setup' not in args:#allows for runtime override of certains aspects of the yaml configuration
				if log: print('Step not selected for setup')
				runload = True
				continue
			if log: print(f'Run Launch Step {step} - {method}')
			if seq[step]['params'] == None:
				thingify(method, self)()#executes a method on the Cloak class with no parameters
			else:
				thingify(method, self)(**seq[step]['params'])#executes a method on the Cloak class with paramters
		return self

	def setup(self):
		'''Overwrite method with application specific setup'''

	def update(self):
		'''Overwrite method with application specific update'''


#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
