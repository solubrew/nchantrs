# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name:
	description: >
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import dirname, join
from typing import Optional, Dict, List

import logging


logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), '')  # ||
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, '_data_', 'license.yaml')

class Ownership(object):
	""""""
	def __init__(self, cfg=None):
		""""""
		self.config = condor.instruct(pxcfg).select('Ownership').override(cfg)
		# [DONE] find NFT contracts
		#  the desktop settings and background can be hard coded into the
		#  software
		#  the NFT will then need to be read to get the public key for the owner
		#  standard NFTs do not have this upload capability so the NFT would need to follow a new standard
		#  or be put into an emblem vault with the capability
		#  what stops someone from sharing the key to allow others to access the NFT features

class TOS():
	""""""
	def __init__(self, cfg=None):
		""""""
		self.config = condor.instruct(pxcfg).select('TOS').override(cfg)




# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||