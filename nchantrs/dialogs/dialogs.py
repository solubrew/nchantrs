#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: <^(UUID)^>
	name:
	description: >
	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#================================Core Modules===================================||
from os.path import abspath, dirname, exists, join, expanduser
#===============================================================================||
from condor import condor
from fxsquirl.orgnql import fonql
from nchantrs.libraries import pyqt
from nchantrs.themes import themes
from nchantrs import nchantrs
from nchantrs.models import models
from nchantrs.models.applicationmodels import NchantdSigilModel
from nchantrs.widgets import widgets
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = f'{here}_data_/dialogs.yaml'#									||
class Cape(pyqt.QApplication):
	''' '''
	def __init__(self, name, cfg={}):
		''' '''
		home = expanduser('~')
		appcfg = f'{home}/.config/{name}/{name}.yaml'
		if not exists(appcfg):
			fonql.touch(appcfg)
		self.config.override(pxcfg).override(cfg)
		self.config.override(appcfg)
		if log: print('CONFIG', self.config.dikt.keys())
		reset = None if 'setup' not in self.config.dikt['args'] else 3659#	||
		pyqt.QApplication.__init__(self, self.config.dikt['args'])#				||
		self.newInstance = True
		self.initDB(reset)
		self.name = name
		self.slug = name.lower().replace(' ', '')
		self.model = NchantdSigilModel(self).initModel()
		self.initUI(name)
		self.exec_()
	def initDB(self, reset=3659):
		''' '''
		self.src = models.initDB(self.config.dikt, reset)
		return self
	def initUI(self, name):
		'''Initialize UI setting the main application layout and building
		 	landing widgets'''
		dtop = self.config.dikt['gui']['dialogs'][name]#										||
		if log: print('UI',dtop)
		self.main = Sigil(name, self).setSource(self.src).buildDialog()
		self.main.MaxRecentFiles = 10#												||
		self.main.windowList = []#													||
		self.main.recentFileActs = []
		self.main.show()
		return self
class Sigil(pyqt.QDialog):
	'''Sigil is the base class for individual dialogs used to interact with the
		user these Sigils allow the user to alter their Cloak'''
	def __init__(self, name, parent=None, cfg: dict={}):
		''' '''
		self.config = condor.instruct(pxcfg).override(cfg)#	||
		if parent:
			self.config.override(parent.config)
		super(Sigil, self).__init__()
		self.dtop = self.config.dikt['gui']['dialogs'][name]
		self.setWindowTitle(self.dtop['title'])#										||
		self.setGeometry(self.dtop['size']['left'], self.dtop['size']['top'],#			||
							self.dtop['size']['width'], self.dtop['size']['height'])#		||
		tablenode = False
		self.pane = {}
		self.setAttribute(pyqt.Qt.WA_DeleteOnClose)#							||
		themes.importTheme(self)
		self.model = parent.model
	def buildDialog(self):
		'''Build the dialog from the provided parameters '''
		position = 'center'
		self.layout = pyqt.QVBoxLayout()
		if log: print('Config Position', self.dtop['layout'][position])
		style = self.dtop['layout']['style']
		cnt = 0
		for pos in self.config.dikt['styles'][style]['positions']:
			self.pane[pos] = widgets.loadWidget(self, self.dtop['layout'][pos])
			self.model.registerListener(self.pane[pos])
			self.layout.addWidget(self.pane[pos], cnt)
			cnt += 1

		self.setLayout(self.layout)
		return self
	def buildLayout(self, layout):
		''' '''
		if layout == 'autoform':
			pass
		return self
	def getData(self):
		if self.records == None:
			return self.defaults
		return self.records
	def setDefaults(self, defaults):
		''' '''
		self.defaults = defaults
		return self
	def setSource(self, src):
		self.src = src
		return self
def setExistingDirectory(self):
	options = pyqt.QFileDialog.DontResolveSymlinks | pyqt.QFileDialog.ShowDirsOnly
	label = 'Choose Report Directory'
	dirtext = self.Widgets['dirlabel'].text()
	directory = pyqt.QFileDialog.getExistingDirectory(self, label, dirtext, options=options)
	if directory:#													||
		self.Widgets['dirlabel'].setText(directory)#						||
	model = FileListModel()
	model.setDirPath(self.Widgets['dirlabel'].text())#					||
	self.Widgets['dirbrowser'].clear()
	self.flist = model.fileList
	for d in self.flist:
		self.Widgets['dirbrowser'].append(d)
	outpath = self.Widgets['dirlabel'].text()
	self.outputFile = outpath
