from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'multipages.yaml')

class NchantdGraphicsView(pyqt.QGrpahicsView):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdGraphicsView').override(cfg))
        logma.info(f'NchantdGraphicsView initialized')

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.scene = pyqt.QGraphicsScene()
        self.setScene(self.scene)
        for page_cfg in self.pages:
            page = self.create_page(page_cfg['content'])
            self.scene.addItem(page)
            page.setVisible(False)
        self.current_page = 0
        self.pages = [self.page1, self.page2]
        self.setWindowTitle('Press Left/Right Keys to Switch Pages')
        self.setFocus()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def create_page(self, text) -> Any:
        """
        Create a single page as a QGraphicsItemGroup with a background and title text.
        """
        group = pyqt.QGraphicsItemGroup()
        title.setPos(20, 20)
        group.addToGroup(title)
        return group

    def switch_page(self, direction) -> None:
        """
        Switch between pages.
        """
        self.current_page = (self.current_page + direction) % len(self.pages)
        for i, page in enumerate(self.pages):
            page.setVisible(i == self.current_page)