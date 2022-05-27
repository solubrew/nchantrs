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
#===============================================================================||
there = abspath(join(''))#												||set path at pheonix level
here = join(dirname(__file__),'')#												||
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/nchantdcalendar.yaml')
class NchantdCalendarApp(NchantdCloak):
	''' '''
	def __init__(self, args=[], parent=None):
		''' '''
		ucfg = f'{there}/_data_/user.yaml'
		self.parent = parent
		self.config = condor.instruct(pxcfg).override(ucfg).addArgs(args)
		if parent:
			self.config.override(parent.config)
		if log: print('Calendar Config', self.config.dikt)
		super(NchantdCalendarApp, self).__init__('NchantdCalendar', self)#					||
		self.model.initModel()
		self.initApp()
	def setup(self):
		''' '''
		if log: print('Run Setup')
		self.initData()#need to work this into default actions for a variety of
		#common datasets like dates
		return self
	def initData(self):
		''' '''
		dtrees.NchantdTreeGenerator().genYearMonthTreeData(self.model.src)
	def update(self):
		''' '''
		return self

if __name__ == '__main__':
	NchantdCalendarApp(sys.argv)
