# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name: Nchantrs File Utilities
        description: >
                File utilities for the nchantrs application including file manipulation
                and QImage to data URI conversion.

        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from __future__ import annotations

import logging
from os.path import abspath, dirname, join
import datetime as dt
from typing import Any, Optional

# ======================================3rd Party Library Modules=====================================================||
import base64

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log: bool = True
logma: Logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


def qimage_to_data_uri(image: pyqt.QImage, fmt: str = "PNG") -> str:
    """Convert QImage to a data URI (<img src="data:image/png;base64,...">)."""
    if image.isNull():
        return ""
    buf = pyqt.QBuffer()
    buf.open(pyqt.QIODevice.WriteOnly)
    image.save(buf, fmt)
    ba: pyqt.QByteArray = buf.data()
    b64 = base64.b64encode(bytes(ba)).decode("ascii")
    mime = "image/png" if fmt.upper() == "PNG" else f"image/{fmt.lower()}"
    return f"data:{mime};base64,{b64}"


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
