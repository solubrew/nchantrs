#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Nchantrs@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid: 'a75f07e9-73f9-4622-b748-5c9cc4c88e8b'  #							||
	name: Nchantrs Application Models Python Excecution Document  #				||
	description: >  #															||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	path: <[LEXIvrs]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#================================Core Modules===================================||
from os.path import abspath, dirname, exists, join, expanduser
import inspect
#===============================================================================||
from condor import condor
from condor.thing import thingify, getName
from fxsquirl.fxsquirl import Chunker
from nchantrs.models import models
#===============================================================================||
here = join(dirname(__file__),'')#												||
log = True
#===============================================================================||
pxcfg = f'{here}_data_/applicationmodels.yaml'

class NchantdPantiesModel():
	'''Base Application Model '''
	def __init__(self, parent=None, cfg=None):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdCloakModel')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		self.name = self.parent.name.lower()
		self.listeners = {}

	def distributeEvents(self):
		''' '''
		functions = self.listeners.get(name, [])
		for func in functions:
			pyqt.QtCore.QTimer.singleShot(0, func)
		return self

	def initBridgeSetModel(self):
		'''Initialize a model for keeping track of connections with external
			services and applications'''
		#self.config.override(pxcfg).select('NchantdBridgeModel')
		if self.parent.newInstance:
			pass#self.src.createAssets(cfg['tables'])
		return self

	def initEventSetModel(self):
		'''Initialize a model for keeping tracking of given commands to allow
		for undo/redo operations as well as a replay option '''
		#self.config.override(pxcfg).select('NchantdEventModel')
		if self.parent.newInstance:
			pass#self.src.createAssets(cfg['tables'])
		return self

	def initDB(self, cfg={}):
		'''Initializing the Database for the Nchantd Cloak application sets the
			primary data source for the application to the self.src model class
			attribute.  This source is set to an instance of a Chunker class
			from the FxSQuiRL module.

			should there be other options for the primary source?


			'''
		reset = None if 'setup' not in self.config.dikt['args'] else 3659#		||
		name = self.parent.name.lower()
		path = join(abspath(expanduser('~')), f'.config/{name}/{name}.db')
		cfg = self.config.dikt['dstruct']['store']
		self.src = Chunker(path, name, cfg, reset)
		return self

	def initModel(self):
		''' '''
		self.initDB()
		self.initEventSetModel()
		self.initListenerSetModel()
		self.initBridgeSetModel()
		return self

	def initListenerSetModel(self):
		'''Initalize a model for keeping track of listeners and distributing
			events to those listeners '''
		#self.config.override(pxcfg).select('NchantdListenerModel')
		if self.parent.newInstance:
			pass#self.src.createAssets(cfg['tables'])
		return self

	def registerListener(self, widget):
		''' '''
		self.listeners[widget] = {}
		return self

	def updateListeners(self, listener, fx):
		''' '''
		if listener not in self.listeners:
			self.registerListener(listener)
		self.listeners[listener].append({'fx': fx, 'uutc': uutc})
		return self

	def updateModel(self):
		''' '''
		return self

