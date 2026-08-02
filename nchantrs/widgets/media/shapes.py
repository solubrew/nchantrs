from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from nchantrs.libraries import pyqt
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')

class NchantdShape(pyqt.QWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdShape')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdShape, self).__init__(self.parent, self.config)
        self.qp = None
        logma.info(f'NchantdShape initialized')

    def initModel(self) -> Any:
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> Any:
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

    def move_shape(self, x, y) -> None:
        logma.info(f'move_shape called')
        return self

    def paintEvent(self, event) -> Any:
        """"""
        self.qp = pyqt.QPainter(self)
        self.qp.setBrush(pyqt.QBrush(pyqt.QColor(self.background_color)))
        return self

    def set_anchor(self) -> None:
        logma.info(f'set_anchor called')
        return self

    def set_background_color(self, color) -> None:
        logma.info(f'set_background_color called')
        return self

    def set_border_color(self, color) -> None:
        logma.info(f'set_border_color called')
        return self

class NchantdEllipse(NchantdShape):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdEllipse')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdEllipse, self).__init__(self.parent, self.config)
        self.dragging = False
        self.drag_offset = None
        logma.info(f'NchantdEllipse initialized')

    def initModel(self) -> Any:
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> Any:
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

    def paintEvent(self, event) -> None:
        qp = pyqt.QPainter(self)
        qp.setBrush(pyqt.QBrush(pyqt.QColor(self.background_color)))
        rect = pyqt.QRectF(0, 0, self.width(), self.height())
        qp.drawEllipse(rect)

    def mousePressEvent(self, event) -> None:
        self.dragging = True
        self.drag_offset = event.posF()

    def mouseMoveEvent(self, event) -> None:
        if self.dragging:
            dx = event.posF().x() - self.drag_offset.x()
            dy = event.posF().y() - self.drag_offset.y()
            self.setGeometry(self.x() + dx, self.y() + dy, self.width(), self.height())

    def mouseReleaseEvent(self, event) -> None:
        self.dragging = False

    def mouseDoubleClickEvent(self, event) -> None:
        self.setGeometry(self.x(), self.y(), self.width() + 50, self.height() + 50)

class NchantdCircle(NchantdEllipse):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdCircle')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdCircle, self).__init__(self.parent, self.config)

    def initModel(self) -> Any:
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> Any:
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

class NchantdPolygon(NchantdShape):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdPolygon')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdPolygon, self).__init__(self.parent, self.config)
        self.background_color = None
        self.border_color = None
        self.foreground_color = None
        self.set_vertices({0: {'x': 0, 'y': 0}, 1: {'x': 1, 'y': 2}, 2: {'x': 2, 'y': 0}})
        logma.info(f'NchantdPolygon initialized')

    def initModel(self) -> Any:
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> Any:
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

    def paintEvent(self, event) -> Any:
        """"""
        super().paintEvent(event)
        pointWs = []
        for point in self.verticies:
            pointWs.append(pyqt.QPoint(point['x'], point['y']))
        polygon = pyqt.QPolygon(pointWs)
        self.qp.drawPolygon(polygon)
        self.qp = None
        return self

    def get_shape(self) -> Any:
        """"""
        if self.vertices_count == 3:
            self.shape = 'triangle'
        elif self.vertices_count == 4:
            self.shape = 'rectangle'
        elif self.vertices_count == 5:
            self.shape = 'pentagon'
        elif self.vertices_count == 6:
            self.shape = 'hexagon'
        elif self.vertices_count == 7:
            self.shape = 'heptagon'
        elif self.vertices_count == 8:
            self.shape = 'octagon'
        elif self.vertices_count == 9:
            self.shape = 'nonagon'
        elif self.vertices_count == 10:
            self.shape = 'decagon'
        return self.shape

    def add_vertex(self, x, y) -> None:
        """"""
        self.vertices[self.vertices_count]['x'] = x
        self.vertices[self.vertices_count]['y'] = y
        self.set_vertices()

    def move_vertex(self, vertex, x, y, x1=None, y1=None) -> None:
        logma.info(f'move_vertex called')
        return self

    def remove_vertex(self, x, y, pos=None) -> None:
        """"""
        if pos is None:
            pos = [i for i in range(len(self.vertices)) if self.vertices[i]['x'] == x and self.vertices[i]['y'] == y][0]
        self.vertices.pop(pos)
        self.set_vertices()

    def set_vertices(self, vertices=None) -> Any:
        """"""
        if vertices is not None:
            self.vertices = vertices
        self.vertices_count = len(self.vertices)
        self.get_shape()
        return self