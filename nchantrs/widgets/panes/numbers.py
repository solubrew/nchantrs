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
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidget

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "numbers.yaml")
pxcfg = {}


class NchantdLineNumberBar(NchantdWidget):
    """A custom widget to display line numbers for a QTextEdit."""

    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def paintEvent(self, event):
        """Override the paint event to draw line numbers."""
        painter = pyqt.QPainter(self)
        painter.fillRect(event.rect(), pyqt.QColor(240, 240, 240))  # Light gray background

        block = self.editor.firstVisibleBlock()  # Get the first visible block
        block_number = block.blockNumber()
        top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
        bottom = top + self.editor.blockBoundingRect(block).height()

        # Iterate through all visible blocks
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(pyqt.QColor(100, 100, 100))  # Dark gray text
                painter.drawText(0, int(top), self.width(), int(bottom - top), pyqt.Qt.AlignRight, number)

            block = block.next()  # Move to the next block
            top = bottom
            bottom = top + self.editor.blockBoundingRect(block).height()
            block_number += 1

    def update_width(self):
        """Update the width of the line number bar based on the number of digits."""
        digits = len(str(self.editor.blockCount()))
        space = self.fontMetrics().horizontalAdvance("9") * digits + 10
        self.setFixedWidth(space)

    def update_area(self, rect, dy):
        """Update the line number bar when the editor's visible area changes."""
        if dy:
            self.scroll(0, dy)
        else:
            self.update(0, rect.y(), self.width(), rect.height())

        if rect.contains(self.editor.viewport().rect()):
            self.update_width()


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
