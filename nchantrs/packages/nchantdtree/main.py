#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@nchantdTree - Main@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	DOCid:   #																	||
	name: Nchantd Tree#													||
	description: >  #															||
		Nchantd Tree is a 3pane tree based note taking application built#	||
		using the nchantrs gui framework#										||
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
from os.path import abspath, dirname, exists, join
#===============================================================================||
from PyQt5.QtWidgets import QApplication
#===============================================================================||
module_path = abspath(join('../../../../devLEXI/3_Work/1_DELTA', dirname(__file__)))
print('ModulePath', module_path)
if module_path not in sys.path:
	sys.path.insert(0, module_path)
#===============================================================================||
from pheonix.organisms.nchantrs import nchantrs
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
#===============================================================================||
def runr(cfg):
	app = QApplication(sys.argv)
	aw = nchantrs.stone()
	aw.show()
	app.exec_()
if __name__ == '__main__':
	if len(sys.argv) == 1:
		cfg = '{0}z-data_/pyffice.yaml'.format(here)
	runr(cfg)
