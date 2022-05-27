#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Nchantrs@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid: ''  #							||
	name: Moonbags Nchnated Python Document#								||
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
from os.path import abspath, dirname, exists, join
import simplejson as j
#===============================================================================||
from condor import condor

from nchantrs.libraries import pyqt
from nchantrs.widgets import tabsets, widgets
#===============================================================================||

#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = False
#===============================================================================||
pxcfg = f'{here}/_data_/browsers.yaml'
class NchantdJupyterBrowser():
	def __init__(self, parent=None, cfg={}, url="http://www.google.com"):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdWebBrowser')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdWebBrowser, self).__init__()
		self.setUrl(pyqt.QUrl(url))
	def initWidget(self):
		''' '''
		return self
class NchantdRSSBrowser():
	def __init__(self, parent=None, cfg={}, url="http://www.google.com"):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdWebBrowser')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdWebBrowser, self).__init__()
		self.setUrl(pyqt.QUrl(url))
	def initWidget(self):
		''' '''
		return self
class NchantdWebBrowser(pyqt.QWebEngineView):
	''' '''
	def __init__(self, parent=None, cfg={}, url="http://www.google.com"):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdWebBrowser')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdWebBrowser, self).__init__()
		#if log: print('WEB Config\n', self.config.dikt)
		widgdata = j.loads(self.config.dikt['tab']['widgdata'])
		if 'url' in widgdata.keys():
			if widgdata['url']:
				url = widgdata['url']
		self.setUrl(pyqt.QUrl(url))
	def initWidget(self):
		''' '''
		return self
class NchantdWebSourceBrowser():
	def __init__(self, parent=None, cfg={}, url="http://www.google.com"):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdWebBrowser')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdWebBrowser, self).__init__()
		if url in self.config.dikt.keys():
			url = self.config.dikt['url']
		self.setUrl(pyqt.QUrl(url))
	def initWidget(self):
		''' '''
		return self
