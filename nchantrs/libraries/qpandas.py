#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Nchantrs@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:   #																	||
	name: Px Organisms Nchantrs Library QPandas Python Importation Document  #	||
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
#=======================================================================||
here = join(dirname(__file__),'')#										||
there = abspath(join('../../..'))#										||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = False
#=======================================================================||
if log: print('Import PyQt5Pandas')

from pandas import DataFrame

from pyqt5pandas.excepthook import excepthook
#from pyqt5pandas.compat import QtCore, QtGui, Qt, Slot, Signal
from pyqt5pandas.models.DataFrameModel import DataFrameModel
from pyqt5pandas.models.DataSearch import DataSearch
from pyqt5pandas.views.CSVDialogs import CSVImportDialog, CSVExportDialog
from pyqt5pandas.views._ui import icons_rc
from pyqt5pandas.views.DataTableView import DataTableWidget
from pyqt5pandas.views.CustomDelegates import DtypeComboDelegate
from pyqt5pandas.models.mime import PandasCellMimeType, PandasCellPayload
#from util import getCsvData, getRandomData
import pandas_profiling, pandasgui, sweetviz
