"""
---
<(META)>:
        docid:
        name:
        description: >
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""
from os.path import abspath, dirname, join
import datetime as dt
import logging
logger = logging.getLogger(__name__)
import os
import sys
from kahndor import kahndor
from typing import Optional, Dict, List, Any, Tuple
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')

def _configure_qt_environment() -> None:
    """Configure Qt environment for better compatibility"""
    chromium_flags = ['--disable-gpu', '--disable-software-rasterizer', '--disable-gpu-sandbox', '--no-sandbox', '--disable-dev-shm-usage']
    os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = ' '.join(chromium_flags)
    os.environ['QT_QUICK_BACKEND'] = 'software'
    os.environ['QT_OPENGL'] = 'software'
    if 'QT_QPA_PLATFORM' not in os.environ:
        if sys.platform.startswith('linux'):
            os.environ['QT_QPA_PLATFORM'] = 'xcb'