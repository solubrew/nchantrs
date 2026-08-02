from typing import Any, Optional, Union

"#\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n---  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n<(META)>:  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n    DOCid:   #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n    name:   #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n    description: >  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n          #\t\t\t||\n    expirary: <[expiration]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t||\n    version: <[version]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n    path: <[LEXIvrs]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n    outline: <[outline]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n    authority: document|this  #\t\t\t\t\t\t\t\t\t\t\t\t\t||\n    security: sec|lvl2  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n    <(WT)>: -32  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n"
from os.path import abspath, dirname, join
from kahndor import kahndor
import ast
import logging
from subtrix.utilities import uuid

logger = logging.getLogger(__name__)
from nchantrs.libraries import pyqt
from nchantrs.models import tabsetmodels
from nchantrs.widgets.media.notes import NchantdStickyNoteEditor
from nchantrs.widgets.widgets import NchantdWidgetMixin, NchantdWidget
from nchantrs.widgets.trees import NchantdApplicationTree
from kahndor.logma import Logma

here = join(dirname(__file__), "")
log = False
logma = Logma(__name__)
if not log:
    logma.off()
pxcfg = join(abspath(here), "_data_", "tabsets.yaml")


class NchantdTab(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdTab").override(cfg))
        self.tid = None
        self.tabn = None
        self.name = None
        self.position = None
        self.type = None
        self.icon = None
        self.app_data_type = None
        self.notes = []
        self.toolbox = None
        self.toolbox_config = None
        self.has_toolbox = None
        self.dummy = None

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        self.app_data_type = self.config.dikt.get("app_data_type", "doc")
        self.name = self.config.dikt.get("name", None)
        self.tid = self.config.dikt.get("tid", None)
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

    def connect_toolbox(self) -> None:
        logma.info(f"connect_toolbox called")
        return self

    def delete_tab(self, tab) -> Any:
        """"""
        self.app.model.delete_tab(tab)
        logma.info(f"Parent {self.parent}")
        self.parent.set_focus(tab.position - 1)
        return self

    def cmd_delete_tab(self, event=None, *args, **kwargs) -> Any:
        """"""
        logma.info(f"Close Tab {event}")
        self.delete_tab(self.app.active_tab)
        return self

    def cmd_save_tab(self, event=None, *args, **kwargs) -> Any:
        """"""
        self.save()
        return self

    def cmd_tab_edit(self, event=None, *args, **kwargs) -> Any:
        logma.info(f"cmd_tab_edit invoked")
        return self

    def focusInEvent(self, event) -> Any:
        super().focusInEvent(event)
        logma.info(f"Focus In")
        return self

    def focusOutEvent(self, event) -> Any:
        super().focusOutEvent(event)
        logma.info(f"Focus Out")
        return self

    def on_window_move(self, x, y) -> Any:
        """"""
        if len(self.notes) > 0:
            for note in self.notes:
                note.move(x, y)
        return self

    def organize_notes(self) -> Any:
        """"""
        pos = self.geometry().topRight()
        for i, note in enumerate(self.notes):
            note.move(pos.x() - 250, pos.y() + i * 25)
        return self

    def save(self) -> Any:
        logma.info(f"save called")
        return self

    def set_position(self, position) -> Any:
        """"""
        self.position = position
        return self

    def set_tid(self, tid=None) -> Any:
        """"""
        if tid is None:
            tid = uuid()
        self.tid = tid
        return self

    def update_position(self, position, db="db") -> Any:
        """"""
        self.set_position(position)
        data = {"table": {"doc_tab": {"data": {"position_int": self.position}}}}
        self.parent.app.model.store.update_record(data, "tid_txt", self.tid, db)
        return self


class NchantdApplicationControlTab(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdApplicationControl").override(cfg)
        super().__init__(self.parent, self.config)
        self.tree = None
        self.note = None
        logma.info(f"NchantdApplicationControlTab initialized")

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.tree = NchantdApplicationTree(self.parent, self.config).initWidget()
        self.layout.addWidget(self.tree)
        self.note = NchantdStickyNoteEditor(self.parent, self.config).initWidget()
        self.layout.addWidget(self.note)
        return self

    def initWidget(self, pos=None) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def __getstate__(self) -> Any:
        """"""
        state = self.__dict__.copy()
        if state.get("unpickable_attribute", False):
            del state["unpicklable_attribute"]
        return state

    def __setstate__(self, state) -> None:
        """"""


class NchantdTabSet(NchantdWidgetMixin, pyqt.QTabWidget):
    """Nchantd Tab Set provides a widget to show multiple tabs pullig data from
    the Nchantd Tab Set Model and displaying it in the application using
    the Nchantd Tab Set View"""

    DEFAULT_POSITION = "center"
    DEFAULT_TAB_INDEX = -1
    DRAG_PIXMAP_WIDTH = 200
    DRAG_PIXMAP_HEIGHT = 30
    BORDER_RADIUS = 5
    ICON_SIZE = 20
    ICON_MARGIN = 5
    TEXT_MARGIN = 10
    TEXT_Y_OFFSET = 20

    def __init__(self, parent=None, cfg=None) -> None:
        """'"""
        self.parent = parent
        super().__init__()
        self.config = kahndor.Instruct(pxcfg).select("NchantdTabSet").override(parent.config).override(cfg)
        self.model = tabsetmodels.NchantdTabSetModel(self, self.config)
        self.app = pyqt.QApplication.instance()
        self.currenttabn = 0
        self.previous_tab_index = -1
        self.pane_position = self.config.dikt.get("pos", "center")
        self.nid = None
        self.toolbox = None
        self.toolbox_config = None
        self.has_toolbox = None
        self.active_tab = None

    def initModel(self, create_objects=True) -> Any:
        """ """
        super().initModel()
        self.model.initModel(create_objects)
        self.has_toolbox = self.config.dikt.get("has_toolbox", False)
        if hasattr(self.parent, "context_menu"):
            self.context_menu = self.parent.context_menu
        else:
            self.initialize_context_menu()
        return self

    def initTriggers(self) -> Any:
        """"""
        self.currentChanged.connect(self.on_tab_focus)
        return self

    def initView(self) -> Any:
        """"""
        self.setTabPosition(pyqt.QTabWidget.South)
        self.setAcceptDrops(True)
        self.setMovable(True)
        self.drag_start_position = pyqt.QPoint()
        self.initTriggers()
        self.set_focus(0)
        return self

    def initWidget(self, cfg=None) -> Any:
        """ """
        self.initModel(cfg.get("create_objects", True))
        self.initView()
        return self

    def changeEvent(self, event) -> Any:
        logma.info(f"changeEvent called")
        return self

    def create_drag_pixmap(self, text, icon) -> Any:
        """Create a pixmap representation of the dragged tab"""
        pixmap = pyqt.QPixmap(self.DRAG_PIXMAP_WIDTH, self.DRAG_PIXMAP_HEIGHT)
        pixmap.fill(pyqt.Qt.transparent)
        painter = pyqt.QPainter(pixmap)
        painter.setRenderHint(pyqt.QPainter.Antialiasing)
        painter.setBrush(self.palette().button())
        painter.setPen(self.palette().buttonText().color())
        painter.drawRoundedRect(
            0, 0, self.DRAG_PIXMAP_WIDTH, self.DRAG_PIXMAP_HEIGHT, self.BORDER_RADIUS, self.BORDER_RADIUS
        )
        if not icon.isNull():
            icon.paint(painter, self.ICON_MARGIN, self.ICON_MARGIN, self.ICON_SIZE, self.ICON_SIZE)
        painter.drawText(self.TEXT_MARGIN, self.TEXT_Y_OFFSET, text)
        painter.end()
        return pixmap

    def create_toolbox(self, parent, cfg) -> Any:
        logma.info(f"create_toolbox called")
        return self

    def defocus(self) -> Any:
        logma.info(f"defocus called")
        return self

    def dragEnterEvent(self, event) -> None:
        """Handle drag enter events."""
        if event.mimeData().hasText():
            try:
                tab_data = ast.literal_eval(event.mimeData().text())
                if isinstance(tab_data, dict) and "source_widget" in tab_data:
                    event.acceptProposedAction()
                    return
            except Exception:
                pass
        event.ignore()

    def dragMoveEvent(self, event) -> None:
        """Handle drag move events."""
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event) -> None:
        """Handle drop events."""
        if not event.mimeData().hasText():
            event.ignore()
            return
        try:
            tab_data = ast.literal_eval(event.mimeData().text())
            source_widget_id = tab_data["source_widget"]
            source_tab_index = tab_data["tab_index"]
            source_widget = self.find_widget_by_id(source_widget_id)
            if source_widget is None:
                event.ignore()
                return
            widget = source_widget.widget(source_tab_index)
            tab_text = tab_data["text"]
            tab_tooltip = tab_data["tooltip"]
            tab_icon = source_widget.tabIcon(source_tab_index)
            drop_position = self.get_drop_position(event.pos())
            if source_widget != self:
                source_widget.removeTab(source_tab_index)
            else:
                if drop_position > source_tab_index:
                    drop_position -= 1
                source_widget.removeTab(source_tab_index)
            if drop_position == -1:
                new_index = self.addTab(widget, tab_icon, tab_text)
            else:
                new_index = self.insertTab(drop_position, widget, tab_icon, tab_text)
            self.setTabToolTip(new_index, tab_tooltip)
            self.setCurrentIndex(new_index)
            event.acceptProposedAction()
        except Exception as e:
            logger.error(f"Drop error: {e}")
            event.ignore()

    def find_widget_by_id(self, widget_id) -> Optional[Any]:
        """Find a widget by its ID in the application."""
        main_window = self.window()
        if hasattr(main_window, "tab_widgets"):
            for tab_widget in main_window.tab_widgets:
                if id(tab_widget) == widget_id:
                    return tab_widget
        return None

    def focusInEvent(self, event) -> Any:
        """ """
        logma.info("Tab has Focus")
        super().focusInEvent(event)
        return self

    def focusOutEvent(self, event) -> Any:
        """ """
        logma.info("Tab lost Focus")
        super().focusOutEvent(event)
        return self

    def get_drop_position(self, pos) -> Union[Any, int]:
        """Calculate the drop position based on mouse position."""
        tab_index = self.tabBar().tabAt(pos)
        if tab_index == -1:
            return -1
        tab_rect = self.tabBar().tabRect(tab_index)
        if pos.x() < tab_rect.center().x():
            return tab_index
        else:
            return tab_index + 1

    def get_tab_widget(self, tabn) -> Any:
        """"""
        tabW = next(self.app.model.store.docs["dbc"].read(tabn))
        return tabW

    def handle_successful_drag(self) -> None:
        """Handle cleanup after successful drag operation."""
        pass

    def load_journal(self) -> None:
        logma.info(f"load_journal called")
        return self

    def load_toolbox(self) -> Any:
        """"""
        position = 0
        if self.app.toolbox is not None:
            position = self.app.toolbox.position
            if position is None:
                position = 0
            self.app.view.panes["right"].removeTab(position)
        cfg = self.config.dikt.get("toolbox", {})
        logma.info(f"Create Toolbox")
        self.app.toolbox = self.create_toolbox(self, cfg)
        logma.info(f"Initialize Toolbox")
        self.app.toolbox.initWidget()
        self.app.toolbox.position = position
        logma.info(f"Toolbox Position {position}")
        self.app.view.panes["right"].insertTab(position, self.app.toolbox, "ToolBox")
        self.app.view.panes["right"].setCurrentIndex(self.app.toolbox.position if self.app.toolbox else 0)
        return self

    def mousePressEvent(self, event) -> Any:
        """ """
        logma.info(f"Mouse Press Event {event.button()}")
        if event.button() == pyqt.Qt.RightButton:
            pass
        if event.button() == pyqt.Qt.LeftButton:
            tab_index = self.tabBar().tabAt(event.pos())
            if tab_index >= 0:
                self.drag_start_position = event.position().toPoint()
                self.dragged_tab_index = tab_index
        super().mousePressEvent(event)
        return self

    def mouseMoveEvent(self, event) -> None:
        """Handle mouse move events to start drag operation."""
        super().mouseMoveEvent(event)
        try:
            if not event.buttons() & pyqt.Qt.LeftButton:
                return
            move_distance = (event.position().toPoint() - self.drag_start_position).manhattanLength()
            if move_distance < pyqt.QApplication.startDragDistance():
                return
            if self.drag_start_position is None:
                self.drag_start_position = event.position().toPoint()
            if not event.buttons() & pyqt.Qt.LeftButton:
                self.drag_start_position = None
                return
            if (
                event.position().toPoint() - self.drag_start_position
            ).manhattanLength() < pyqt.QApplication.startDragDistance():
                self.drag_start_position = None
                logma.info(f"Mouse Move Event {event.button()}")
                return
            tab_index = self.tabBar().tabAt(self.drag_start_position)
            logma.info(f"Tab Index {tab_index}")
            if tab_index < 0:
                self.drag_start_position = None
                return
            self.start_drag(tab_index)
        except Exception as e:
            logma.warning(e)

    def on_tab_focus(self, tabn=None) -> Any:
        """"""
        self.set_focus(tabn)
        return self

    def on_tab_bar_clicked(self, event) -> Any:
        logma.info(f"on_tab_bar_clicked event received")
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_tab_bar_clicked_double(self, event) -> Any:
        logma.info(f"on_tab_bar_clicked_double event received")
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def on_tab_changed(self, index) -> Any:
        """Ensure proper size and position updates when tab is changed."""
        if self.model.current_tab_has_changed is True:
            self.model.save_tab()
        self.adjustSize()
        self.resize(self.sizeHint())
        self.setFixedSize(self.size())
        return self

    def start_drag(self) -> None:
        """Initialize and execute the drag operation."""
        if self.dragged_tab_index == -1:
            return
        widget = self.widget(self.dragged_tab_index)
        tab_text = self.tabText(self.dragged_tab_index)
        tab_icon = self.tabIcon(self.dragged_tab_index)
        tab_tooltip = self.tabToolTip(self.dragged_tab_index)
        mime_data = pyqt.QMimeData()
        tab_data = {
            "text": tab_text,
            "tooltip": tab_tooltip,
            "source_widget": id(self),
            "tab_index": self.dragged_tab_index,
        }
        mime_data.setText(str(tab_data))
        pixmap = self.create_drag_pixmap(tab_text, tab_icon)
        drag = pyqt.QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(pixmap)
        drag.setHotSpot(pyqt.QPoint(pixmap.width() // 2, pixmap.height() // 2))
        # Execute the drag and capture the user's drop action.  The
        # drag.exec_() call blocks until the user drops the tab (or
        # cancels).  When the drop action is ``MoveAction``, the tab
        # has been successfully moved to its new position.
        drop_action = drag.exec_(pyqt.Qt.MoveAction | pyqt.Qt.CopyAction)
        if drop_action == pyqt.Qt.MoveAction:
            self.handle_successful_drag()

    def reconnect_tabs(self) -> Any:
        """"""
        self.currentChanged.disconnect(self.on_tab_focus)
        self.currentChanged.connect(self.on_tab_focus)
        return self

    def refreshTabSet(self) -> Any:
        """Get data from the model via the chunker by passing it various
        configurations given the selected node and tabset position
        ex. nodeid: 2, position: center -> tabset
        """
        self.model.src.load()
        return self

    def remove_tab(self, tabn) -> Any:
        """"""
        self.removeTab(tabn)
        del self.model.tab_widgets[tabn]
        self.update()
        self.app.view.refresh_window_size()
        return self

    def removeTab(self, index) -> Any:
        """"""
        self.blockSignals(True)
        super().removeTab(index)
        self.blockSignals(False)
        return self

    def save(self) -> Any:
        logma.info(f"save called")
        return self

    def set_active_tab(self, tabset) -> Any:
        logma.info(f"set_active_tab called")
        if hasattr(self, "active_tab"):
            logma.info(f"  has active_tab attr")
        return self

    def set_focus(self, tabn=None) -> Any:
        """
        :param tabn: Tab Number to show when a tab gets selected for focus
        :return:
        need to store each pull of data? this will be the only way to get a usage number
        could keep track in the cache and only store it on end or some other pause point
        this leave the possibility of losses but will be more efficent
        """
        logma.info(f"On Tab Focus {self.pane_position}")
        if self.model.current_tab is not None:
            self.defocus()
        if tabn is None:
            tabn = self.currentIndex()
        if tabn > len(self.model.tabsdata) or tabn < 0 or tabn is None:
            tabn = 0
        if tabn == len(self.model.tab_widgets):
            logma.info(f"Creating New Tab {tabn}")
            tabW = self.model.new_document
        else:
            tabW = self.model.tab_widgets[tabn]
        logma.info(f"Tab Position {tabn}")
        logma.info(f"tabW {tabW}")
        if tabW is None:
            return self
        if tabW.dummy is True:
            self.model.load_tab(self.model.tabsdata[tabn], tabn, self.pane_position, tabn)
            tabW = self.model.tab_widgets[tabn]
        if tabW is not None:
            if hasattr(tabW, "widget_initialized") is False or tabW.widget_initialized is False:
                logma.info(f"Initializing Tab {tabn} for Position {self.pane_position}")
                tabW.initWidget()
                logma.info(f"Widget Initialized")
            tabW.pos = tabn
            self.model.current_tab = tabW
        if self.pane_position == "center":
            self.app.active_tab = self.model.current_tab
            logma.info(f"Load Journal")
            self.load_journal()
            logma.info(f"Load Toolbox")
        logma.info(f"Finish Tab Focus")
        return self

    def showEvent(self, event) -> Any:
        logma.info(f"showEvent called")
        return self

    def start_drag(self, index) -> Any:
        """Start dragging the tab."""
        logma.info(f"Start Drag {index}")
        tab_text = self.tabText(index)
        tab_widget = self.widget(index)
        mime_data = pyqt.QMimeData()
        mime_data.setText(tab_text)
        mime_data.setData("application/x-tab-index", str(index).encode())
        drag = pyqt.QDrag(self)
        drag.setMimeData(mime_data)
        pixmap = self.tabBar().grab()
        painter = pyqt.QPainter(pixmap)
        painter.setCompositionMode(pyqt.QPainter.CompositionMode_DestinationIn)
        painter.fillRect(pixmap.rect(), pyqt.Qt.transparent)
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(pyqt.QPoint(pixmap.width() // 2, pixmap.height() // 2))
        drop_action = drag.exec(pyqt.Qt.MoveAction)
        return self

    def dragEnterEvent(self, event) -> Any:
        if event.mimeData().hasFormat("application/x-tab-index"):
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)
        return self

    def dragMoveEvent(self, event) -> Any:
        """"""
        if event.mimeData().hasFormat("application/x-tab-index"):
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)
        return self

    def dropEvent(self, event) -> Any:
        """"""
        self.drag_start_position = None
        logma.info(f"Drop Event {event}")
        if not event.mimeData().hasFormat("application/x-tab-index"):
            super().dropEvent(event)
            return
        source_index = int(event.mimeData().data("application/x-tab-index").data().decode())
        target_index = self.tabBar().tabAt(event.position().toPoint())
        if target_index < 0:
            target_index = self.count()
        if source_index == target_index:
            event.ignore()
            return
        self.move_tab(source_index, target_index)
        event.acceptProposedAction()
        return self

    def move_tab(self, from_index, to_index) -> Any:
        """Move a tab from one position to another."""
        logma.info(f"Move Tab {from_index} to {to_index}")
        if from_index == to_index:
            return
        widget = self.widget(from_index)
        text = self.tabText(from_index)
        icon = self.tabIcon(from_index)
        tooltip = self.tabToolTip(from_index)
        self.removeTab(from_index)
        if from_index < to_index:
            to_index -= 1
        new_index = self.insertTab(to_index, widget, icon, text)
        self.setTabToolTip(new_index, tooltip)
        self.model.update_position(from_index, to_index)
        self.setCurrentIndex(new_index)
        return self

    def update(self) -> Any:
        """"""
        super().update()
        self.app.view.refresh_window_size()
        return self
