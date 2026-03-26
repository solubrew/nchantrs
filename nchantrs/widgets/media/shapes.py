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
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")
pxcfg = {}


class NchantdShape(pyqt.QWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdShape")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdShape, self).__init__(self.parent, self.config)
        self.qp = None

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

    def move_shape(self, x, y):
        """"""

    def paintEvent(self, event):
        """"""
        self.qp = pyqt.QPainter(self)
        self.qp.setBrush(pyqt.QBrush(pyqt.QColor(self.background_color)))
        return self

    def set_anchor(self):
        """"""

    def set_background_color(self, color):
        """"""

    def set_border_color(self, color):
        """"""


class NchantdEllipse(NchantdShape):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdEllipse")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdEllipse, self).__init__(self.parent, self.config)
        self.dragging = False
        self.drag_offset = None

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

    def paintEvent(self, event):
        qp = pyqt.QPainter(self)
        qp.setBrush(pyqt.QBrush(pyqt.QColor(self.background_color)))
        rect = pyqt.QRectF(0, 0, self.width(), self.height())
        qp.drawEllipse(rect)

    def mousePressEvent(self, event):
        self.dragging = True
        self.drag_offset = event.posF()

    def mouseMoveEvent(self, event):
        if self.dragging:
            dx = event.posF().x() - self.drag_offset.x()
            dy = event.posF().y() - self.drag_offset.y()
            self.setGeometry(self.x() + dx, self.y() + dy, self.width(), self.height())

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def mouseDoubleClickEvent(self, event):
        self.setGeometry(self.x(), self.y(), self.width() + 50, self.height() + 50)


class NchantdCircle(NchantdEllipse):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdCircle")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdCircle, self).__init__(self.parent, self.config)

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


class NchantdPolygon(NchantdShape):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdPolygon")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdPolygon, self).__init__(self.parent, self.config)
        self.background_color = None
        self.border_color = None
        self.foreground_color = None
        self.set_vertices({0: {"x": 0, "y": 0}, 1: {"x": 1, "y": 2}, 2: {"x": 2, "y": 0}})

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

    def paintEvent(self, event):
        """"""
        super().paintEvent(event)
        pointWs = []
        for point in self.verticies:
            pointWs.append(pyqt.QPoint(point["x"], point["y"]))
        polygon = pyqt.QPolygon(pointWs)
        self.qp.drawPolygon(polygon)
        self.qp = None
        return self

    def get_shape(self):
        """"""
        if self.vertices_count == 3:
            self.shape = "triangle"
        elif self.vertices_count == 4:
            self.shape = "rectangle"
        elif self.vertices_count == 5:
            self.shape = "pentagon"
        elif self.vertices_count == 6:
            self.shape = "hexagon"
        elif self.vertices_count == 7:
            self.shape = "heptagon"
        elif self.vertices_count == 8:
            self.shape = "octagon"
        elif self.vertices_count == 9:
            self.shape = "nonagon"
        elif self.vertices_count == 10:
            self.shape = "decagon"
        return self.shape

    def add_vertex(self, x, y):
        """"""
        self.vertices[self.vertices_count]["x"] = x
        self.vertices[self.vertices_count]["y"] = y
        self.set_vertices()

    def move_vertex(self, vertex, x, y, x1=None, y1=None):
        """"""

    def remove_vertex(self, x, y, pos=None):
        """"""
        if pos is None:
            pos = [i for i in range(len(self.vertices)) if self.vertices[i]["x"] == x and self.vertices[i]["y"] == y][0]
        self.vertices.pop(pos)
        self.set_vertices()

    def set_vertices(self, vertices=None):
        """"""
        if vertices is not None:
            self.vertices = vertices
        self.vertices_count = len(self.vertices)
        self.get_shape()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
