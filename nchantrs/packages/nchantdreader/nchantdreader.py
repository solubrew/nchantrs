#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@nchantdTree - Main@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid: '202520ac-28ad-4b1f-ac39-103a98d765b2'  #							||
	name: Nchantd Reader#													||
	description: >  #															||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
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
log = True
#===============================================================================||
pxcfg = f'{there}/_data_/nchantdreader.yaml'

class NchantdReader(Cape):
	'''A Dialog for entrying Account Addresses with detail information into a
		table'''

	def __init__(self, args):
		# '''Create new database eventually have checks in place so as not to
		# 	delete user db also have a way of backing up any nonblockchain data
		# 	so it can be selectively reimported to a new database if needed'''
		ucfg = f'{there}/_data_/user.yaml'
		self.config = condor.instruct(pxcfg).override(ucfg).addArgs(args)
		if log: print('CONFIG', self.config.dikt.keys())
		super(NchantdAccountEntry, self).__init__('NchantdAccountEntry')#					||

	def setup(self):
		''''''
		self.dialogAddAccounts()
		return self

	def dialogAddAccounts(self, params=None):
		'''Build dialog to make the appropriate number of account entries
			available to the user based on NFT held by main account'''
		return self


class NMBNEWSLSummaryTab(NMBTab):
	''' '''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NMBNEWSLSummaryTab')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NMBNEWSLSummaryTab, self).__init__(parent, self.config)
	def buildPane(self):
		''' '''
		layout = pyqt.QVBoxLayout()
		sections = [['Daily Updates',]]
		feeds = ['http://rss.cnn.com/rss/cnn_topstories.rss',
					'http://rssfeeds.usatoday.com/UsatodaycomNation-TopStories',
					'https://archive.nytimes.com/www.nytimes.com/services/xml/rss/index.html',
					'http://www.nbcnews.com/id/6257883/t/press-release/',
					'https://www.washingtontimes.com/feeds/',
					'https://www.huffingtonpost.in/news/rss/',
					'https://www.abc.net.au/news/rural/rss/',
					'https://www.theage.com.au/rssheadlines',
					'https://www.heraldsun.com.au/help-rss',
					'https://www.yahoo.com/news/rss',
					'https://www.yahoo.com/news/rss/us',
					'https://finance.yahoo.com/news/rssindex',
					'https://news.bitcoin.com/feed/'
				]
		cnt = 0
		for section in sections:
			gb = pyqt.QGroupBox(section[0])
			scroll = pyqt.QScrollArea()
#			scroll.setFixedHeight(500)
			scroll.setWidget(gb)
			scroll.setWidgetResizable(True)
			gblo = pyqt.QVBoxLayout()
			for feed in feeds:
				feeddata = feedparser.parse(feed)
				if log: print('Feeds', feeddata['feed'].keys())
				if 'title' in feeddata['feed'].keys():
					title = anns.NchantdLabel(feeddata['feed']['title'])
				elif 'summary' in feeddata['feed'].keys():
					continue
					#title = anns.NchantdLabel(feeddata['feed']['summary'])
				else:
					continue
					if log: print('Feed Keys', feeddata['feed'].keys())
				feedlo = pyqt.QVBoxLayout()
				feedlo.addWidget(title)
				gblo.addLayout(feedlo)
			gb.setLayout(gblo)
			layout.addWidget(scroll, cnt)
			cnt += 1
		self.setLayout(layout)
		return self



if __name__ == '__main__':
	NchantdAccountEntry(sys.argv)
