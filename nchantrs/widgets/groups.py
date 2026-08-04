from typing import Any

"\n---\n<(META)>:\n    docid:\n    name:\n    description: >\n    version: 0.0.0.0.0.0\n    authority: filesystem\n    security: seclvl2\n    <(WT)>: -32\n"
from os.path import abspath, dirname, join
import datetime as dt
from kahndor import kahndor
from networkx.algorithms.connectivity import minimum_node_cut
from nchantrs.libraries import pyqt
from kahndor.logma import Logma
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin

here = join(dirname(__file__), "")
logma = Logma(__name__)
logma.off()
pxcfg = join(here, "_data_", "groups.yaml")


class NchantdGroup(NchantdWidgetMixin, pyqt.QGroupBox):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__()
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdGroup").override(parent.config).override(cfg)
        self.collapsible = None
        self.fixed_height = None
        # self.set_collapsible(self.config.dikt.get("collapsible", False))
        # self.collapsed = self.config.dikt.get("collapsed", False)
        # if self.collapsed:
        #     self.set_open(False)
        label = self.config.dikt.get("text", "Missing Group Text")
        self.setTitle(label)
        # self.setSizePolicy(self.sizePolicy().horizontalPolicy(), self.sizePolicy().verticalPolicy())
        self.toggled.connect(self.set_open)

    def set_height(self, height, show=True) -> Any:
        """"""
        self.fixed_height = height
        if self.fixed_height is not None and show:
            self.set_open(True)
        return self

    def show(self) -> Any:
        """"""
        logma.info(f"Show {self.config.dikt.get('text', 'Missing Group Text')}")
        logma.info(f"Size {self.parent.size().height()}")
        return self

    def hide(self) -> Any:
        """"""
        logma.info(f"Hide {self.config.dikt.get('text', 'Missing Group Text')}")
        size = self.config.dikt.get("hidden_size", [None, 30])
        self.set_size("auto", size[1], size[0], size[1])
        self.setMinimumHeight(size[1])
        self.setMaximumHeight(size[1])
        self.parent.updateGeometry()
        return self

    def set_open(self, switch=True) -> Any:
        """"""
        if switch:
            self.setChecked(True)
            self.show()
        else:
            self.setChecked(False)
            self.hide()
        return self

    def set_collapsible(self, switch=True) -> Any:
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

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdCollapsableGroup").override(cfg))
        self.tree = None
        self.root_item = None
        self.child_item = None
        self.widget = None

    def initView(self, cfg=None) -> Any:
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
            "\n            QTreeView {\n                border: 1px solid #4F5665;\n            }\n            QTreeView::item {\n                border: 1px solid #5F5FDF;     /* Border only for child items */\n                padding: 4px;\n                font-size: 14px;\n            }\n        "
        )
        if self.config.dikt.get("layout", None) == "horizontal":
            self.layout = pyqt.QHBoxLayout()
        elif self.config.dikt.get("layout", None) == "grid":
            self.layout = pyqt.QGridLayout()
        else:
            self.layout = pyqt.QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.set_size()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initView()
        return self

    def addWidget(self, widget, cfg=None, row=0, column=0, row_span=1, column_span=1) -> Any:
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

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        super().__init__(parent, cfg)
        self.config = kahndor.Instruct(pxcfg).select("NchantdHGroupBox")
        self.parent = parent
        if parent is not None and (not isinstance(parent, pyqt.QWidget)):
            self.config.override(parent.config)
        self.config.override(cfg)
        logma.info(f"NchantdHGroupBox initialized")

    def addWidget(self, widget) -> Any:
        """"""
        self.layout.addWidget(widget)
        return self

    def initModel(self) -> Any:
        super().initModel()
        logma.info(f"initModel {{type(self).__name__}}")
        return self

    def initView(self) -> Any:
        """"""
        self.layout = pyqt.QHBoxLayout(self)
        self.setLayout(self.layout)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdVGroupBox(pyqt.QGroupBox):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        super().__init__()
        self.config = kahndor.Instruct(pxcfg).select("NchantdVGroupBox")
        self.parent = parent
        if parent is not None and (not isinstance(parent, pyqt.QWidget)):
            self.config.override(parent.config)
        self.config.override(cfg)
        logma.info(f"NchantdVGroupBox initialized")

    def addWidget(self, widget) -> Any:
        """"""
        self.layout.addWidget(widget)
        return self

    def initModel(self) -> Any:
        super().initModel()
        logma.info(f"initModel {{type(self).__name__}}")
        return self

    def initView(self) -> Any:
        """"""
        self.layout = pyqt.QHBoxLayout(self)
        self.setLayout(self.layout)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdVScrollGroupBox(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdVScrollGroupBox").override(cfg))
        self.initLayout()
        logma.info(f"NchantdVScrollGroupBox initialized")

    def addWidget(self, widget) -> Any:
        """"""
        self.layout_box.addWidget(widget)
        return self

    def initLayout(self) -> Any:
        """"""
        cfg = {}
        self.group = NchantdGroup(self, cfg)
        if self.config.get("height", None):
            self.setMaxiumHeight(self.config.get("height"))
        self.layout_box = pyqt.QVBoxLayout(self)
        # self.layout_box.addStretch()
        # self.layout_box.setSpacing(0)
        self.layout_box.setContentsMargins(0, 0, 0, 0)
        self.scroll = pyqt.QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(pyqt.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(pyqt.Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self)
        layout = pyqt.QVBoxLayout()
        self.group.setLayout(layout)
        # layout.setSpacing(0)
        # layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.scroll)
        self.layout = pyqt.QVBoxLayout()
        self.layout.addWidget(self.group)
        # self.layout.setSpacing(0)
        # self.layout.setContentsMargins(0, 0, 0, 0)
        return self

    def setTitle(self, title) -> None:
        self.group.setTitle(title)

    def setMaxiumHeight(self, height) -> None:
        """"""
        self.group.setMaximumHeight(height)

    def setMinimumHeight(self, height) -> None:
        """"""
        self.group.setMinimumHeight(height)

    def set_scroll_bar_position(self, position) -> None:
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

    def set_size(self, width=None, height=None) -> None:
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


class NchantdHScrollGroupBox(pyqt.QWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        super().__init__(parent)
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdHScrollGroupBox").override(cfg)
        self.group = None
        self.layout_box = None
        self.scroll = None
        self.initLayout()

    def addWidget(self, widget) -> Any:
        """"""
        self.layout_box.addWidget(widget)
        return self

    def initLayout(self) -> Any:
        """"""
        self.layout_box = pyqt.QHBoxLayout(self)
        self.scroll = pyqt.QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(pyqt.Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(pyqt.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self)
        self.group = pyqt.QGroupBox()
        if self.config.get("height", None):
            self.setMaxiumHeight(self.config.get("height"))
        layout = pyqt.QVBoxLayout(self.group)
        layout.addWidget(self.scroll)
        self.layout = pyqt.QVBoxLayout()
        self.layout.addWidget(self.group)
        return self

    def setTitle(self, title) -> None:
        """"""
        self.group.setTitle(title)

    def setMinimumHeight(self, height) -> None:
        """"""
        self.group.setMinimumHeight(height)

    def setMaxiumHeight(self, height) -> None:
        """"""
        self.group.setMaximumHeight(height)

    def set_size(self, width=None, height=None) -> None:
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

    def set_scroll_bar_position(self, position) -> None:
        """"""
        min_ = self.scroll.horizontalScrollBar().minimum()
        max_ = self.scroll.horizontalScrollBar().maximum()
        if max_ == 0:
            max_ = self.scroll.viewport().size().width() * 2
            self.scroll.horizontalScrollBar().setMaximum(max_)
        logma.info(f"Min {min_} Max {max_}")
        if position == "left":
            position = min_
        elif position == "center":
            position = int((max_ + min_) / 2 + (max_ + min_) / 3)
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

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        super().__init__(parent)
        self.config = kahndor.Instruct(pxcfg)
        self.parent = parent
        if parent is not None and (not isinstance(parent, pyqt.QWidget)):
            self.config.override(parent.config)
        self.config.override(cfg)
        self.initLayout()
        logma.info(f"NchantdGridScrollGroupBox initialized")

    def addWidget(self, widget, row=0, column=0, row_span=1, column_span=1) -> Any:
        """"""
        self.layout_grid.addWidget(widget, row, column, row_span, column_span)
        return self

    def initLayout(self) -> Any:
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

    def limit_horizontal(self, limit=True) -> None:
        """"""
        if limit:
            self.scroll.setHorizontalScrollBarPolicy(pyqt.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        else:
            self.scroll.setHorizontalScrollBarPolicy(pyqt.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    def limit_vertical(self, limit=True) -> None:
        """"""
        if limit:
            self.scroll.setVerticalScrollBarPolicy(pyqt.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        else:
            self.scroll.setVerticalScrollBarPolicy(pyqt.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    def setTitle(self, title) -> None:
        """"""
        self.group.setTitle(title)

    def set_minimum_height(self, height) -> None:
        """"""
        self.group.setMinimumHeight(height)

    def set_maximum_height(self, height) -> None:
        """"""
        self.group.setMaximumHeight(height)

    def set_size(self, width=None, height=None) -> None:
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
