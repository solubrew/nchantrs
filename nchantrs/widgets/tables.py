#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Nchantrs@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:   #																	||
	name: Nchantrs Widgets Tables Python Excecution Document  #	||
	description: >  #															||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#================================Core Modules===================================||
from os.path import abspath, dirname, exists, join
from sys import argv, exit
#===============================================================================||
from condor import condor, thing#												||
from nchantrs.libraries import pyqt, qpandas
from nchantrs import utils
from nchantrs.models import tablemodels
from nchantrs.views import tableviews
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
log = True
#===============================================================================||
pxcfg = join(abspath(here), f'_data_/tables.yaml')

class NchantdTable(pyqt.QTableWidget):
	''' '''

	def __init__(self, parent=None, data=[], cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdTable')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdTable, self).__init__()
		self.model = tablemodels.NchantdTableModel(self).initModel()

	def initModel(self):
		''' '''
		self.model.initModel()
		return self

	def initView(self):
		''' '''
		#self.setModel(self.model)
		#self.setFixedWidth(1000)
		self.setRowCount(30)
		coln = 20
		self.setColumnCount(coln)
		headers = [utils.calcERN(x) for x in range(1,coln+1)]
		print('Headers', headers)
		self.setHorizontalHeaderLabels(headers)
		x = 0
		data = []
		for row in data:
			y = 0
			for col in row:
				self.setItem(x,y, pyqt.QTableWidgetItem(col))
				y += 1
			x += 1
		return self

	def initWidget(self):
		''' '''
		self.initModel()
		self.initView()
		return self

class NchantdDataFrameTable(qpandas.DataTabWidget):
	''' '''

	def __init__(self):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdDataFrameTable')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdDataFrameTable, self).__init__()
		self.model = tablemodels.NchantdDataFrameModel()
		self.view = tableviews.NchantdDataFrameView()

	def initModel(self):
		''' '''
		return self

	def initView(self):
		''' '''
		return self

	def initWidget(self):
		''' '''
		return self

	def buildTable(self):
		''' '''
		return self


class NchantdTaskTable(NchantdTable):
	'''A Task table is a specifically structured table to track the status,
	and details of a task within a network of tasks and resources being used
	across various projects, operations by multiple actors '''
	def __init__(self, parent, data=[], cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdTaskTable')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdTable, self).__init__()
		self.buildPane()

	def buildPane(self):
		''' '''
		columns = ['name', 'description', 'due date', 'duration', 'dependacies',
					'dependants', 'resources']
		return self


class NchantdTableEditor():
	''' '''
	def __init__(self):
		''' '''


class NchantdSpreadsheet():
	''' '''
	def __init__(self):
		''' '''


class NchantdHeadlineTable():
	''' '''
	def __init__(self):
		''' '''


#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
