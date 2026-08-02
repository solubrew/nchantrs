from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidgetMixin
from kahndor.logma import Logma
from nchantrs.widgets.canvases.scenes import NchantdScene
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'canvases.yaml')

class ThreeJSWidget(pyqt.QWebEngineView):
    """
    This widget renders a `pythreejs` 3D visualization inside a QWebEngineView.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        html_content = self.generate_html()
        self.setHtml(html_content)

    def generate_html(self) -> str:
        """
        Generate a pythreejs 3D scene as an HTML string.
        """
        geometry = BoxGeometry(width=1, height=1, depth=1)
        material = MeshStandardMaterial(color='blue')
        cube = Mesh(geometry, material)
        scene = Scene(children=[cube, AmbientLight(color='#aaaaaa')])
        camera = PerspectiveCamera(position=[3, 3, 3])
        camera.lookAt([0, 0, 0])
        controls = OrbitControls(controlling=camera)
        renderer = Renderer(camera=camera, scene=scene, controls=[controls], width=800, height=600)
        return f'\n        <!DOCTYPE html>\n        <html>\n        <head>\n            <title>PyThreeJS Visualization</title>\n        </head>\n        <body>\n            {renderer._repr_html_()}\n        </body>\n        </html>\n        '

class NchantdCanvas(NchantdWidgetMixin, pyqt.QGraphicsView):
    """NchantdCanvas is a Generic Canvas Widget"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdCanvas').override(cfg)
        self.scene = None
        self.shapes = None
        self._display_pixmap = None
        logma.info(f'NchantdCanvas initialized')

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        self.context_menu = self.parent.context_menu
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        cfg = {}
        self.scene = NchantdScene(self, cfg).initWidget()
        self.setScene(self.scene)
        self.scene.setSceneRect(pyqt.QRectF(0, 0, 10000, 10000))
        ellipse = pyqt.QGraphicsEllipseItem(0, 0, 100, 100)
        ellipse.setPos(5000, 5000)
        self.scene.addItem(ellipse)
        self.setDragMode(pyqt.QGraphicsView.ScrollHandDrag)
        self.set_size()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def add_item(self, item, position=[0, 0]) -> None:
        """"""
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
        if self._display_pixmap and (not self._display_pixmap.isNull()):
            painter.save()
            painter.resetTransform()
            painter.drawPixmap(0, 0, self._display_pixmap)
            painter.restore()

class NchantdPaintCanvas(NchantdCanvas):
    """A canvas widget specifically designed for direct painting/drawing operations."""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdPaintCanvas').override(cfg))
        logma.info(f'NchantdPaintCanvas initialized')

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
        if hasattr(self, 'canvas'):
            new_pixmap = pyqt.QPixmap(event.size())
            new_pixmap.fill(pyqt.Qt.white)
            painter = pyqt.QPainter(new_pixmap)
            painter.drawPixmap(0, 0, self.canvas)
            painter.end()
            self.canvas = new_pixmap

    def drawForeground(self, painter, rect) -> None:
        """Draw the paint canvas pixmap."""
        super().drawForeground(painter, rect)
        if hasattr(self, 'canvas') and (not self.canvas.isNull()):
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
        if event.buttons() & pyqt.Qt.LeftButton and hasattr(self, 'canvas'):
            painter = pyqt.QPainter(self.canvas)
            painter.setPen(pyqt.QPen(self.pen_color, self.pen_width, pyqt.Qt.SolidLine, pyqt.Qt.RoundCap, pyqt.Qt.RoundJoin))
            painter.drawLine(self.last_point, event.pos())
            painter.end()
            self.last_point = event.pos()
            self.viewport().update()

    def clear(self) -> None:
        """Clear the canvas."""
        if hasattr(self, 'canvas'):
            self.canvas.fill(pyqt.Qt.white)
            self.viewport().update()

    def select_pen_color(self) -> None:
        """Open color dialog to select pen color."""
        color = pyqt.QColorDialog.getColor()
        if color.isValid():
            self.pen_color = color

    def select_pen_width(self) -> None:
        """Open dialog to select pen width."""
        i, okPressed = pyqt.QInputDialog.getInt(self, 'Pen Width', 'Value:', self.pen_width, 1, 50, 1)
        if okPressed:
            self.pen_width = i

class NchantdGameCanvas(NchantdCanvas):
    """NchantdGame is a Canvas Widget sandbox for running a game inside an
    Nchantd application using the PyGame game engine"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdGameCanvas').override(cfg))
        logma.info(f'NchantdGameCanvas initialized')

    def initModel(self) -> Any:
        super().initModel()
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> Any:
        super().initView()
        logma.info(f'initView {{type(self).__name__}}')
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def startGame(self) -> Any:
        logma.info(f'startGame called')
        return self

    def pauseGame(self) -> Any:
        logma.info(f'pauseGame called')
        return self

    def exitGame(self) -> Any:
        logma.info(f'exitGame called')
        return self

    def resetGame(self) -> Any:
        logma.info(f'resetGame called')
        return self

class NchantdMapCanvas(NchantdCanvas):
    """ """

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdMapCanvas').override(cfg))

    def initModel(self) -> Any:
        super().initModel()
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> Any:
        super().initView()
        logma.info(f'initView {{type(self).__name__}}')
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
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdWireFrameCanvas').override(cfg))

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
        self.config = kahndor.Instruct(pxcfg).select('NchantdSpace')
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