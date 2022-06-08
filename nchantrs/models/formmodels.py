#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid: <^(UUID)^>
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
from os.path import abspath, dirname, exists, join

from pandas import DataFrame
#===============================================================================||
from condor import condor#										||

from fxsquirl import collector

from worldbridger.source import etherscanSRC

from nchantrs import utils
from nchantrs.libraries import pyqt
from nchantrs.models.applicationmodels import NchantdCloakModel
from nchantrs.models import models, treemodels
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = f'{here}/_data_/models.yaml'

class NchantdDynamicRecordEntryFormModel():
	''' '''
	def __init__(self):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg)
		self.config.select('NchantdDynamicRecordEntryFormModel').override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdDynamicRecordEntryFormModel, self).__init__(parent)


class NchantdAPIEntryFormModel():
	''' '''
	def __init__(self):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg)
		self.config.select('NchantdAPIEntryFormModel').override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdAPIEntryFormModel, self).__init__(parent)
