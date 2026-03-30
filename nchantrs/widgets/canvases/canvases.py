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

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidgetMixin
from ogma.logma import Logma
from nchantrs.widgets.canvases.scenes import NchantdScene

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "canvases.yaml")


class ThreeJSWidget(pyqt.QWebEngineView):
    """
    This widget renders a `pythreejs` 3D visualization inside a QWebEngineView.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Generate and load the 3D visualization
        html_content = self.generate_html()
        self.setHtml(html_content)  # Load the HTML directly into the QWebEngineView

    def generate_html(self):
        """
        Generate a pythreejs 3D scene as an HTML string.
        """
        # Create a box (cube)
        geometry = BoxGeometry(width=1, height=1, depth=1)
        material = MeshStandardMaterial(color="blue")
        cube = Mesh(geometry, material)

        # Setup the scene
        scene = Scene(children=[cube, AmbientLight(color="#aaaaaa")])

        # Create a perspective camera
        camera = PerspectiveCamera(position=[3, 3, 3])
        camera.lookAt([0, 0, 0])
        controls = OrbitControls(controlling=camera)

        # Create the renderer
        renderer = Renderer(camera=camera, scene=scene, controls=[controls], width=800, height=600)

        # Generate raw HTML representation
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>PyThreeJS Visualization</title>
        </head>
        <body>
            {renderer._repr_html_()}
        </body>
        </html>
        """


class NchantdCanvas(NchantdWidgetMixin, pyqt.QGraphicsView):
    """NchantdCanvas is a Generic Canvas Widget"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdCanvas")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.init_variables()
        self.scene = None
        self.shapes = None

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        self.context_menu = self.parent.context_menu
        # self.shapes = self.app.model.store.get_shapes()
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        cfg = {}
        self.scene = NchantdScene(self, cfg).initWidget()
        self.setScene(self.scene)

        # Set the scene rect to an arbitrary large size
        self.scene.setSceneRect(pyqt.QRectF(0, 0, 10000, 10000))

        # Add a test item to the scene
        ellipse = pyqt.QGraphicsEllipseItem(0, 0, 100, 100)
        ellipse.setPos(5000, 5000)  # Position it at the center of the scene
        self.scene.addItem(ellipse)

        # Enable dragging with the left mouse button
        self.setDragMode(pyqt.QGraphicsView.ScrollHandDrag)

        # Enable smooth transformation for better rendering quality
        # self.setRenderHint(pyqt.QGraphicsView.Antialiasing)
        self.set_size()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def add_item(self, item, position=[0, 0]):
        """"""
        # self.scene.addItem(item)
        self.scene.add_proxy_widget(item, position)


class NchantdPaintCanvas(NchantdCanvas):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdPaintCanvas")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        self.last_point = pyqt.QPoint()
        self.pen_colr = pyqt.Qt.black
        self.pen_width = 10

        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def paintEvent(self, event):
        """"""
        painter = pyqt.QPainter(self)
        painter.drawPixmap(self.rect(), self.canvas, self.rect())

    def mousePressEvent(self, event):
        """"""

    def mouseMoveEvent(self, event):
        """"""

    def clear(self):
        self.canvas.fill(pyqt.Qt.white)
        self.update()

    def select_pen_color(self):
        self.pen_color = pyqt.QColorDialog.getColor()

    def select_pen_width(self):
        i, okPressed = pyqt.QInputDialog.getInt(self, "Pen Width", "Value:", self.pen_width, 1, 50, 1)
        if okPressed:
            self.pen_width = i


class NchantdGameCanvas(NchantdCanvas):
    """NchantdGame is a Canvas Widget sandbox for running a game inside an
    Nchantd application using the PyGame game engine"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdPaintCanvas")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)

    def initModel(self):
        """"""
        return self

    def initView(self):
        """"""
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def startGame(self):
        """ """
        return self

    def pauseGame(self):
        """ """
        return self

    def exitGame(self):
        """ """
        return self

    def resetGame(self):
        """ """
        return self


class NchantdMapCanvas(NchantdCanvas):
    """ """

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdPaintCanvas")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)

    def initModel(self):
        """"""
        return self

    def initView(self):
        """"""
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdWireFrameCanvas(NchantdCanvas):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("Nchantd")
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


class NchantdSpace(NchantdCanvas):
    """An Nchantd Space is a 3D Canvas Widget"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdSpace")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self.parent, self.config)
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
