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
from nchantrs.libraries import pyqt
from nchantrs.views.paneviews import NchantdImageView
from nchantrs.widgets import widgets
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
#===============================================================================||
class NchantdImagePane(pyqt.QWidget):
	''' '''
	def __init__(self, app, cfg, parent=None):
		'''' '''
		super(NchantdImagePane, self).__init__(parent)
		pxcfg = f'{here}_data_/widgets.yaml'
		self.config = condor.instruct(pxcfg).select('paneviews').override(cfg)
		self.app = app
		self.view = NchantdImageView(app, cfg, parent)
		self.layout = pyqt.QVBoxLayout()
		self.layout.addWidget(self.view)
		self.setLayout(self.layout)
	def initModel(self):
		''' '''
		return self
	def initView(self):
		''' '''
		return self
	def initWidget(self):
		''' '''
		return self
class NchantdVideoPane(pyqt.QWidget):
	''' '''
	def __init__(self, app, cfg, parent=None):
		'''' '''
		super(NchantdImagePane, self).__init__(parent)
		pxcfg = f'{here}_data_/widgets.yaml'
		self.config = condor.instruct(pxcfg).select('paneviews').override(cfg)
		self.app = app
		self.view = NchantdImageView(app, cfg, parent)
		self.layout = pyqt.QVBoxLayout()
		self.layout.addWidget(self.view)
		self.setLayout(self.layout)
	def initModel(self):
		''' '''
		return self
	def initView(self):
		''' '''
		return self
	def initWidget(self):
		''' '''
		return self
class NchantdPDFPane(pyqt.QWidget):
	''' '''
	def __init__(self, app, cfg, parent=None):
		'''' '''
		super(NchantdImagePane, self).__init__(parent)
		pxcfg = f'{here}_data_/widgets.yaml'
		self.config = condor.instruct(pxcfg).select('paneviews').override(cfg)
		self.app = app
		self.view = NchantdImageView(app, cfg, parent)
		self.layout = pyqt.QVBoxLayout()
		self.layout.addWidget(self.view)
		self.setLayout(self.layout)
	def initModel(self):
		''' '''
		return self
	def initView(self):
		''' '''
		return self
	def initWidget(self):
		''' '''
		return self
class NchantdRSSPane(pyqt.QWidget):
	''' '''
	def __init__(self, app, cfg, parent=None):
		'''' '''
		super(NchantdImagePane, self).__init__(parent)
		pxcfg = f'{here}_data_/widgets.yaml'
		self.config = condor.instruct(pxcfg).select('paneviews').override(cfg)
		self.app = app
		self.view = NchantdImageView(app, cfg, parent)
		self.layout = pyqt.QVBoxLayout()
		self.layout.addWidget(self.view)
		self.setLayout(self.layout)
	def initModel(self):
		''' '''
		return self
	def initView(self):
		''' '''
		return self
	def initWidget(self):
		''' '''
		return self
