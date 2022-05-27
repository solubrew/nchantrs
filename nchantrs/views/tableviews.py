#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Nchantrs@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:   #																	||
	name: Nchantrs Widgets Tables Python Excecution Document  #	||
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
#================================Core Modules===================================||
from os.path import abspath, dirname, exists, join
from sys import argv, exit
#===============================================================================||
from condor import condor
from nchantrs.libraries import pyqt
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
#===============================================================================||
pxcfg = f'{here}/_data_/tableviews.yaml'
class NchantdTableView(pyqt.QListView):
	def __init__(self, parent=None):
		''' '''
		self.parent = parent
		if parent:
			cfg = self.parent.config
		self.config = condor.instruct(pxcfg).select('NchantdTableView')
		self.config.override(cfg)
		super(NchantdTableView, self).__init__()
	def initView(self):
		''' '''
		self.setModel(self.parent.model)
		self.setFixedWidth(1000)
		self.setRowCount(30)
		coln = 25
		self.setColumnCount(coln)
		headers = [calcERN(x) for x in range(1,coln+1)]
		print('Headers', headers)
		self.setHorizontalHeaderLabels(headers)
		x = 0
		for row in data:
			y = 0
			for col in row:
				self.setItem(x,y, pyqt.QTableWidgetItem(col))
				y += 1
			x += 1
		return widget
