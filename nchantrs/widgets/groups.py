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

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from networkx.algorithms.connectivity import minimum_node_cut

from nchantrs.libraries import pyqt
from ogma.logma import Logma
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "groups.yaml")
pxcfg = {}


class NchantdGroup(NchantdWidgetMixin, pyqt.QGroupBox):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__()
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdGroup")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.init_variables()
        self.collapsible = None
        self.fixed_height = None
        self.set_collapsible(self.config.dikt.get("collapsible", False))
        self.collapsed = self.config.dikt.get("collapsed", False)
        if self.collapsed:
            self.set_open(False)
        label = self.config.dikt.get("text", "Missing Group Text")
        self.setTitle(label)
        self.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop | pyqt.Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(self.sizePolicy().horizontalPolicy(), self.sizePolicy().verticalPolicy())
        self.toggled.connect(self.set_open)

    def set_height(self, height, show=True):
        """"""
        self.fixed_height = height
        if self.fixed_height is not None and show:
            self.set_open(True)
        return self

    def show(self):
        """"""
        logma.info(f"Show {self.config.dikt.get('text', 'Missing Group Text')}")
        # size = self.config.dikt.get("size", [None, 250])
        logma.info(f"Size {self.parent.size().height()}")
        minimum_height = 250
        height = self.parent.size().height()
        if height < minimum_height:
            height = minimum_height
        logma.info(f"Height {self.height}")
        if self.fixed_height is None:
            self.set_height(height)
        # self.set_size("auto", self.parent.size().height(), None, 250)
        # cfg_height = self.config.dikt.get("size", [None, minimum_height])[1]
        # if cfg_height == "auto":
        # height = minimum_height

        self.setMinimumHeight(self.fixed_height)
        self.setMaximumHeight(self.fixed_height)
        # self.updateGeometry()
        # self.parent.updateGeometry()
        return self

    def hide(self):
        """"""
        logma.info(f"Hide {self.config.dikt.get('text', 'Missing Group Text')}")
        size = self.config.dikt.get("hidden_size", [None, 30])
        self.set_size("auto", size[1], size[0], size[1])
        self.setMinimumHeight(size[1])
        self.setMaximumHeight(size[1])
        self.parent.updateGeometry()
        return self

    def set_open(self, switch=True):
        """"""
        if switch:
            self.setChecked(True)
            self.show()
        else:
            self.setChecked(False)
            self.hide()
        return self

    def set_collapsible(self, switch=True):
        """"""
        if switch:
            self.setCheckable(True)
            self.set_open(True)
        else:
            self.setCheckable(False)
            self.set_open(True)
        return self


