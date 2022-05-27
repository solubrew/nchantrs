#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	DOCid:   #																	||
	name:   #																	||
	description: >  #															||
		  #			||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	path: <[LEXIvrs]>  #														||
	outline: <[outline]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#===============================Core Modules====================================||
from os.path import abspath, dirname, exists, join
#===============================================================================||
from condor import condor
from condor.thing import thingify
from nchantrs.libraries import pyqt
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/widgets.yaml')

def buildPane(parent, cfg, offsetcol=0):
	''' '''
	widgets.expandCFG(cfg)
	for row in cfg['seq'].keys():
		for col, wdgt in cfg['seq'][row].items():
			key = list(wdgt.keys())[0]
			cfg['widget'] = widgets.lookupWidget(key)
			widget = loadWidget(parent, cfg)
			parent.layout.addWidget(widget, int(row), int(col) + offsetcol)

def expandCFG(cfg):
	'''Expand Configuration Details to all child wigets within config '''
	dcfg = condor.instruct(pxcfg).select('expandCFG').override(cfg).dikt
	fonts, styles = dcfg['fonts'], dcfg['styles']
	for row in dcfg['seq'].keys():
		for col, wCFG in dcfg['seq'][row].items():
			widget = list(wCFG.keys())[0]
			cfg['seq'][row][col][widget] = expandFonts(wCFG[widget], fonts)
			cfg['seq'][row][col][widget] = expandStyles(wCFG[widget], styles)
	return cfg

def expandFonts(cfg, fonts):
	''' '''
	if 'font' in cfg:
		font = cfg['font']
	else:
		font = 'default'
	cfg['font'] = fonts[font]
	return cfg

def expandStyles(cfg, styles):
	''' '''
	if 'style' in cfg.keys():
		style = cfg['style']
	else:
		style = 'default'
	cfg['style'] = styles[style]
	return cfg

def loadWidget(parent, cfg={}, pos=None):
	'''Load the defined widget from its parameters or from a list of registered
		widgets
		Load Source for Daynamically building the tabset for the pane'''
	pxconfig = condor.instruct(pxcfg).load()
	#*************<(HACK)>**********Work around for calcgen.tree merge error
	ecfg = pxconfig.override(cfg).dikt
	ecfg['widget'] = cfg['widget']
	cfg = ecfg
	#*************END
	if 'widget' in cfg.keys():
		if cfg['widget']:
			if log: print('Widget', cfg['widget'])
			widget = thingify(cfg['widget'])(parent, cfg)
			if pos:
				widget.initWidget(pos)
			else:
				widget.initWidget()
		else:
			widget = pyqt.QWidget(parent)
	else:
		registesterd_widget = lookupWidget(list(cfg.keys())[0])
		widget = thingify(registered_widget)(parent, cfg)
		widget.initWidget(parent.newInstance)
	return widget

def lookupWidget_a000(code):
	'''Lookup up widget code in registered widgets dictionary returning the
		widget string for thingification and the sequence for identification'''
	widgets = pxcfg.dikt['RegisteredWidgets']
	code = calct.stuff(code).trimPast(':.', 'exclude')
	widgetcode =  f'{code.it})>'
	widgetseq = code.that
	if wigetcode in widgets.keys():
		return widgets[wigetcode], widgetseq
	return 'pyqt.QWidget', widgetseq

def lookupWidget(key):
	''' '''
	return condor.instruct(pxcfg).select('RegisteredWidgets').dikt[key]
