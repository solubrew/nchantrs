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
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "multipages.yaml")


class NchantdGraphicsView(pyqt.QGrpahicsView):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdGraphicsView").override(cfg))

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        # Create a QGraphicsScene
        self.scene = pyqt.QGraphicsScene()
        self.setScene(self.scene)

        for page_cfg in self.pages:
            # Create individual pages as QGraphicsItemGroup
            page = self.create_page(page_cfg["content"])
            self.scene.addItem(page)
            page.setVisible(False)
        # Page control
        self.current_page = 0  # Start with Page 1
        self.pages = [self.page1, self.page2]

        self.setWindowTitle("Press Left/Right Keys to Switch Pages")
        self.setFocus()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def create_page(self, text):
        """
        Create a single page as a QGraphicsItemGroup with a background and title text.
        """
        group = pyqt.QGraphicsItemGroup()
        # Background rect
        # rect = self.scene.addRect(0, 0, 800, 600)
        # rect.setBrush(pyqt.QColor(color))
        # group.addToGroup(rect)
        # Text
        # title = pyqt.QGraphicsTextItem(text)

        title.setPos(20, 20)
        group.addToGroup(title)
        return group

    def switch_page(self, direction):
        """
        Switch between pages.
        """
        self.current_page = (self.current_page + direction) % len(self.pages)

        # Update visibility of all pages
        for i, page in enumerate(self.pages):
            page.setVisible(i == self.current_page)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
