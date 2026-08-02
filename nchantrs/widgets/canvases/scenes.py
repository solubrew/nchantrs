from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidgetMixin
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'scenes.yaml')

class NchantdProxyWidget(NchantdWidgetMixin, pyqt.QGraphicsProxyWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdProxyWidget').override(cfg))
        logma.info(f'NchantdProxyWidget initialized')

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def mousePressEvent(self, event) -> None:
        """Detect and start resizing if the user clicks near the edges."""
        if self.is_near_edge(event.pos()):
            self.is_resizing = True
            self.setCursor(Qt.SizeHorCursor)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        """Handle resizing or dragging based on the event."""
        if self.is_resizing:
            delta_x = event.scenePos().x() - self.sceneBoundingRect().right()
            new_width = max(50, self.line_edit.width() + delta_x)
            self.line_edit.setFixedWidth(new_width)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        """Stop resizing when the mouse button is released."""
        if self.is_resizing:
            self.is_resizing = False
            self.setCursor(pyqt.Qt.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)

    def is_near_edge(self, pos) -> bool:
        """Determine if the mouse is near the right edge of the textbox."""
        rect = self.boundingRect()
        return rect.right() - 10 < pos.x() < rect.right() + 10

class NchantdScene(pyqt.QGraphicsScene):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent)
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdScene').override(cfg)
        self.widgets = []
        self.lines = []
        self.start_widget = None
        logma.info(f'NchantdScene initialized')

    def initModel(self, cfg=None) -> Any:
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self, cfg=None) -> Any:
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initView {{type(self).__name__}}')
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def add_proxy_widget(self, widget, position=[0, 0]) -> Any:
        """"""
        proxy = pyqt.QGraphicsProxyWidget()
        proxy.setWidget(widget)
        proxy.setPos(*position)
        proxy.setFlag(proxy.GraphicsItemFlag.ItemIsMovable)
        proxy.setFlag(proxy.GraphicsItemFlag.ItemIsFocusable)
        proxy.setFlag(proxy.GraphicsItemFlag.ItemSendsGeometryChanges)
        proxy.setFlag(proxy.GraphicsItemFlag.ItemIsSelectable)
        self.addItem(proxy)
        self.widgets.append(proxy)
        return self

    def create_line(self, start_widget, end_widget) -> None:
        """Create and draw a link (line) between two widgets."""
        start_center = start_widget.sceneBoundingRect().center()
        end_center = end_widget.sceneBoundingRect().center()
        path = pyqt.QPainterPath()
        path.moveTo(start_center)
        path.lineTo(end_center)
        line = self.addPath(path, pyqt.QPen(pyqt.Qt.black, 2))
        self.lines.append((start_widget, end_widget, line))

    def mouseMoveEvent(self, event) -> None:
        """Update linked lines when a widget is dragged."""
        for start_widget, end_widget, line in self.lines:
            start_center = start_widget.sceneBoundingRect().center()
            end_center = end_widget.sceneBoundingRect().center()
            path = pyqt.QPainterPath()
            path.moveTo(start_center)
            path.lineTo(end_center)
            line.setPath(path)
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event) -> None:
        """Handle mouse press events to start linking widgets."""
        item = self.itemAt(event.scenePos(), pyqt.QTransform())
        if isinstance(item, pyqt.QGraphicsProxyWidget):
            if self.start_widget is None:
                self.start_widget = item
                item.widget().setStyleSheet('background-color: lightblue;')
            else:
                self.create_line(self.start_widget, item)
                self.start_widget.widget().setStyleSheet('')
                self.start_widget = None
        else:
            if self.start_widget:
                self.start_widget.widget().setStyleSheet('')
            self.start_widget = None
        super().mousePressEvent(event)

    def add_connection(self, start_textbox, end_textbox) -> None:
        """Draw a line between two textboxes."""
        start_center = start_textbox.sceneBoundingRect().center()
        end_center = end_textbox.sceneBoundingRect().center()
        path = pyqt.QPainterPath()
        path.moveTo(start_center)
        path.lineTo(end_center)
        line = self.addPath(path, pyqt.QPen(pyqt.Qt.black, 2))
        self.lines.append((start_textbox, end_textbox, line))