class NchantdCollapsableGroup(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdCollapsableGroup"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.tree = None
        self.root_item = None
        self.child_item = None
        self.widget = None

    def initView(self, cfg=None):
        """"""
        self.config.override(cfg)
        layout = pyqt.QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.tree = pyqt.QTreeWidget()
        layout.addWidget(self.tree)
        self.tree.setHeaderHidden(True)
        self.tree.setColumnCount(1)
        self.tree.setIndentation(5)
        self.tree.setStyleSheet(
            """
            QTreeView {
                border: 1px solid #4F5665;
            }
            QTreeView::item {
                border: 1px solid #5F5FDF;     /* Border only for child items */
                padding: 4px;
                font-size: 14px;
            }
        """
        )
        # self.root_item = pyqt.QTreeWidgetItem(self.tree)
        # self.root_item.setText(0, self.config.dikt.get("text", "Missing Group Title"))
        # self.child_item = pyqt.QTreeWidgetItem()
        # self.root_item.addChild(self.child_item)
        # widget = pyqt.QWidget()
        if self.config.dikt.get("layout", None) == "horizontal":
            self.layout = pyqt.QHBoxLayout()
        elif self.config.dikt.get("layout", None) == "grid":
            self.layout = pyqt.QGridLayout()
        else:
            self.layout = pyqt.QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # widget.setLayout(self.layout)
        # self.tree.setItemWidget(self.child_item, 0, widget)
        self.setLayout(self.layout)
        self.set_size()
        return self

    def initWidget(self):
        """"""
        self.initView()
        return self

    def addWidget(self, widget, cfg=None, row=0, column=0, row_span=1, column_span=1):
        """"""
        self.config.override(cfg)
        root_item = pyqt.QTreeWidgetItem(self.tree)
        root_item.setText(0, self.config.dikt.get("text", "Missing Group Title"))
        self.child_item = pyqt.QTreeWidgetItem()
        root_item.addChild(self.child_item)
        self.tree.setItemWidget(self.child_item, 0, widget)
        return self


class NchantdHGroupBox(pyqt.QGroupBox):
    """"""

    def __init__(self, parent=None, cfg=None):
        """"""
        super().__init__(parent, cfg)
        self.config = condor.Instruct(pxcfg).select("NchantdHGroupBox")
        self.parent = parent
        if parent is not None and not isinstance(parent, pyqt.QWidget):
            self.config.override(parent.config)
        self.config.override(cfg)

    def addWidget(self, widget):
        """"""
        self.layout.addWidget(widget)
        return self

    def initModel(self):
        """"""
        return self

    def initView(self):
        """"""
        self.layout = pyqt.QHBoxLayout(self)
        self.setLayout(self.layout)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdVGroupBox(pyqt.QGroupBox):
    """"""

    def __init__(self, parent=None, cfg=None):
        """"""
        super().__init__()
        self.config = condor.Instruct(pxcfg).select("NchantdVGroupBox")
        self.parent = parent
        if parent is not None and not isinstance(parent, pyqt.QWidget):
            self.config.override(parent.config)
        self.config.override(cfg)

    def addWidget(self, widget):
        """"""
        self.layout.addWidget(widget)
        return self

    def initModel(self):
        """"""
        return self

    def initView(self):
        """"""
        self.layout = pyqt.QHBoxLayout(self)
        self.setLayout(self.layout)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdVScrollGroupBox(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """"""
        super().__init__(parent, cfg)
        self.config.override(condor.Instruct(pxcfg).select("NchantdVScrollGroupBox"))
        self.parent = parent
        if parent is not None and not isinstance(parent, pyqt.QWidget):
            self.config.override(parent.config)
        self.config.override(cfg)
        self.initLayout()

    def addWidget(self, widget):
        """"""
        self.layout_box.addWidget(widget)
        return self

    def initLayout(self):
        """"""
        cfg = {}
        self.group = NchantdGroup(self, cfg)
        layout = pyqt.QVBoxLayout()
        self.group.setLayout(layout)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.scroll = pyqt.QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(pyqt.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(pyqt.Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self)
        self.scroll.setWidgetResizable(False)
        self.scroll.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)

        layout.addWidget(self.scroll)
        layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)

        self.layout = pyqt.QVBoxLayout()
        self.layout.addWidget(self.group)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout_box = pyqt.QVBoxLayout(self)
        logma.info(f"Parent Size {self.parent.size().height()}")
        logma.info(f"Size {self.size().width()}")
        logma.info(f"Group Size {self.group.size().height()}")
        self.set_size("auto", self.parent.size().height())
        return self

    def setTitle(self, title):
        self.group.setTitle(title)

    def setMinimumHeight(self, height):
        """"""
        self.group.setMinimumHeight(height)

    def set_scroll_bar_position(self, position):
        """"""
        if position == "top":
            position = self.scroll.horizontalScrollBar().minimum()
            self.scroll.horizontalScrollBar().setSliderPosition(position)

        elif position == "center":
            position = int((self.scroll.verticalScrollBar().minimum() + self.scroll.verticalScrollBar().maximum()) / 2)
            self.scroll.horizontalScrollBar().setSliderPosition(position)

        elif position == "bottom":
            position = self.scroll.horizontalScrollBar().maximum()
            self.scroll.horizontalScrollBar().setSliderPosition(position)

    def set_size(self, width=None, height=None):
        """"""
        super().set_size(width, height)
        if self.max_width is not None:
            self.group.setMaximumWidth(self.max_width)
        if self.min_width is not None:
            self.group.setMinimumWidth(self.min_width)
        if self.max_height is not None:
            self.group.setMaximumHeight(self.max_height)
        if self.min_height is not None:
            self.group.setMinimumHeight(self.min_height)
        # self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
        # self.layout.setSpacing(0)
        # self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
        # self.layout.setSpacing(0)


class NchantdHScrollGroupBox(pyqt.QWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """"""
        super().__init__(parent)
        self.config = condor.Instruct(pxcfg).select("NchantdHScrollGroupBox")
        self.parent = parent
        if parent is not None and not isinstance(parent, pyqt.QWidget):
            self.config.override(parent.config)
        self.config.override(cfg)
        self.group = None
        self.layout_box = None
        self.scroll = None
        self.initLayout()

    def addWidget(self, widget):
        """"""
        self.layout_box.addWidget(widget)
        return self

    def initLayout(self):
        """"""
        self.layout_box = pyqt.QHBoxLayout(self)

        self.scroll = pyqt.QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(pyqt.Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(pyqt.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self)

        self.group = pyqt.QGroupBox()
        layout = pyqt.QVBoxLayout(self.group)
        layout.addWidget(self.scroll)

        self.layout = pyqt.QVBoxLayout()
        self.layout.addWidget(self.group)
        return self

    # def initLayout(self):
    #     """"""
    #     self.group = pyqt.QGroupBox()
    #     self.layout = pyqt.QHBoxLayout()
    #     self.group.setLayout(self.layout)
    #     self.scroll = pyqt.QScrollArea()
    #     self.scroll.setVerticalScrollBarPolicy(pyqt.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    #     self.scroll.setHorizontalScrollBarPolicy(pyqt.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    #     self.scroll.setWidgetResizable(True)
    #     self.scroll.setWidget(self.group)
    #     self.layout.addWidget(self.scroll)

    def setTitle(self, title):
        self.group.setTitle(title)

    def setMinimumHeight(self, height):
        """"""
        self.group.setMinimumHeight(height)

    def set_size(self, width=None, height=None):
        """"""
        if width is not None:
            self.group.setMaximumWidth(width)
            self.group.setMinimumWidth(width)
        if height is not None:
            self.group.setMaximumHeight(height)
            self.group.setMinimumHeight(height)
        self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)

    def set_scroll_bar_position(self, position):
        """"""
        min_ = self.scroll.horizontalScrollBar().minimum()
        max_ = self.scroll.horizontalScrollBar().maximum()
        if max_ == 0:
            max_ = self.scroll.viewport().size().width() * 2  # TODO HACK:
            self.scroll.horizontalScrollBar().setMaximum(max_)  # TODO HACK:

        logma.info(f"Min {min_} Max {max_}")
        if position == "left":
            position = min_
        elif position == "center":
            position = int((max_ + min_) / 2 + (max_ + min_) / 3)  # TODO HACK:
        elif position == "right":
            position = max_
        else:
            raise Exception(f"Invalid position {position}")
        logma.info(f"Position {position}")
        scrollbar = self.scroll.horizontalScrollBar()
        scrollbar.setSliderPosition(position)
        scrollbar.setValue(position)
        logma.info(f"Position {scrollbar.sliderPosition()}")


class NchantdGridScrollGroupBox(pyqt.QWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """"""
        super().__init__(parent)
        self.config = condor.Instruct(pxcfg)
        self.parent = parent
        if parent is not None and not isinstance(parent, pyqt.QWidget):
            self.config.override(parent.config)
        self.config.override(cfg)
        self.initLayout()

    def addWidget(self, widget, row=0, column=0, row_span=1, column_span=1):
        """"""
        self.layout_grid.addWidget(widget, row, column, row_span, column_span)
        return self

    def initLayout(self):
        """"""
        self.layout_grid = pyqt.QGridLayout(self)
        self.layout_grid.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
        self.scroll = pyqt.QScrollArea()
        self.scroll.setContentsMargins(0, 0, 0, 0)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self)
        self.group = pyqt.QGroupBox()
        layout = pyqt.QVBoxLayout(self.group)
        layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.scroll)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.layout = pyqt.QVBoxLayout()
        self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.group)
        return self

    def limit_horizontal(self, limit=True):
        """"""
        if limit:
            self.scroll.setHorizontalScrollBarPolicy(pyqt.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        else:
            self.scroll.setHorizontalScrollBarPolicy(pyqt.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    def limit_vertical(self, limit=True):
        """"""
        if limit:
            self.scroll.setVerticalScrollBarPolicy(pyqt.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        else:
            self.scroll.setVerticalScrollBarPolicy(pyqt.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    def setTitle(self, title):
        """"""
        self.group.setTitle(title)

    def set_minimum_height(self, height):
        """"""
        # self.scroll.setMinimumHeight(height)
        self.group.setMinimumHeight(height)
        # self.setMinimumHeight(height)

    def set_maximum_height(self, height):
        """"""
        # self.scroll.setMaximumHeight(height)
        self.group.setMaximumHeight(height)
        # self.setMaximumHeight(height)

    def set_size(self, width=None, height=None):
        """"""
        if width is not None:
            self.group.setMaximumWidth(width)
            self.group.setMinimumWidth(width)
        if height is not None:
            self.group.setMaximumHeight(height)
            self.group.setMinimumHeight(height)
        self.layout_grid.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
        self.layout_grid.setSpacing(0)
        self.layout_grid.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
