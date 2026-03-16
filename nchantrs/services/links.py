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
from os.path import abspath, dirname, join
import datetime as dt
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import pyqt
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), '')  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, '_data_', '.yaml')

class LinkService:
	"""
		This will be used to move link data this is specific to affiliates, operations and advertisements from the
		Nchantrs service to the Nchantd Applications
	"""
	def __init__(self, parent, cfg: dict = None) -> None:
		""""""
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('').override(cfg)
		self.app = pyqt.QApplication.instance()

	def get_links(self) -> None:
		"""
		need to send a request to a service and then parse the response

		:return:
		"""




	def store_link(self, name: str, path: str, tags: str) -> None:
		""""""
		location = 'remote'
		encoding = 'html'
		policy_FK = 1
		tags = "{'link': {" + tags + "}}"
		self.app.model.store_media('WEB', name, path, location, encoding, tags, policy_FK)

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