class NchantdCapeModel(NchantdPantiesModel):
	''' '''
	def __init__(self, parent=None, cfg=None):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg)
		self.config.select('NchantdSigilModel').override(cfg)
		if parent:
			self.config.override(parent.config)
		self.listeners = {}

	def initModel(self):
		''' '''
		self.initDB()
		self.initEventSetModel()
		self.initListenerSetModel()
		self.initBridgeSetModel()
		return self

	def initBridgeSetModel(self):
		'''Initialize a model for keeping track of connections with external
			services and applications'''
		cfg = self.config.override(pxcfg).select('NchantdBridgeModel')
		if self.parent.newInstance:
			pass#self.src.createAssets(cfg['tables'])
		return self

	def initEventSetModel(self):
		'''Initialize a model for keeping tracking of given commands to allow
		for undo/redo operations as well as a replay option '''
		cfg = self.config.override(pxcfg).select('NchantdEventModel')
		if self.parent.newInstance:
			pass#self.src.createAssets(cfg['tables'])
		return self

	def initDB(self):
		''' '''
		if log: print('initDB Called by', inspect.currentframe().f_back.f_code.co_name)
		reset = None if 'setup' not in self.config.dikt['args'] else 3659#		||

		name = self.parent.name.lower()
		path = join(abspath(expanduser('~')), f'.config/{name}/{name}.db')
		cfg = self.config.dikt['dstruct']['store']['db']

		self.src = Chunker(path, name, cfg, reset)
		return self

	def initListenerSetModel(self):
		'''Initalize a model for keeping track of listeners and distributing
			events to those listeners '''
		cfg = self.config.override(pxcfg).select('NchantdListenerModel')
		if self.parent.newInstance:
			pass#self.src.createAssets(cfg['tables'])
		return self

	def distributeEvents(self):
		''' '''
		functions = self.listeners.get(name, [])
		for func in functions:
			pyqt.QtCore.QTimer.singleShot(0, func)
		return self

	def registerListener(self, widget):
		''' '''
		self.listeners[widget] = {}
		return self

	def updateListeners(self, listener, fx):
		''' '''
		if listener not in self.listeners:
			self.registerListener(listener)
		self.listeners[listener].append({'fx': fx, 'uutc': uutc})
		return self

	def updateData(self):
		''' '''
		return self

class NchantdCloakModel(NchantdPantiesModel):
	'''The Nchantd Cloak Model setups the connection to the data for a generic
		Nchantd Cloak application.  '''
	def __init__(self, parent=None, cfg=None):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdCloakModel')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		self.name = self.parent.name.lower()
		self.listeners = {}
		self.node = 'main'

	def distributeEvents(self):
		''' '''
		functions = self.listeners.get(name, [])
		for func in functions:
			pyqt.QtCore.QTimer.singleShot(0, func)
		return self

	def initBridgeSetModel(self):
		'''Initialize a model for keeping track of connections with external
			services and applications'''
		#self.config.override(pxcfg).select('NchantdBridgeModel')
		if self.parent.newInstance:
			pass#self.src.createAssets(cfg['tables'])
		return self

	def initEventSetModel(self):
		'''Initialize a model for keeping tracking of given commands to allow
		for undo/redo operations as well as a replay option '''
		#self.config.override(pxcfg).select('NchantdEventModel')
		if self.parent.newInstance:
			pass#self.src.createAssets(cfg['tables'])
		return self

	def initDB(self, cfg={}):
		'''Initializing the Database for the Nchantd Cloak application sets the
			primary data source for the application to the self.src model class
			attribute.  This source is set to an instance of a Chunker class
			from the FxSQuiRL module.

			should there be other options for the primary source?


			'''
		reset = None if 'setup' not in self.config.dikt['args'] else 3659#		||
		name = self.parent.name.lower()
		path = join(abspath(expanduser('~')), f'.config/{name}/{name}.db')
		cfg = self.config.dikt['dstruct']['store']
		self.src = Chunker(path, name, cfg, reset)
		return self

	def initModel(self):
		''' '''
		self.initDB()
		self.initEventSetModel()
		self.initListenerSetModel()
		self.initBridgeSetModel()
		return self

	def initListenerSetModel(self):
		'''Initalize a model for keeping track of listeners and distributing
			events to those listeners '''
		#self.config.override(pxcfg).select('NchantdListenerModel')
		if self.parent.newInstance:
			pass#self.src.createAssets(cfg['tables'])
		return self

	def registerListener(self, widget):
		''' '''
		self.listeners[widget] = {}
		return self

	def updateListeners(self, listener, fx):
		''' '''
		if listener not in self.listeners:
			self.registerListener(listener)
		self.listeners[listener].append({'fx': fx, 'uutc': uutc})
		return self

	def updateModel(self):
		''' '''
		return self

