#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																	||
---  #																	||
<(META)>:  #															||
	docid:   #															||
	name:	#														||
	description: >  #													||
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
from os.path import abspath, dirname, join
#===============================================================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.models.applicationmodels import NchantdCloakModel
#=======================================================================||
here = join(dirname(__file__),'')#										||
there = abspath(join('../../..'))#										||set path at pheonix level
version = '0.0.0.0.0.0'#												||
log = True
#=======================================================================||
class NchantdCalculator(NchantdCloak):
	''' '''
	def __init__(self, args):
		''' '''
		pxcfg = f'{here}z-data_/nchantdtodos.yaml'
		ucfg = f'{there}/z-data_/user.yaml'
		self.parent = parent
		if parent:
			cfg = self.parent.config
		self.config = condor.instruct(pxcfg).override(ucfg).addArgs(args)
		super(NchantdTODOs, self).__init__('NchantdTODOs', self)
		self.model = self.getAppModel()
	def setup(self):
		''''''
		self.applicationSetup()
		return self
	def applicationSetup(self):
		''' '''
		self.newApp = True
		self.instanceSetup()
		self.newApp = False
		return self
	def instanceSetup(self):
		''' '''
		self.newInstance = True
		self.model.updateData()
		self.newInstance = False
		return self
	def getAppModel(self):
		''' '''
		model = NchantdCloakModel(self)
		return model
if __name__ == '__main__':
	NchantdCalculator(sys.argv)
