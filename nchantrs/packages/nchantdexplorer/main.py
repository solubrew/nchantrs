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
from pandas import DataFrame
#===============================================================================||
import crow
#===============================================================================||
from condor import condor#										||
from nchantrs import nchantrs
from nchantrs.dialogs.dialogs import Cape, Sigil
from nchantrs.libraries import pyqt
#===============================================================================||
there = abspath(join(''))#												||set path at pheonix level
here = join(dirname(__file__),'')#												||
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
class NchantdFileViewer(pyqt.QTreeView):
	def __init__(self):
		pyqt.QTreeView.__init__(self)
		model = pyqt.QFileSystemModel()
		model.setRootPath('/home/solubrew')
		self.setModel(model)
		self.doubleClicked.connect(self.test)
	def test(self, signal):
		file_path=self.model().filePath(signal)
		print(file_path)
if __name__ == '__main__':
	import sys
	app = pyqt.QApplication(sys.argv)
	w = NchantdFileViewer()
	w.show()
	sys.exit(app.exec_())
