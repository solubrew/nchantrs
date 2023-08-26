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
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = f'{here}_data_/editormodels.yaml'#									||assign default config
class NchantdDocEditorModel(pyqt.QAbstractItemModel):
	''' '''
	def __init__(self, parent=None):
		''' '''
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('nchantdbutton')
		self.config.override(cfg)
		super(NchantdDocEditorModel, self).__init__(parent)

	def initModel(self):
		''' '''

		return self

class NchantdEntryEditorModel(pyqt.QAbstractItemModel):
	'''connect to the parent source and allow it to say '''
	def __init__(self, parent=None):
		''' '''
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('nchantdentryeditormodel')
		self.config.override(cfg)
		super(NchantdEntryEditorModel, self).__init__(parent)

	def initModel(self):
		''' '''
		return self

	def


class NchantdJournalEditorModel(NchantdDocEditorModel):
	''' '''
	def __init__(self, parent=None):
		''' '''
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('nchantdbutton')
		self.config.override(cfg)
		super(NchantdJournalEditorModel, self).__init__(parent)


class NchantdScratchEditorModel(NchantdDocEditorModel):
	''' '''
	def __init__(self, parent=None):
		''' '''
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('nchantdbutton')
		self.config.override(cfg)
		super(NchantdScratchEditorModel, self).__init__(parent)

	def initModel(self):
		''' '''
		return self
