#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@nchantdTree - Main@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:    #								||
	name: Nchantd Moon Bags#													||
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
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = f'{there}/_data_/nchantdaccountentry.yaml'
class NchantdAccountEntry(Cape):
	'''A Dialog for entrying Account Addresses with detail information into a
		table'''
	def __init__(self, args):
		# '''Create new database eventually have checks in place so as not to
		# 	delete user db also have a way of backing up any nonblockchain data
		# 	so it can be selectively reimported to a new database if needed'''
		ucfg = f'{there}/_data_/user.yaml'
		self.config = condor.instruct(pxcfg).override(ucfg).addArgs(args)
		if log: print('CONFIG', self.config.dikt.keys())
		super(NchantdAccountEntry, self).__init__('NchantdAccountEntry')#					||
	def setup(self):
		''''''
		self.dialogAddAccounts()
		return self
	def dialogAddAccounts(self, params=None):
		'''Build dialog to make the appropriate number of account entries
			available to the user based on NFT held by main account'''

		return self
if __name__ == '__main__':
	NchantdAccountEntry(sys.argv)
