#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid:
	name:
	description: >
	expirary: <[expiration]>
	Version: <[Version]>
	path: <[LEXIvrs]>panda/LEXI/
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#=======================================================================||
from os.path import abspath, join
#===============================================================================||
from condor import condor#										||
#===============================================================================||
pxcfg = abspath(join('../../..','0_Config','cfg.yaml'))#								|
cfg = condor.instruct(pxcfg).load().dikt
