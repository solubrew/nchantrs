# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
from typing import Any

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
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidgetMixin
from kahndor.logma import Logma
from nchantrs.widgets.canvases.scenes import NchantdScene

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "canvases.yaml")


class ThreeJSWidget(pyqt.QWebEngineView):
    """
    This widget renders a `pythreejs` 3D visualization inside a QWebEngineView.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Generate and load the 3D visualization
        html_content = self.generate_html()
        self.setHtml(html_content)  # Load the HTML directly into the QWebEngineView

    def generate_html(self) -> str:
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

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdCanvas").override(cfg)
        self.scene = None
        self.shapes = None
        self._display_pixmap = None
        logma.info(f"NchantdCanvas initialized")


    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        self.context_menu = self.parent.context_menu
        # self.shapes = self.app.model.store.get_shapes()
        return self

    def initView(self, cfg=None) -> Any:
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

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def add_item(self, item, position=[0, 0]) -> None:
        """"""
        # self.scene.addItem(item)
        self.scene.add_proxy_widget(item, position)

    def setDisplayPixmap(self, pixmap) -> None:
        """
        Set a pixmap to be displayed as an overlay on this canvas.
        This allows external code to render graphics and display them on the canvas.

        Args:
            pixmap (QPixmap): The pixmap to display on the canvas
        """
        self._display_pixmap = pixmap
        self.viewport().update()

    def getDrawingSurface(self) -> Any:
        """
        Return the actual widget that can be painted on.
        For QGraphicsView, this is the viewport.

        Returns:
            QWidget: The viewport widget that handles paint events
        """
        return self.viewport()

    def drawForeground(self, painter, rect) -> None:
        """
        Override drawForeground to draw the display pixmap over the scene.
        This is called after the scene is drawn.

        Args:
            painter (QPainter): The painter to use for drawing
            rect (QRectF): The rectangle to draw in
        """
        super().drawForeground(painter, rect)

        if self._display_pixmap and not self._display_pixmap.isNull():
            # Draw the pixmap at the top-left of the view
            painter.save()
            painter.resetTransform()
            painter.drawPixmap(0, 0, self._display_pixmap)
            painter.restore()


class NchantdPaintCanvas(NchantdCanvas):
    """A canvas widget specifically designed for direct painting/drawing operations."""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdPaintCanvas").override(cfg))
        logma.info(f"NchantdPaintCanvas initialized")


    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.last_point = pyqt.QPoint()
        self.pen_color = pyqt.Qt.black
        self.pen_width = 10

        # Initialize the canvas pixmap for painting
        self.canvas = pyqt.QPixmap(self.size())
        self.canvas.fill(pyqt.Qt.white)

        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def resizeEvent(self, event) -> None:
        """Handle resize events to maintain canvas size."""
        super().resizeEvent(event)
        if hasattr(self, "canvas"):
            # Create new pixmap with new size
            new_pixmap = pyqt.QPixmap(event.size())
            new_pixmap.fill(pyqt.Qt.white)
            # Copy old content
            painter = pyqt.QPainter(new_pixmap)
            painter.drawPixmap(0, 0, self.canvas)
            painter.end()
            self.canvas = new_pixmap

    def drawForeground(self, painter, rect) -> None:
        """Draw the paint canvas pixmap."""
        super().drawForeground(painter, rect)

        if hasattr(self, "canvas") and not self.canvas.isNull():
            painter.save()
            painter.resetTransform()
            painter.drawPixmap(0, 0, self.canvas)
            painter.restore()

    def mousePressEvent(self, event) -> None:
        """Handle mouse press for drawing."""
        if event.button() == pyqt.Qt.LeftButton:
            self.last_point = event.pos()

    def mouseMoveEvent(self, event) -> None:
        """Handle mouse move for drawing."""
        if event.buttons() & pyqt.Qt.LeftButton and hasattr(self, "canvas"):
            painter = pyqt.QPainter(self.canvas)
            painter.setPen(
                pyqt.QPen(self.pen_color, self.pen_width, pyqt.Qt.SolidLine, pyqt.Qt.RoundCap, pyqt.Qt.RoundJoin)
            )
            painter.drawLine(self.last_point, event.pos())
            painter.end()

            self.last_point = event.pos()
            self.viewport().update()

    def clear(self) -> None:
        """Clear the canvas."""
        if hasattr(self, "canvas"):
            self.canvas.fill(pyqt.Qt.white)
            self.viewport().update()

    def select_pen_color(self) -> None:
        """Open color dialog to select pen color."""
        color = pyqt.QColorDialog.getColor()
        if color.isValid():
            self.pen_color = color

    def select_pen_width(self) -> None:
        """Open dialog to select pen width."""
        i, okPressed = pyqt.QInputDialog.getInt(self, "Pen Width", "Value:", self.pen_width, 1, 50, 1)
        if okPressed:
            self.pen_width = i


class NchantdGameCanvas(NchantdCanvas):
    """NchantdGame is a Canvas Widget sandbox for running a game inside an
    Nchantd application using the PyGame game engine"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdGameCanvas").override(cfg))
        logma.info(f"NchantdGameCanvas initialized")


    def initModel(self) -> Any:
        """"""
        return self

    def initView(self) -> Any:
        """"""
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def startGame(self) -> Any:
        """ """
        return self

    def pauseGame(self) -> Any:
        """ """
        return self

    def exitGame(self) -> Any:
        """ """
        return self

    def resetGame(self) -> Any:
        """ """
        return self


class NchantdMapCanvas(NchantdCanvas):
    """ """

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdMapCanvas").override(cfg))

    def initModel(self) -> Any:
        """"""
        return self

    def initView(self) -> Any:
        """"""
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdWireFrameCanvas(NchantdCanvas):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdWireFrameCanvas").override(cfg))

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


class NchantdSpace(NchantdCanvas):
    """An Nchantd Space is a 3D Canvas Widget"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdSpace")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self.parent, self.config)
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


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
