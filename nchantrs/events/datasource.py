#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid: <^(UUID)^>
	name:
	description: >
	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
from nchantrs.nchantrs import buildDialog
#===============================================================================||
def adddatasource(cfg=None):
	'''Launch a dialog for a new datasource which defaults to an sqlite database
	 	with the ability to set the name of the data source and change formats
		to 1 of the formats from list of compatible source types'''
	path = '{0}z-data/datasource'
	cfg = config.instruct(path).override(cfg).dikt
	dialog = buildDialog(cfg)
	try:
		store.stuff(path).touch()
		done = True
	except Exception as e:
		done = False
	return done
def linkdatasource():
	'''Link to a datasource which could be any kind of document or application
	that pheonix can interact with like sql databases '''
	return done
def bookmarks():
	'''Create bookmark links to attribtrary places within a datasource'''
	return done
