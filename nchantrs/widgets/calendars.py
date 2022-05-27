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
from nchantrs.widgets import tabsets
#=======================================================================||
here = join(dirname(__file__),'')#										||
there = abspath(join('../../..'))#										||set path at pheonix level
version = '0.0.0.0.0.0'#												||
log = True
#=======================================================================||
pxcfg = f'{here}_data_/calendars.yaml'
class NchantdDayCalendar(tabsets.NchantdTab):
	''' '''
	def __init__(self, parent=None, cfg={}):
		self.parent = parent
		self.src = parent.model.src
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).override(cfg)
		super(NchantdDayCalendar, self).__init__(parent, cfg)
	def buildPane(self):
		''' '''
		self.layout = pyqt.QVBoxLayout()
		self.layout.addWidget(annotations.NchantdLabel('Thursday'))
		self.layout.addWidget(annotations.NchantdLabel('1/30/2022'))
		self.editor = editors.NchantdDocEditor(self).initWidget()
		self.layout.addWidget(self.editor)
		self.setLayout(self.layout)
		return self

class NchantdMonthCalendar(tabsets.NchantdTab):
	''' '''
	def __init__(self, parent=None, cfg={}):
		self.parent = parent
		self.src = parent.model.src
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).override(cfg)
		super(NchantdMonthCalendar, self).__init__(parent, cfg)
	def buildPane(self):
		''' '''
		cnt = 0
		for week in weeks:
			self.addWidget(NchantdDayCalendar, cnt, 0)  #Monday
			self.addWidget(NchantdDayCalendar, cnt, 1)  #Tuesday
			self.addWidget(NchantdDayCalendar, cnt, 2)  #Wednesday
			self.addWidget(NchantdDayCalendar, cnt, 3)  #Thursday
			self.addWidget(NchantdDayCalendar, cnt, 4)  #Friday
			self.addWidget(NchantdDayCalendar, cnt, 5)  #Saturday
			self.addWidget(NchantdDayCalendar, cnt, 6)  #Sunday
			cnt += 1
class NchantdWeekCalendar(tabsets.NchantdTab):
	''' '''
	def __init__(self, parent=None, cfg={}):
		self.parent = parent
		self.src = parent.model.src
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).override(cfg)
		super(NchantdWeekCalendar, self).__init__(parent, cfg)
	def buildPane(self):
		''' '''
		self.layout = pyqt.QGridLayout()
		self.addWidget(NchantdDayCalendar, 0, 0)  #Monday
		self.addWidget(NchantdDayCalendar, 0, 1)  #Tuesday
		self.addWidget(NchantdDayCalendar, 1, 0)  #Wednesday
		self.addWidget(NchantdDayCalendar, 1, 1)  #Thursday
		self.addWidget(NchantdDayCalendar, 2, 0)  #Friday
		self.addWiget(NchantdDayCalendar, 2, 1)  #Saturday
		self.addWiget(NchantdDayCalendar, 3, 0, 2)  #Sunday

		return self
class NchantdYearCalendar(tabsets.NchantdTab):
	''' '''
	def __init__(self, parent=None, cfg={}):
		self.parent = parent
		self.src = parent.model.src
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).override(cfg)
		super(NchantdYearCalendar, self).__init__(parent, cfg)
	def buildPane(self):
		''' '''
		self.layout = pyqt.QGridLayout()
