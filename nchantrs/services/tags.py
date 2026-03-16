# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name:
	description: >
		Create a system that manages and creates tags that will be used for various organization within the Nchantrs
		Application System
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import qpandas
from ogma.logma import Logma
from subtrix import thing

# ====================================================================================================================||
here = join(dirname(__file__), '')  # ||
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, '_data_', 'tags.yaml')

class TagGroup():
	""""""
	def __init__(self, name: str, description: str = '', uuid: str = None) -> None:
		""""""
		self.name = name
		self.description = description
		self.uuid = uuid
		if self.uuid is None:
			self.uuid = thing.What().uuid().ruuid
		self.tags = {}

class Tag():
	""""""
	def __init__(self, name: str, description: str = '', uuid: str = None) -> None:
		""""""
		self.name = name
		self.description = description
		self.uuid = uuid
		if self.uuid is None:
			self.uuid = thing.What().uuid().ruuid

	def rename(self, name: str) -> None:
		""""""

	def storage(self) -> 'qpandas.DataFrame':
		""""""
		columns = ['name', 'description', 'uuid']
		df = qpandas.DataFrame([[self.name, self.description, self.uuid]], columns=columns)
		return df

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||