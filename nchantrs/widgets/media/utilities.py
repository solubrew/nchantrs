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
from os.path import dirname, join

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor

import logging
from nchantrs.libraries import pyqt

logger = logging.getLogger(__name__)

# from nchantrs.widgets.media.media import NchantdFileViewer
from nchantrs.widgets.widgets import NchantdWidget
from kahndor.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


def render_svg_to_pixmap(svg_file_path, width, height):
    # Create a QPixmap with the desired size
    pixmap = pyqt.QPixmap(width * 1.01, height * 1.01)
    pixmap.fill()  # Clear the pixmap
    # Create an SVG Renderer
    svg_renderer = pyqt.QSvgRenderer(svg_file_path)
    # Paint the SVG into the QPixmap
    painter = pyqt.QPainter(pixmap)
    background_color = pyqt.QColor("#5352b8")  # Hexadecimal color code for orange
    painter.fillRect(pixmap.rect(), background_color)
    svg_renderer.render(painter)
    painter.end()
    return pixmap


class NchantdPaletteShifter(NchantdWidget):
    """Nchantd Palette Shifter allows for editing an image by shifting each color in the image palette to a newly
    selected color, with the ability to look an offset threshold and apply to each color."""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdPaletteShifter")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
