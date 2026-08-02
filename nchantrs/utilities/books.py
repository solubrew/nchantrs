"""
---
<(META)>:
        docid:
        name:
        description: >
                Document-book conversion helpers. The previous pyffice-backed
                cherrytree/file import paths lived here; the pyffice
                integration moved to nchantdoffice (which is the package
                that combines nchantrs + pyffice). This module now
                contains only the nchantrs-side wiring and a clear
                NotImplementedError for the pyffice-only paths.
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""
from os.path import abspath, dirname, join
import datetime as dt
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from kahndor.logma import Logma
from squirl.orgnql import fonql
from typing import Optional, Dict, List, Any, Tuple
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'nchantrs.yaml')

def convert_cherrytree_2_nchantdbook(path, name=None, import_=False) -> None:
    """Convert a cherrytree file to a nchantd note book.

    Moved to nchantdoffice — nchantrs has no pyffice dependency.
    """
    raise NotImplementedError('convert_cherrytree_2_nchantdbook lives in nchantdoffice; nchantrs does not depend on pyffice.')

def convert_filesystem_2_nchantdbook(path, name=None, import_=False) -> None:
    """Convert a filesystem tree to a nchantd note book.

    Moved to nchantdoffice — nchantrs has no pyffice dependency.
    """
    raise NotImplementedError('convert_filesystem_2_nchantdbook lives in nchantdoffice; nchantrs does not depend on pyffice.')

def convert_excel_2_nchantdmatrix(path, name=None) -> None:
    """Convert an Excel file to a nchantd matrix.

    Moved to nchantdoffice — nchantrs has no pyffice dependency.
    """
    raise NotImplementedError('convert_excel_2_nchantdmatrix lives in nchantdoffice; nchantrs does not depend on pyffice.')

def convert_word_2_nchantdscript(path, name=None) -> None:
    """Convert a Word file to a nchantd script.

    Moved to nchantdoffice — nchantrs has no pyffice dependency.
    """
    raise NotImplementedError('convert_word_2_nchantdscript lives in nchantdoffice; nchantrs does not depend on pyffice.')