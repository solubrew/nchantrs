# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Nchantrs@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
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
'''  # ||
# -*- coding: utf-8 -*-#														||
# ================================Core Modules===================================||
from os.path import abspath, dirname, join
from typing import Optional, Dict, List, Any, Tuple

import logging

# =======================================================================||
here = join(dirname(__file__), '')  # ||
log = False
# =======================================================================||
if log: print('Import pyside6pandas')

from pandas import DataFrame

#from pyside6pandas.excepthook import excepthook
# from pyside6pandas.compat import QtCore, QtGui, Qt, Slot, Signal
from pyside6pandas.models.DataFrameModel import DataFrameModel
from pyside6pandas.models.DataSearch import DataSearch
from pyside6pandas.views.CSVDialogs import CSVImportDialog, CSVExportDialog
from pyside6pandas.views._ui import icons_rc
from pyside6pandas.views.DataTableView import DataTableWidget
from pyside6pandas.views.CustomDelegates import DtypeComboDelegate
from pyside6pandas.models.mime import PandasCellMimeType, PandasCellPayload
# from util import getCsvData, getRandomData
# import pandas_profiling, pandasgui, sweetviz
