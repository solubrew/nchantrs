#@@@@@@@@@@@@@@@@@@@@@@@@Pheonix.Organisms.Djynn.Djynn@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(meta)>:
	docid: <^[uuid]^>
	name:
	description: >
	expirary: <[expiration]>
	version: <[version]>
	path:
	outline: <[outline]>
	authority: document|this
	security: seclvl2
	<(wt)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
from os.path import abspath, dirname, join
from sys import argv
import datetime as dt, time#					||
#===============================================================================||
from condor import condor, thing#										||
from fxsquirl import collector
#===============================================================================||
from worldbridger.web3 import web3
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
where = abspath(join(''))#														||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
def github():
	'''Use github to provide small datasets that require little change and no
		permissions or control of requested material
		specifically start by using it to provide the yearend block data
			really should get NFTd at some point
	'''
