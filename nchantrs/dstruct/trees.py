#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:   #																	||
	name:	#																	||
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
from os.path import abspath, dirname, join
import simplejson as j
#===============================================================================||
from condor import condor
from excalc import ts as calcts
from nchantrs.libraries import pyqt, qpandas
#===============================================================================||

#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = f'{here}_data_/trees.yaml'
class NchantdTreeGenerator():
	''' '''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.config = condor.instruct(pxcfg).select('MBAppModel')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
	def genYearMonthTreeData(self, src, pos=0, pid=0, nid=None):
		'''Generate a table of date nodes for initilization of a timeline based
			tree widget
			need to get first data from data? or hand it the date?'''
		cols = ['nid', 'name', 'ntype', 'parentid', 'position', 'tabset',
			'treeid', 'readonly', 'editable', 'visible', 'moveable',
			'pregnable', 'isparent', 'expanded', 'tabfocus']
		format = '%d/%m/%Y %H:%M:%S'
		if pid != 0 and nid == None:
			node = self.src.getNode(pid)
			nid = node.nid
		if nid == None:
			nid = 1
		nodes, tabs = [], []
		startdate = calcts.getDateObject('01/01/2022 00:00:00', format)
		enddate = calcts.getTodayObject()
		for year in range(int(enddate.year) - int(startdate.year)+5):
			year += startdate.year
			nid, nodes, tabs = self.genYearNode(tabs, nodes, nid, year, pid, pos, year)
			pos += 1
		src.wrtr({'trnodes': qpandas.DataFrame(nodes, columns=cols)})
		cols = ['name', 'widget', 'widgdata', 'parentid', 'position',
				'readonly', 'editable', 'visible', 'moveable']
		src.wrtr({'tabs': qpandas.DataFrame(tabs, columns=cols)})
	def genYearNode(self, tabs, nodes, nid, name, pid, pos, year):
		''' '''
		nbase = [0, 1, 0, 1, 0, 0, 0, 0, 0]
		tbase = [0, 1, 1, 1]
		tabset = 'NchantdSummaryOfMonthsTabSet'
		nodes.append([nid, name, 'node', pid, pos, tabset] + nbase)
		widget = 'dashboards.NchantdYearSummary'
		widget = 'editors.NchantdJournalEditor'
		data = f'This is the data {year}'
		data = j.dumps({'text': data})
		tabs.append([name, widget, data, nid, 0] + tbase)
		pid = nid
		nid += 1
		for month in range(1, 13):
			name = calcts.getMonthLabel(month)
			tabset = 'NchantdMonthOfDaysTabSet'
			nodes.append([nid, name, 'node', pid, pos, tabset] + nbase)
			tabs += self.genMonthOfDays(month, year, nid, tbase)
			pos += 1
			nid += 1
		return nid, nodes, tabs
	def genMonthOfDays(self, month, year, pid, base):
		''' '''
		widget = 'editors.NchantdJournalEditor'
		lastday = int(calcts.getLastDayofMonth(month, year))
		tabs = []
		pos = 0
		for day in range(1, lastday+1):
			#if log: print(f'Create Day {day} of Month {month} and Year {year}')
			data = f'This is the data {day}'
			data = j.dumps({'text': data})
			tabs.append([day, widget, data, pid, pos] + base)
			pos += 1
		return tabs
