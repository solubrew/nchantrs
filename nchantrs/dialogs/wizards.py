#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>: '' #								||
	docid:   #																	||
	name: Nchantrs Module Dialogs Wizards Python Excecution Document  #			||
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
from nchantrs.libraries import pyqt
from nchantrs.models.tablemodels import NchantdTableModel
from nchantrs.widgets.controls import NchantdSubmissionButtons
from nchantrs.widgets.editors import NchantdEntryEditor
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
log = True
#===============================================================================||
pxcfg = join(abspath(here), '_data_/forms.yaml')#								||assign default config

class NchantdWizard(pyqt.QWidget):#ithink there is a wizard widget already see if i can pull it in
	'''A multipage dialog for setting up applications by providing the user a
		set of preference options in an ever narrowing order so that the
		application can be bootstrapped into place '''

	def __init__(self):
		''' '''

	def initWidget(self):
		''' '''
