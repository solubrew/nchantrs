# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
    docid:
    name: Nchantrs Formatting Utilities
    description: >
        Font and alignment utilities for the nchantrs application.
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
from typing import Any, Optional

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma: Logma = Logma(__name__)


# ====================================================================================================================||
pxcfg = join(here, "_data_", "formatting.yaml")


class NchantdFonts:
    """Font management class for nchantrs."""

    def __init__(self, cfg: Optional[dict[str, Any]] = None) -> None:
        """Initialize the fonts with optional configuration."""
        self.config = kahndor.Instruct(pxcfg).select("NchantdFonts").override(cfg)
        self.fonts = self.apply_sequence(pyqt.QFontDatabase().families())

    def apply_sequence(self, fonts: list[str]) -> list[str]:
        """Apply font sequence ordering."""
        logma.info(f"fonts: {self.config.dikt.get('sequence', {})}")
        unsequenced = [x for x in fonts if x not in self.config.dikt.get("sequence", {}).values()]
        logma.info(f"unsequenced: {len(unsequenced)} {len(fonts)}")
        fonts = list(self.config.dikt.get("sequence", {}).values()) + unsequenced
        logma.info(f"fonts: {len(fonts)}")
        return fonts


def getAlignment(justify: str) -> int:
    """Get Qt alignment flag from justification string.

    Args:
        justify: The justification type ('left', 'center', 'right', 'top', 'bottom', 'top_left')

    Returns:
        Qt alignment flag
    """
    # Dictionary for switch_abuse replacement
    ALIGNMENT_MAP = {
        "left": pyqt.Qt.AlignmentFlag.AlignLeft,
        "center": pyqt.Qt.AlignmentFlag.AlignCenter,
        "right": pyqt.Qt.AlignmentFlag.AlignRight,
        "top": pyqt.Qt.AlignmentFlag.AlignTop,
        "bottom": pyqt.Qt.AlignmentFlag.AlignBottom,
        "top_left": pyqt.Qt.AlignmentFlag.AlignTop | pyqt.Qt.AlignmentFlag.AlignLeft,
    }
    return ALIGNMENT_MAP.get(justify.lower(), pyqt.Qt.AlignmentFlag.AlignLeft)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