class NchantdBridgeSetModel():
	'''Nchantd Bridge Set Model provides a data model for managing connections with
		external services and data sources integrating outputs with application
		data'''
	def __init__(self):
		'''Add a bridge '''

	def add(self):
		''' '''
		return self

	def drop(self):
		'''Drop a bridge '''
		return self

class NchantdEventSetModel():
	'''Nchantd Event Model provides a data model for tracking and working with
		a history of actions and events relative to the application providing
		for an undo/redo system as well as a replay system'''
	def __init__(self):
		''' '''

	def addEvent(self):
		'''Add an event to the event log the event is parsed and then played
			through the application '''
		self._playEvent()
		return self

	def replayEvent(self):
		''' '''
		self.undoEvent()
		self._playEvent()
		return self

	def undoEvent(self):
		''' '''
		return self

	def _playEvent(self):
		''' '''
		return self

class NchantdListenerSetModel():
	''' '''
	def __init__(self):
		''' '''

	def addListener(self):
		''' '''
		return self

	def dropListener(self):
		''' '''
		return self

	def registerStream(self):
		''' '''
		return self

class NchantdBridgeModel():
	''' '''
	def __init__(self):
		''' '''

	def connect(self):
		''' '''
		return self

	def collect(self):
		''' '''
		return self

class NchantdEventModel():
	''' '''
	def __init__(self):
		''' '''

	def executeCMD(self):
		''' '''
		return self

	def reverseCMD(self):
		''' '''
		return self

class NchantdListenerModel():
	''' '''
	def __init__(self):
		''' '''

class NchantdSigilModel():
	''' '''
	def __init__(self, parent=None, cfg=None):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg)
		self.config.select('NchantdSigilModel').override(cfg)
		if parent:
			print('Parent', parent.config.dikt['args'])
			self.config.override(parent.config)
			print('Self', self.config.dikt['args'])
		self.listeners = {}

	def initModel(self, reset=None):
		''' '''
		self.initDB(reset)
		self.initEventSetModel()
		self.initListenerSetModel()
		self.initBridgeSetModel()
		return self

	def initBridgeSetModel(self):
		'''Initialize a model for keeping track of connections with external
			services and applications'''
		cfg = self.config.override(pxcfg).select('NchantdBridgeModel')
		if self.parent.newInstance:
			pass#self.src.createAssets(cfg['tables'])
		return self

	def initEventSetModel(self):
		'''Initialize a model for keeping tracking of given commands to allow
		for undo/redo operations as well as a replay option '''
		cfg = self.config.override(pxcfg).select('NchantdEventModel')
		if self.parent.newInstance:
			pass#self.src.createAssets(cfg['tables'])
		return self

	def initDB(self, reset=None):
		''' '''
		if log: print('initDB Called by', inspect.currentframe().f_back.f_code.co_name)
		print('Config', self.config.dikt)
		reset = None if 'setup' not in self.config.dikt['args'] else 3659#		||

		name = self.parent.name.lower()
		path = join(abspath(expanduser('~')), f'.config/{name}/{name}.db')
		cfg = self.config.dikt['dstruct']['store']['db']

		self.src = Chunker(path, name, cfg, reset)
		return self

	def initListenerSetModel(self):
		'''Initalize a model for keeping track of listeners and distributing
			events to those listeners '''
		cfg = self.config.override(pxcfg).select('NchantdListenerModel')
		if self.parent.newInstance:
			pass#self.src.createAssets(cfg['tables'])
		return self

	def distributeEvents(self):
		''' '''
		functions = self.listeners.get(name, [])
		for func in functions:
			pyqt.QtCore.QTimer.singleShot(0, func)
		return self

	def registerListener(self, widget):
		''' '''
		self.listeners[widget] = {}
		return self

	def updateListeners(self, listener, fx):
		''' '''
		if listener not in self.listeners:
			self.registerListener(listener)
		self.listeners[listener].append({'fx': fx, 'uutc': uutc})
		return self

	def updateData(self):
		''' '''
		return self

#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
