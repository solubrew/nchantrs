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
#===============================================================================||
from fxsquirl import fxsquirl
from fxsquirl.fxsquirl import Chunker
from nchantrs.libraries import pyqt
#===============================================================================||

#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
def getLastNodeId(src, name):
	''' '''
	lnode, col = 0, 'lastnode'
	src.setReader({'view': ['vw_last_node']}, name)
	src.initExtract(col, 'set')
	src.extract('vw_last_node')
	nodel = list(src.cache.store[col])
	if nodel != [] and nodel != [None]:
		lnode = nodel[0]
	return int(lnode)

def getNodeBase(nodetype, treeid=0, tabfocus=0):
	if nodetype == 'appnode':
		base = [1, 0, 1, 0, 1, 1, 1]
	elif nodetype == 'datanode':
		base = [1, 0, 1, 0, 1, 1, 0]
	elif nodetype == 'usernode':
		base = [1, 0, 1, 0, 1, 1, 0]

	return treeid + base + tabfocus

def getTabBase(tabtype):
	''' '''
	if nodetype == 'tab':
		base = []
	return base
