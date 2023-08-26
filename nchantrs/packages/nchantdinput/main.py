#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@nchantdTree - Main@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid: '202520ac-28ad-4b1f-ac39-103a98d765b2'  #							||
	name: Nchantd Input#													||
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
from nchantrs.dialogs.dialogs import NchantdCape, NchantdSigil
from nchantrs.libraries import pyqt
#===============================================================================||
there = abspath(join(''))#												||set path at pheonix level
here = join(dirname(__file__),'')#												||
log = True
#===============================================================================||
pxcfg = join(abspath(there), '_data_', 'nchantdinput.yaml')

class NchantdInput(NchantdCape):
	'''A Dialog for entrying Account Addresses with detail information into a
		table'''

	def __init__(self, args):
		# '''Create new database eventually have checks in place so as not to
		# 	delete user db also have a way of backing up any nonblockchain data
		# 	so it can be selectively reimported to a new database if needed'''
		ucfg = f'{there}/_data_/user.yaml'
		self.config = condor.instruct(pxcfg).override(ucfg).addArgs(args)
		if log: print('CONFIG', self.config.dikt.keys())
		super(NchantdInput, self).__init__('NchantdInput')#					||
		self.initApp()

	# def setup(self):
	# 	''''''
	# 	self.dialogAddAccounts()
	# 	return self
	#
	# def dialogAddAccounts(self, params=None):
	# 	'''Build dialog to make the appropriate number of account entries
	# 		available to the user based on NFT held by main account'''
	# 	return self


if __name__ == '__main__':
	NchantdInput(sys.argv)
