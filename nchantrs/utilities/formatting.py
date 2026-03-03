# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
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
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from nchantrs.libraries import pyqt


# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "formatting.yaml")


class NchantdFonts(object):
    """"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("NchantdFonts").override(cfg)
        self.fonts = self.apply_sequence(pyqt.QFontDatabase().families())

    def apply_sequence(self, fonts):
        """"""
        logma.info(f"fonts: {self.config.dikt.get('sequence', {})}")
        unsequenced = [x for x in fonts if x not in self.config.dikt.get("sequence", {}).values()]
        logma.info(f"unsequenced: {len(unsequenced)} {len(fonts)}")
        fonts = list(self.config.dikt.get("sequence", {}).values()) + unsequenced
        logma.info(f"fonts: {len(fonts)}")
        return fonts


def getAlignment(justify):
    """"""
    justify = justify.lower()
    if justify == "left":
        return pyqt.Qt.AlignmentFlag.AlignLeft
    elif justify == "center":
        return pyqt.Qt.AlignmentFlag.AlignCenter
    elif justify == "right":
        return pyqt.Qt.AlignmentFlag.AlignRight
    elif justify == "top":
        return pyqt.Qt.AlignmentFlag.AlignTop
    elif justify == "bottom":
        return pyqt.Qt.AlignmentFlag.AlignBottom
    elif justify == "top_left":
        return pyqt.Qt.AlignmentFlag.AlignTop | pyqt.Qt.AlignmentFlag.AlignLeft


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
