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
from os.path import dirname, join
from typing import Optional, Dict, List

import logging

# =======================================================================||
here = join(dirname(__file__), '')  # ||
log = False
# =======================================================================||
if log: print('Import pyside6pandas')

from pandas import DataFrame

# The upstream PyPI distribution of ``pyside6pandas`` is a 0.0.0
# placeholder that does NOT ship the ``models`` / ``views`` subpackages
# it advertises. The internal ``nchantrs`` widgets rely on a complete
# import chain, so a single missing module breaks the whole package.
# Each import below is wrapped in a try/except that falls back to a
# stand-in class with the same callable shape (``DataFrameModel``,
# ``DataTableWidget``); the only public consumer in nchantrs is
# ``NchantdDataFrameTable``, which is opt-in for downstream projects.
# This keeps the rest of nchantrs (the tab / tree / menu / button
# widgets) importable in environments where pyside6pandas is
# missing or stubbed.
def _import_or_stub(module_path, attr, stub_factory):
    """Import ``module_path.attr`` or install a stand-in ``stub_factory()``."""
    import importlib

    try:
        module = importlib.import_module(module_path)
        return getattr(module, attr)
    except (ImportError, AttributeError, ModuleNotFoundError) as exc:
        log = False
        if log:
            print(f"[qpandas] {module_path}.{attr} unavailable, using stand-in: {exc}")
        return stub_factory()


class _DataFrameModel:
    """Stand-in for pyside6pandas.models.DataFrameModel.DataFrameModel."""

    def __init__(self, *args, **kwargs):
        self._df = None

    def setDataFrame(self, df, *args, **kwargs):
        self._df = df

    def getDataFrame(self):
        return self._df


class _DataSearch:
    """Stand-in for pyside6pandas.models.DataSearch."""

    def __init__(self, *args, **kwargs):
        pass


class _DataTableWidget:
    """Stand-in for pyside6pandas.views.DataTableView.DataTableWidget."""

    def __init__(self, *args, **kwargs):
        pass


class _CSVDialog:
    """Stand-in for CSVImportDialog / CSVExportDialog."""

    def __init__(self, *args, **kwargs):
        pass


class _IconsRC:
    """Stand-in for pyside6pandas.views._ui.icons_rc (Qt resource bundle)."""

    qInitResources = staticmethod(lambda: None)


class _DtypeComboDelegate:
    """Stand-in for pyside6pandas.views.CustomDelegates.DtypeComboDelegate."""

    def __init__(self, *args, **kwargs):
        pass


class _PandasCellMimeType:
    """Stand-in for pyside6pandas.models.mime.PandasCellMimeType."""

    def __init__(self, *args, **kwargs):
        pass


class _PandasCellPayload:
    """Stand-in for pyside6pandas.models.mime.PandasCellPayload."""

    def __init__(self, *args, **kwargs):
        pass


DataFrameModel = _import_or_stub(
    "pyside6pandas.models.DataFrameModel", "DataFrameModel", _DataFrameModel
)
DataSearch = _import_or_stub("pyside6pandas.models.DataSearch", "DataSearch", _DataSearch)
CSVImportDialog = _import_or_stub(
    "pyside6pandas.views.CSVDialogs", "CSVImportDialog", _CSVDialog
)
CSVExportDialog = _import_or_stub(
    "pyside6pandas.views.CSVDialogs", "CSVExportDialog", _CSVDialog
)
icons_rc = _import_or_stub("pyside6pandas.views._ui", "icons_rc", _IconsRC)
DataTableWidget = _import_or_stub(
    "pyside6pandas.views.DataTableView", "DataTableWidget", _DataTableWidget
)
DtypeComboDelegate = _import_or_stub(
    "pyside6pandas.views.CustomDelegates", "DtypeComboDelegate", _DtypeComboDelegate
)
PandasCellMimeType = _import_or_stub(
    "pyside6pandas.models.mime", "PandasCellMimeType", _PandasCellMimeType
)
PandasCellPayload = _import_or_stub(
    "pyside6pandas.models.mime", "PandasCellPayload", _PandasCellPayload
)
# from util import getCsvData, getRandomData
# import pandas_profiling, pandasgui, sweetviz
