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
#===============================================================================||
from condor import condor, thing#												||
from nchantrs.libraries import pyqt
from nchantrs.widgets import annotations, editors, tables
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = f'{here}_data_/editormodels.yaml'#									||assign default config
class NchantdDocEditorView(pyqt.QListView):
	''' '''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('NchantdEditorView')
		self.config.override(cfg)
		super(NchantdDocEditorView, self).__init__(parent)
	def initView(self):
		''' '''
		#self.layout = pyqt.QVBoxLayout()
		#self.layout.addWidget(self)
		self.buildEditor()
		return self
	def buildEditor(self):
		''' '''
		return self
	def setTheme(self, theme):
		''' '''
		self.setMarginsForegroundColor()
		self.setMarginsBackgroundColor()
		self.SendScintilla(pyqt.QsciScintillaBase.SCI_STYLESETBACK, pyqt.QsciScintillaBase.STYLE_DEFAULT, theme.Paper.Default)
		self.SendScintilla(pyqt.QsciScintillaBase.SCI_STYLESETBACK, pyqt.QsciScintillaBase.STYLE_LINENUMBER, theme.LineMargin.BackGround)
		self.SendScintilla(pyqt.QsciScintillaBase.SCI_SETCARETFORE, theme.Cursor)
class NchantdJournalEditorView(NchantdDocEditorView):
	''' '''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('NchantdJournalEditorView')
		self.config.override(cfg)
		super(NchantdJournalEditorView, self).__init__(parent)
	def buildEditor(self):
		''' '''
		self.layout = pyqt.QVBoxLayout()
		self.layout.addWidget(annotations.NchantdLabel('Date: 01/01/2022'))
		self.editor = editors.NchantdDocEditor(self).initWidget()
		if log: print(f'Editor {self.editor.__dir__()}')
		self.layout.addWidget(self.editor)
		return self
class NchantdScratchEditorView(NchantdDocEditorView):
	''' '''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('NchantdScratchEditorView')
		self.config.override(cfg)
		super(NchantdScratchEditorView, self).__init__(parent)
