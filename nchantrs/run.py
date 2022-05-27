#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@nchantdTree - Main@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	DOCid: d0966a0a-f1ef-4f18-a4e9-a00b9b695d0e   #								||
	name: Nchantd Moon Bags#													||
	description: >  #															||
		Nchantd Moon Bag is a simple utility for showing a summerized view of
		various cryptocurrency accounts accross networks focusing on dollar
		averaging values from DEX trading activities using the nchantrs gui
		framework#																||
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
module_path = '/home/solubrew/Design/SB/Projects/devPheonix/3_Work/1_DELTA'
if module_path not in sys.path:
	sys.path.insert(0, module_path)
#===============================================================================||
from nchantrs import nchantrs
from nchantrs.libraries import pyqt
from setup import NchantdSetup
#===============================================================================||
there = abspath(join('../../..'))#												||set path at pheonix level
here = join(dirname(__file__),'')#												||
if there == '/':
	path = f'{here}data'
else:
	#path = f'{there}/1_DELTA/moonbags/nchantdMoonBags/data'
	path = f'/home/solubrew/Design/SB/Projects/devMoonBags/3_Work/1_DELTA/moonbags/nchantdMoonBags/data'
version = '0.0.0.0.0.0'#														||
#===============================================================================||
def runr(cfg):
	print('HERE',here, 'THERE', there)
	path = f'{path}/db/moonbags.db'#Configure Database for application
	app = pyqt.QApplication(sys.argv)
	aw = nchantrs.robe(cfg, path)
	aw.show()
	app.exec_()
if __name__ == '__main__':
	if len(sys.argv) == 1:
		cfg = f'{here}z-data_/moonbags.yaml'
	runr(cfg)
