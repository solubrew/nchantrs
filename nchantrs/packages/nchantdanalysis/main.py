#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@nchantdTree - Main@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid: '7bdf0ef6-3a8c-40e6-95c0-9bbb0d40fe34' #								||
	name: Nchantd Analysis#														||
	description: >  #															||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#=================================Core Modules==================================||
import sys
from os.path import abspath, dirname, exists, join, expanduser
from pandas import DataFrame
#===============================================================================||
import crow
#===============================================================================||
from condor import condor#										||
from nchantrs import nchantrs
from nchantrs.dialogs.dialogs import Cape, Sigil
from nchantrs.libraries import pyqt
#===============================================================================||
there = abspath(join(''))#												||set path at pheonix level
here = join(dirname(__file__),'')#												||
log = True
#===============================================================================||
pxcfg = join(abspath(here), f'_data_/nchantdanalysis.yaml')

class NchantdAnalysis(Cape):
	'''A Dialog for entrying Account Addresses with detail information into a
		table'''

	def __init__(self, args):
		''' '''
		ucfg = f'{there}/_data_/user.yaml'
		self.config = condor.instruct(pxcfg).override(ucfg).addArgs(args)
		if log: print('CONFIG', self.config.dikt.keys())
		super(NchantdAnalysis, self).__init__('NchantdAnalysis')#				||

	def setup(self):
		''''''


if __name__ == '__main__':
	NchantdAnalysis(sys.argv)
