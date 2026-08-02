from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import dirname, join
from kahndor import kahndor
import logging
from nchantrs.libraries import pyqt
logger = logging.getLogger(__name__)
from nchantrs.widgets.widgets import NchantdWidget
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')

def render_svg_to_pixmap(svg_file_path, width, height) -> Any:
    pixmap = pyqt.QPixmap(width * 1.01, height * 1.01)
    pixmap.fill()
    svg_renderer = pyqt.QSvgRenderer(svg_file_path)
    painter = pyqt.QPainter(pixmap)
    background_color = pyqt.QColor('#5352b8')
    painter.fillRect(pixmap.rect(), background_color)
    svg_renderer.render(painter)
    painter.end()
    return pixmap

class NchantdPaletteShifter(NchantdWidget):
    """Nchantd Palette Shifter allows for editing an image by shifting each color in the image palette to a newly
    selected color, with the ability to look an offset threshold and apply to each color."""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdPaletteShifter')
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self