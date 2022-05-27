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
from nchantrs.dialogs.dialogs import Sigil
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = f'{here}_data_/forms.yaml'
class SimpleEntryDialog(Sigil):
	''' '''
	def __init__(self, name, fields, cfg: dict={}):
		''' '''
		self.config = condor.instruct(pxcfg).select('simpleentrydialog')
		self.config.override(cfg)
		self.config.dikt['title'] = name
		super(SimpleEntryDialog, self).__init__()
	def buildDialog(self):
		''' '''
		return self
class PreferencesDialog(Sigil):
	''' '''
	def __init__(self):
		''' '''
	def buildDialog(self):
		''' '''
		return self
class SplashDialog(Sigil):
	''' '''
	def __init__(self):
		''' '''
	def buildDialog(self):
		''' '''
		return self
class NchantdNodeEditor(Sigil):
	'''General Record Editor Dialog specialized for editing a tree nodes fields
	'''
	def __init__(self):
		''' '''
class NchantdNodeEditor(Sigil):
	''' '''
	def __init__(self, name, parent=None):
		''' '''
		pxcfg = f'{here}_data_/forms.yaml'
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('NchantdNodeEditor')
		self.config.override(cfg)
