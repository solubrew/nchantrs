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
from ogma.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidgetMixin

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "scenes.yaml")
pxcfg = {}


class NchantdProxyWidget(NchantdWidgetMixin, pyqt.QGraphicsProxyWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdProxyWidget")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def mousePressEvent(self, event):
        """Detect and start resizing if the user clicks near the edges."""
        if self.is_near_edge(event.pos()):
            self.is_resizing = True  # Start resizing mode
            self.setCursor(Qt.SizeHorCursor)  # Change cursor to horizontal resize
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle resizing or dragging based on the event."""
        if self.is_resizing:
            # Resize the widget by adjusting its width while dragging
            delta_x = event.scenePos().x() - self.sceneBoundingRect().right()
            new_width = max(50, self.line_edit.width() + delta_x)  # Minimum width = 50
            self.line_edit.setFixedWidth(new_width)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Stop resizing when the mouse button is released."""
        if self.is_resizing:
            self.is_resizing = False
            self.setCursor(pyqt.Qt.ArrowCursor)  # Reset cursor to default
        else:
            super().mouseReleaseEvent(event)

    def is_near_edge(self, pos):
        """Determine if the mouse is near the right edge of the textbox."""
        rect = self.boundingRect()
        return rect.right() - 10 < pos.x() < rect.right() + 10  # Distance near the edge


class NchantdScene(pyqt.QGraphicsScene):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent)
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdScene")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.widgets = []
        self.lines = []
        self.start_widget = None

    def initModel(self, cfg=None):
        """"""
        return self

    def initView(self, cfg=None):
        """"""
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def add_proxy_widget(self, widget, position=[0, 0]):
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

    def create_line(self, start_widget, end_widget):
        """Create and draw a link (line) between two widgets."""
        start_center = start_widget.sceneBoundingRect().center()
        end_center = end_widget.sceneBoundingRect().center()
        # Draw a line connecting the two widget centers
        path = pyqt.QPainterPath()
        path.moveTo(start_center)
        path.lineTo(end_center)
        line = self.addPath(path, pyqt.QPen(pyqt.Qt.black, 2))
        # Keep track of the line
        self.lines.append((start_widget, end_widget, line))

    def mouseMoveEvent(self, event):
        """Update linked lines when a widget is dragged."""
        for start_widget, end_widget, line in self.lines:
            start_center = start_widget.sceneBoundingRect().center()
            end_center = end_widget.sceneBoundingRect().center()
            # Update the line position dynamically
            path = pyqt.QPainterPath()
            path.moveTo(start_center)
            path.lineTo(end_center)
            line.setPath(path)
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        """Handle mouse press events to start linking widgets."""
        item = self.itemAt(event.scenePos(), pyqt.QTransform())
        if isinstance(item, pyqt.QGraphicsProxyWidget):
            if self.start_widget is None:
                # Store the widget as the starting point
                self.start_widget = item
                item.widget().setStyleSheet("background-color: lightblue;")  # Highlight the starting widget
            else:
                # Create a line from the start widget to the clicked widget
                self.create_line(self.start_widget, item)
                self.start_widget.widget().setStyleSheet("")  # Remove the highlight
                self.start_widget = None  # Reset the starting widget
        else:
            # If user clicks outside a widget, reset the starting widget
            if self.start_widget:
                self.start_widget.widget().setStyleSheet("")
            self.start_widget = None
        super().mousePressEvent(event)

    def add_connection(self, start_textbox, end_textbox):
        """Draw a line between two textboxes."""
        start_center = start_textbox.sceneBoundingRect().center()
        end_center = end_textbox.sceneBoundingRect().center()

        # Create a straight line between the two textboxes
        path = pyqt.QPainterPath()
        path.moveTo(start_center)
        path.lineTo(end_center)
        line = self.addPath(path, pyqt.QPen(pyqt.Qt.black, 2))

        # Keep track of connections
        self.lines.append((start_textbox, end_textbox, line))


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
