#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																	||
---  #																	||
<(META)>:  #															||
	docid:   #															||
	name:	#														||
	description: >  #													||
		Nchantd Time is a packaged to provide time tracking leveraging
		the calendar and fund packages
	expirary: <[expiration]>  #											||
	version: <[version]>  #												||
	path: <[LEXIvrs]>  #												||
	outline: <[outline]>  #												||
	authority: document|this  #											||
	security: sec|lvl2  #												||
	<(WT)>: -32  #														||
''' #																	||
# -*- coding: utf-8 -*-#														||
#===============================Core Modules====================================||
import sys
from os.path import abspath, dirname, join
#===============================================================================||
import crow

from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.nchantrs import NchantdCloak
from nchantrs.models import applicationmodels, treemodels
#=======================================================================||
here = join(dirname(__file__),'')#										||
there = abspath(join('../../..'))#										||set path at pheonix level
version = '0.0.0.0.0.0'#												||
log = True
#=======================================================================||
