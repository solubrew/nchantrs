# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Aberration Test App
	description: >
		Example of aberration (L1) entry point - single widget dialog
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
import os
import sys

# Set Qt platform before importing PySide6
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

from os.path import dirname, join

# Add nchantrs to path
here = join(dirname(__file__), "")
sys.path.insert(0, here)

from nchantrs.nchantrs import aberration  # noqa: E402


class TestLabelWidget:
    """Simple test widget for aberration"""

    def __init__(self, parent=None):
        self.parent = parent
        self.widget = None

    def initWidget(self):
        """Initialize the widget"""
        from nchantrs.libraries import pyqt
        self.widget = pyqt.QLabel("Aberration Test - L1 Entry Point")
        self.widget.setStyleSheet("font-size: 24px; padding: 20px;")
        return self.widget


if __name__ == "__main__":
    print("="*60)
    print("Testing Aberration (L1 Entry Point)")
    print("="*60)

    # Create widget class for aberration
    widget = TestLabelWidget

    # Call aberration entry point
    aberration(
        name="Test Aberration",
        args=sys.argv,
        widget=widget,
        cfg={"title": "Aberration Test"}
    )

    print("Aberration complete")
