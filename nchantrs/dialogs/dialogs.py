#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: <^(UUID)^>
	name:
	description: >
	expirary: <[expiration]>
	version: <[version]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#================================Core Modules===================================||
from os.path import abspath, dirname, exists, join, expanduser
#===============================================================================||
from condor import condor
from squirl.orgnql import fonql
from nchantrs.libraries import pyqt
from nchantrs.themes import themes
from nchantrs import nchantrs
from nchantrs.models import models
from nchantrs.models.applicationmodels import NchantdSigilModel
from nchantrs.widgets import widgets
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
home = expanduser('~')
log = True
#===============================================================================||
pxcfg = join(abspath(here), f'_data_/dialogs.yaml')#							||

class NchantdCape(pyqt.QApplication):
	'''Cape is the base class for single pane applications'''

	def __init__(self, name, cfg={}):
		''' '''
		appcfg = join(abspath(home), f'.config/{name}/{name}.yaml')
		if not exists(appcfg):
			fonql.touch(appcfg)
		self.config.override(pxcfg).override(cfg)
		self.config.override(appcfg)
		reset = None if 'setup' not in self.config.dikt['args'] else 3659#	||
		pyqt.QApplication.__init__(self, self.config.dikt['args'])#				||
		self.newInstance = True
		self.name = name
		self.slug = name.lower().replace(' ', '')

		self.model = NchantdSigilModel(self).initModel(reset)
		#self.model.initDB(reset)
		self.initUI(name)
		self.exec_()

	def initApp(self):
		''' '''
		#not to create a dialog model to replace this and mimic application models
		#self.src = models.initDB(self.config.dikt, reset)
		self.src = self.model.src
		return self

	def initUI(self, name):
		'''Initialize UI setting the main application layout and building
		 	landing widgets'''
		dtop = self.config.dikt['gui']['dialogs'][name]#										||
		if log: print('UI',dtop)
		self.main = NchantdSigil(name, self).setSource(self.model.src).buildDialog()
		self.main.MaxRecentFiles = 10#												||
		self.main.windowList = []#													||
		self.main.recentFileActs = []
		self.main.show()
		return self


class NchantdSigil(pyqt.QDialog):
	'''Sigil is the base class for individual dialogs used to interact with the
		user these Sigils allow the user to alter their Cloak'''
	def __init__(self, name, parent=None, cfg: dict={}):
		''' '''
		self.config = condor.instruct(pxcfg).override(cfg)#	||
		if parent:
			self.config.override(parent.config)
		super(NchantdSigil, self).__init__()
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
		if log: print('Config Position', self.dtop['layout'][position]['params'])
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


#==============================Source Materials=================================||
'''

'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
