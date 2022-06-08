#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:   #																	||
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
import json as j
#===============================================================================||
from condor import condor, thing#												||
from nchantrs.libraries import pyqt
from nchantrs.models import editormodels
from nchantrs.logr import editor
from nchantrs.views import editorviews
from nchantrs.widgets import controls
from nchantrs.widgets import annotations, editors, tables
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/editors.yaml')#									||assign default config

class NchantdDocEditor(pyqt.QTextEdit):#(pyqt.QsciScintillaBase):

	def __init__(self, parent=None, cfg={}):
		'''Document editor widget built on top of QsciScintilla widget
			I believe this requires PyQt5, not sure what is available as a
			substitute for PySide2'''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdDocEditor')
		self.config.override(cfg)
		if parent:
			if log: print('Parent', parent.config.dikt)
			self.config.override(parent.config)
		super(NchantdDocEditor, self).__init__()

	def initModel(self):
		''' '''
		if log: print('CONFIG', self.config.dikt)
		self.name = self.config.dikt['tab']['name']
		self.data = j.loads(self.config.dikt['tab']['widgdata'])
		self.setText(self.data.get('text'))
		return self

	def initWidget(self):
		''' '''
		self.initModel()
		return self

	def onEnterEvent(self):
		'''Run a save of the doc editor data to the database '''

	def mousePressEvent(self, event):
		''' '''
		editor.mousePressEventLog(event)
		super().mousePressEvent(event)
		return self

class NchantdCodeEditor(NchantdDocEditor):
	''' '''
	def __init__(self, parent=None):
		''' '''
		super(NchantdDocEditor, self).__init__(app, cfg, parent)
	def setLinter(self, language='python'):
		'''Turn on linter for current code editor '''
		return self
	def setWDir(self):
		'''Set working directory for import/export of files from editor
			widget'''
		return self

class NchantdEntryEditor(pyqt.QWidget):
	''' '''

	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdEntryEditor')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdEntryEditor, self).__init__(parent)

	def initModel(self):
		''' '''
		self.buildEditor()
		return self

	def initWidget(self):
		''' '''
		self.layout = pyqt.QVBoxLayout()
		self.initModel()
		return self

	def buildEditor(self):
		''' '''
		if log: print('Nchantd Entry Editor', self.config.dikt.keys())
		self.createLabel(self.config.dikt['label'])
		self.layout.addWidget(self.label)
		self.createTextBox(self.config.dikt['default'])
		self.layout.addWidget(self.textbox)
		self.setLayout(self.layout)
		return self

	def createLabel(self, name):
		''' '''
		self.label = annotations.NchantdLabel(name)
		return self

	def createTextBox(self, value):
		''' '''
		self.textbox = annotations.NchantdEntryBox(self)
		return self


class NchantdJournalEditor(pyqt.QWidget):
	''' '''

	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdJournalEditor')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdJournalEditor, self).__init__()
		self.model = editormodels.NchantdJournalEditorModel(self)
		#self.view = editorviews.NchantdJournalEditorView(self)

	def initModel(self):
		''' '''
		if log: print('CONFIG', self.config.dikt)
		self.name = self.config.dikt['tab']['name']
		self.model.initModel()
		return self

#	def initView(self):
#		''' '''
#		self.view.initView()
#		self.setLayout(self.view.layout)
#		return self

	def initWidget(self):
		''' '''
		self.initModel()
		self.buildEditor()
#		self.initView()
		return self

	def buildEditor(self):
		''' '''
		self.layout = pyqt.QVBoxLayout()
		self.layout.addWidget(annotations.NchantdLabel('Date: 01/01/2022'))
		self.editor = editors.NchantdDocEditor(self).initWidget()
		if log: print(f'Editor {self.editor.__dir__()}')
		self.layout.addWidget(self.editor)
		self.setLayout(self.layout)
		return self


class NchantdScratchEditor(pyqt.QWidget):
	'''Continous text editor that autosaves and restores has a clear button and
	 	a save tab which allows you to save a seperate document or as a tab'''

	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		if parent:
			cfg = self.parent.config
		self.config = condor.instruct(pxcfg).select('NchantdScratchEditor')
		self.config.override(cfg)
		super(NchantdScratchEditor, self).__init__(parent)
		self.model = editormodels.NchantdScratchEditorModel(self)
		self.view = editorviews.NchantdScratchEditorView(self)

	def initModel(self):
		''' '''
		self.model.initModel()
		return self

	def initView(self):
		''' '''
		mainLayout = pyqt.QGridLayout()
		self.createExportButton()
		mainLayout.addWidget(self.btn_export, 1, 1)
		self.createMakeTabButton()
		mainLayout.addWidget(self.btn_maketab, 1, 2)
		self.createEditor()
		mainLayout.addWidget(self.editor, 2, 1, 1, 2)
		self.setLayout(mainLayout)
		return self

	def initWidget(self):
		''' '''
		self.initModel()
		self.initView()
		return self

	def createEditor(self):
		''' '''
		self.editor = pyqt.QTextEdit(self)
		self.editor.setHorizontalScrollBarPolicy(pyqt.Qt.ScrollBarAlwaysOff)
		return self

	def createExportButton(self):
		''' '''
		self.btn_export = controls.NchantdButton(self, {'name': 'Export'})
		return self

	def createMakeTabButton(self):
		''' '''
		self.btn_maketab = controls.NchantdButton(self, {'name': 'Clear'})
		return self

	def clear(self):
		''' '''

	def export(self):
		''' '''

	def setTheme(self):
		''' '''
