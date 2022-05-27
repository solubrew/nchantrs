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

from datetime import timedelta
#===============================================================================||
import crow
#===============================================================================||
from condor import condor#										||
from nchantrs.dstruct import trees as dtrees
from nchantrs.nchantrs import NchantdCloak
from nchantrs.libraries import pyqt
from nchantdmoonbags import widgets
#===============================================================================||
there = abspath(join(''))#												||set path at pheonix level
here = join(dirname(__file__),'')#												||
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = join(abspath(there), '_data_/nchantdpane.yaml')
class NchantdPane(NchantdCloak):
	''' '''
	def __init__(self, args=[], parent=None):
		''' '''
		ucfg = f'{there}/_data_/user.yaml'
		self.parent = parent
		self.config = condor.instruct(pxcfg).override(ucfg).addArgs(args)
		if parent:
			self.config.override(parent.config)
		super(NchantdPane, self).__init__('NchantdPane', self)#					||
		self.model.initModel()
		self.initApp()


if __name__ == '__main__':
	NchantdPane(sys.argv)


#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
