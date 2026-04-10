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
import json as j
import math

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import pyqt
from ogma.logma import Logma
from condor.utils import thingify
from nchantrs.utilities.utils import lookup
from nchantrs.widgets.controls.menus import NchantdMenu, NchantdContextMenu
from pyffice.items.colors import PyfficeColor

# ====================================================================================================================||
here = join(dirname(__file__), "")
debug = True
log = False
logma = Logma(__name__)
if not log:
    logma.off()

# ====================================================================================================================||
pxcfg = join(abspath(here), "_data_", "widgets.yaml")


class NchantdAction(object):
    """"""

    def __init__(self, action_term, code_group="base", parent=None, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("NchantdAction").override(cfg)
        self.app = None
        # logma.info(f"Action {parent}")
        if parent is not None:
            self.parent = parent
            self.app = self.parent.app
        self.action = self.lookup_action(action_term, code_group)

    def get_lookup_code(self):
        """"""
        return self.action["lookup_code_txt"]

    def get_name(self):
        """"""
        return self.action["name_txt"]

    def get_description(self):
        """"""
        return self.action["description_ltxt"]

    def get_UUID(self):
        """"""
        return self.action["UUID"]

    def get_icon(self):
        """"""
        return self.action["icon_txt"]

    def get_short_cut(self):
        """"""
        return self.action["short_cut_txt"]

    def get_tip(self):
        """"""
        return self.action["tip_txt"]

    def get_advanced_tip(self):
        """"""
        return self.action["advanced_tip_ltxt"]

    def get_widget(self):
        """"""
        return self.action["widget"]

    def get_parameters(self):
        """"""
        return j.loads(self.action.get("parameters_dict", "{}").replace("'", '"').strip())

    def lookup_action(self, action_term, code_group="base"):
        """"""
        return lookup(self.app, action_term, {"code_group": code_group})


class NchantdWidgetMixin(object):
    """"""

    def init_variables(self):
        """"""
        self.app = None
        # First, try to get app from parent directly (most reliable)
        if self.parent is not None and hasattr(self.parent, "app"):
            self.app = self.parent.app
        # Traverse parent chain to find the Nchantrs application (NchantdCape or NchantdCloak)
        # This handles both simple dialogs (distortion) and complex apps (nchantment)
        if self.parent is not None:
            current = self.parent
            visited = set()  # Prevent infinite loops in case of circular references
            while current is not None:
                # Prevent infinite loops by tracking visited objects
                current_id = id(current)
                if current_id in visited:
                    break
                visited.add(current_id)

                # Check if parent is the actual application widget
                # The top-level application will have these specific attributes:
                # - model: the main application model (not a tree model)
                # - app: reference to self (for the main app)
                # - view: the main view
                # - new_application: app-specific attribute
                if (
                    hasattr(current, "model")
                    and hasattr(current, "app")
                    and hasattr(current, "view")
                    and hasattr(current, "new_application")
                ):
                    # Make sure it's not a model object (models don't have 'view')
                    if not hasattr(current, "rowCount"):  # QStandardItemModel has rowCount
                        self.app = current
                        break
                # Move up the parent chain
                current = getattr(current, "parent", None)
        self.action = None
        self.changed = False
        self.context_menu = None
        self.context_menu_name = "context"
        self.handler = None
        self.max_width = None
        self.max_height = None
        self.min_width = None
        self.min_height = None
        self.name = None
        self.toolbox_config = None
        self.widget_initialized = False
        # logma.info(f"Initialize Variables {type(self)}")
        return self

    def initModel(self, objects=None, get_actions=True):
        """"""
        # logma.info("Mixin Model")
        self.init_variables()
        # logma.info(f"Initialize Context Menu")
        if self.context_menu_name is not None:
            if getattr(self, "context_menu", None) is not None:
                if self.parent.context_menu is not None:
                    self.context_menu = self.parent.context_menu
            else:
                self.initialize_context_menu(self.context_menu_name)
        action = None
        if get_actions:
            action = self.config.dikt.get("action", None)
        if action:
            self.action = NchantdAction(action, "base", self)
            self.config.override(self.action.action)
        self.widget_dstruct_initialized = True
        # self.app.model.store.store_app_event("initialize", "widget_model_initialization")
        # self.initTriggers()
        return self

    def initView(self, cfg={}):
        """"""
        # logma.info(f"Initialize View")
        self.config.override(cfg)
        if self.config.dikt.get("layout", None) == "horizontal":
            # logma.info("Set Horizontal Layout")
            self.layout = pyqt.QHBoxLayout()
        elif self.config.dikt.get("layout", None) == "grid":
            # logma.info("Set Grid Layout")
            self.layout = pyqt.QGridLayout()
        else:
            # logma.info("Set Vertical Layout")
            self.layout = pyqt.QVBoxLayout()
        self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop | pyqt.Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.layout)
        # self._set_alignment()
        # self.app.model.store.store_app_event("initialize", "widget_view_initialization")
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)
        self.widget_initialized = True
        return self

    def accpet(self):
        """"""
        return self

    def initialize_context_menu(self, menu_name=None):
        """"""
        if menu_name is None:
            menu_name = self.context_menu_name
        # logma.info(f"Initialize Context Menu Name {menu_name}")

        # Guard against missing .app.model by checking if we have a proper app
        if hasattr(self, "app") and hasattr(self.app, "model") and hasattr(self.app.model, "get_menu"):
            try:
                menu_df = self.app.model.get_menu(menu_name)
                # logma.info(f"Initialize Context Menu Data {menu_df}")
                cfg = {"actions": {}}
                if not menu_df.empty:
                    cfg = {"actions": menu_df.to_dict("records")}
            except Exception as e:
                logma.warning(f"Failed to load menu '{menu_name}': {e}")
                cfg = {"actions": {}}
        else:
            logma.warning(f"No app model available for context menu")
            cfg = {"actions": {}}

        # logma.info(f"Initialize Context Menu {cfg.get('actions', {})}")
        self.context_menu = NchantdContextMenu(self, cfg).initWidget()
        return self

    # def initialize_context_menu(self, menu_name=None):
    #     """"""
    #     if menu_name is None:
    #         menu_name = self.context_menu_name
    #     logma.info(f"Initialize Context Menu Name {menu_name}")
    #     menu_df = self.parent.app.model.get_menu(menu_name)
    #     logma.info(f"Initialize Context Menu Data {menu_df}")
    #     cfg = {"actions": {}}
    #     if not menu_df.empty:
    #         cfg = {"actions": menu_df.to_dict("records")}
    #     logma.info(f"Initialize Context Menu {cfg["actions"]}")
    #     self.context_menu = NchantdContextMenu(self, cfg).initWidget()
    #     return self

    def contextMenuEvent(self, event):
        """"""
        logma.info(f"execute contextMenuEvent {self}")
        logma.info(f"Context Menu {self.context_menu}")
        # if self.context_menu is None:
        self.initialize_context_menu()
        logma.info(f"execute contextMenuEvent {self.context_menu.menu_data}")
        self.context_menu.exec(event.globalPos())
        return self

    def cmd_copy_selection(self, selection=""):
        """"""
        return self

    def cmd_cut_selection(self, selection=""):
        """"""
        return self

    def cmd_delete_selection(self, selection=""):
        """"""
        return self

    def cmd_paste_selection(self, selection=""):
        """"""
        return self

    def cmd_paste_selection_formatting(self, selection=""):
        """"""
        return self

    def cmd_paste_selection_formula(self, selection=""):
        """"""
        return self

    def cmd_paste_selection_values(self, selection=""):
        """"""
        return self

    def cmd_set_bold(self, selection=""):
        fmt = self.editor.currentCharFormat()
        if fmt.fontWeight() > pyqt.QFont.Normal:
            fmt.setFontWeight(pyqt.QFont.Normal)
        else:
            fmt.setFontWeight(pyqt.QFont.Bold)
        self.editor.setCurrentCharFormat(fmt)
        return self

    def cmd_set_file_path(self, path):
        """"""
        if path is None:
            path = self.config.dikt.get("path", None)
        self.file_path = path
        return self

    def cmd_set_font(self, selection=""):
        """"""
        return self

    def cmd_set_font_color(self, selection=""):
        """"""
        color = pyqt.QColorDialog.getColor()
        fmt = self.editor.currentCharFormat()
        fmt.setForeground(pyqt.QColor(color))
        self.editor.setCurrentCharFormat(fmt)
        return self

    def cmd_set_italic(self, selection=""):
        """"""
        fmt = self.editor.currentCharFormat()
        fmt.setFontItalic(not fmt.fontItalic())
        self.editor.setCurrentCharFormat(fmt)
        return self

    def cmd_set_underline(self, selection=""):
        fmt = self.editor.currentCharFormat()
        fmt.setFontUnderline(not fmt.fontUnderline())
        self.editor.setCurrentCharFormat(fmt)
        return self

    def cmd_set_background_color(self, selection=""):
        """"""
        return self

    def cmd_set_highlight_color(self, selection=""):
        """"""
        return self

    def cmd_set_number_format(self, selection=""):
        """"""
        return self

    def cmd_set_text_format(self, selection=""):
        """"""
        return self

    def cmd_set_size(self, selection=""):
        """"""
        return self

    def cmd_set_superscript(self, selection=""):
        """"""
        return self

    def cmd_set_subscript(self, selection=""):
        """"""
        return self

    def cmd_set_strikeout(self, selection=""):
        fmt = self.editor.currentCharFormat()
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())
        self.editor.setCurrentCharFormat(fmt)
        return self

    def defocus(self):
        """"""
        return self

    def focusInEvent(self, event):
        super().focusInEvent(event)
        logma.info(f"Focus In")
        return self

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        logma.info(f"Focus Out")
        return self

    def getAlignment(self, justify):
        """"""
        justify = justify.lower()
        if justify == "left":
            return pyqt.Qt.AlignmentFlag.AlignLeft
        elif justify == "center":
            return pyqt.Qt.AlignmentFlag.AlignCenter
        elif justify == "right":
            return pyqt.Qt.AlignmentFlag.AlignRight
        elif justify == "top":
            return pyqt.Qt.AlignmentFlag.AlignTop
        elif justify == "bottom":
            return pyqt.Qt.AlignmentFlag.AlignBottom
        elif justify == "top_left":
            return pyqt.Qt.AlignmentFlag.AlignTop | pyqt.Qt.AlignmentFlag.AlignLeft

    def get_viewport_size(self):
        """"""
        return self

    def keyPressEvent(self, event):
        """Exit fullscreen mode when ESC key is pressed."""
        if self.isFullScreen() and event.key() in {27}:  # ESC key
            self.showNormal()
        super().keyPressEvent(event)
        return self

    def mousePressEvent(self, event):
        """"""
        logma.info("Mouse Press Event")
        if event.button() == pyqt.Qt.MouseButton.LeftButton:
            # self.clicked.emit()
            self.onLeftClick(event)
        elif event.button() == pyqt.Qt.MouseButton.RightButton:
            self.onRightClick(event)
        elif event.button() == pyqt.Qt.MouseButton.MiddleButton:
            self.onMiddleClick(event)
        else:
            pass
        super().mousePressEvent(event)
        return self

    def on_widget_changed(self):
        """"""
        self.app.model.has_changed = True
        return self

    def onLeftClick(self, signal=None):
        """"""
        logma.info(f"Left Click {signal}")
        logma.info(f"Left Click")
        return self

    def onRightClick(self, signal=None):
        """ """
        logma.info(f"Right Click")
        return self

    def onExpand(self):
        """ """
        return self

    def onLeftDoubleClick(self, signal):
        logma.info(f"Left Double Click")
        return self

    def onMiddleClick(self, signal=None):
        """ """
        logma.info(f"Middle Click")
        return self

    def onSelection(self, fx, mod=None):
        """On selection of tree node load data for tabs in center widget"""
        event.on_clickleft_press(fx)

        return

    def onDeselection(self, fx, mod=None):
        """On deslection of tree node save any changes to node options"""
        event.on_clickleft_release(fx)
        return

    def onEnter(self, fx, mod=None):
        """Need to build if a node was selected an enter create a new sibling
        node. shift-enter creates a new child node, ctrl-enter creates
        a new tab in the node"""
        event.on_enter_kp(fx, mod)
        return

    def onDelete(self, fx, mod=None):
        """Launch Dialog to confirm deletion of node, which marks as deleted in database
        and is not removed until a database cleanup is run"""

    def reject(self):
        """"""
        return self

    def run_size_control(self):
        """"""
        return self

    def save(self, *args, **kwargs):
        """"""
        # params = {}
        # cfg = {}
        # self.app.model.store.write(params, cfg)
        return self

    def set_background(self, color=None, hex=None):
        """"""
        logma.info(f"Set Background {color} {hex}")
        if color is not None:
            cfg = {"unit": {"color": color}}
            color = PyfficeColor(cfg).load_unit()
        if hex is not None:
            cfg = {"unit": {"hex": hex}}
            color = PyfficeColor(cfg).load_unit()

        logma.info(f"Set Background {color.get_hex()}")
        self.setStyleSheet(f"background-color: {color.get_hex()}; color: {color.calculate_text_color()}")
        return self

    def set_font(self):
        """"""
        if self.config.dikt.get("font", None):
            font_cfg = self.config.dikt.get("font")
            font = pyqt.QFont(font_cfg.get("type", ""), font_cfg.get("size", ""), pyqt.QFont.Bold)
        else:
            type_ = ""
            size_ = ""
            bold_ = ""
            font = pyqt.QFont(type_, size_, bold_)
        self.setFont(font)
        return self

    def set_changed(self):
        """"""
        self.changed = True
        return self

    def set_handler(self, handler=None, params=None):
        """"""
        self.handler = handler
        return self

    def set_size(self, set_width=None, set_height=None, min_width=10, min_height=10, max_width=None, max_height=None):
        """"""
        # logma.info(f"Set Size {set_width} {set_height} {min_width} {min_height} {max_width} {max_height}")
        self._set_width(set_width, min_width, max_width)
        self._set_height(set_height, min_height, max_height)
        self.updateGeometry()
        return self

    def change_label_text(self, label):
        """Change text of label"""
        label.setText("Text changed!")

    def change_label_color(self, label):
        """Change color of label"""
        label.setStyleSheet("color: red; background-color: yellow;")

    def change_button_style(self, button):
        """Change style of button"""
        button.setStyleSheet("background-color: lightblue; border: 2px solid blue;")

    def _set_alignment(self):
        """"""
        if self.config.dikt.get("justify", None) is not None:
            justify = self.config.dikt.get("justify")
            if justify == "left":
                self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignLeft)
            elif justify == "right":
                self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignRight)
            elif justify == "top":
                self.layout.setAlignmnet(pyqt.Qt.AlignmentFlag.AlignTop)
            elif justify == "bottom":
                self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignBottom)
            elif justify == "top_left":
                self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop | pyqt.Qt.AlignmentFlag.AlignLeft)
            elif justify == "top_right":
                self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignRight | pyqt.Qt.AlignmentFlag.AlignTop)
            elif justify == "bottom_left":
                self.layout.setAlignmnet(pyqt.Qt.AlignmentFlag.AlignBottom | pyqt.Qt.AlignmentFlag.AlignLeft)
            elif justify == "bottom_right":
                self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignBottom | pyqt.Qt.AlignmentFlag.AlignRight)
        return self

    def _set_width(self, set_width=None, min_width=None, max_width=None):
        """"""
        if set_width == "auto":
            return self
        if min_width is None:
            min_width = 10
        min_width = int(min_width)
        if min_width < 15:
            min_width = 15
        if set_width is None:
            size = self.config.dikt.get("size", None)
            if isinstance(size, list):
                set_width = size[0]
            if set_width == "auto":
                return self
            # logma.info(f"Set Width {set_width} Min {min_width}")
            if set_width is None:
                set_width = min_width
        # logma.info(f"Set Width {set_width} Min {min_width}")
        if set_width != min_width:
            min_width = set_width
        if max_width is None:
            max_width = set_width
        if max_width is None:
            max_width = min_width * 1.5
        self.min_width = min_width
        self.max_width = max_width
        # logma.info(f"Set Width {self.min_width} {self.max_width}")
        if isinstance(self.max_width, str):
            return self
        # logma.info(f"Set Width {self.min_width} {self.max_width}")
        self.setMinimumWidth(self.min_width)
        # Don't set maximum width to allow expansion
        # self.setMaximumWidth(self.max_width)
        return self

    #
    # def _set_height(self, set_height=None, min_height=None, max_height=None):
    #     """"""
    #     # logma.off()
    #     # logma.info(f"Set Height {set_height} Min {min_height} Max {max_height}")
    #     # logma.info(f"Current Height {self.min_height} {self.max_height} {set_height}")
    #     # logma.info(f"Current Height {self.size().height()}")
    #     if set_height == "auto":
    #         return self
    #     if min_height is None:
    #         min_height = 10
    #     min_height = int(min_height)
    #     if min_height < 15:
    #         min_height = 15
    #     if set_height is None:
    #         size = self.config.dikt.get("size", None)
    #         if isinstance(size, list):
    #             set_height = size[1]
    #         if set_height == "auto":
    #             current_height = self.size().height()
    #             # logma.info(f"Current Height {current_height}")
    #             if current_height >= min_height:
    #                 return self
    #         # logma.info(f"Set Height {set_height} Min {min_height}")
    #         if set_height is None:
    #             set_height = min_height
    #
    #     # logma.info(f"Set Height {set_height} Min {min_height}")
    #     # if set_height != min_height:
    #     #     min_height = set_height
    #
    #     if min_height is None:
    #         min_height = set_height
    #     self.min_height = min_height
    #
    #     if max_height is None:
    #         max_height = set_height
    #     if max_height is None:
    #         max_height = min_height * 1.5
    #     self.max_height = max_height
    #     # logma.info(f"Set Height {self.min_height} {self.max_height}")
    #     if isinstance(self.min_height, str):
    #         return self
    #     self.setMinimumHeight(self.min_height)
    #     # Don't set maximum height to allow expansion
    #     # if isinstance(self.max_height, str):
    #     #     return self
    #     # self.setMaximumHeight(self.max_height)
    #     # logma.off()
    #     return self

    def _set_height(self, set_height=None, min_height=None, max_height=None):
        """"""
        # logma.off()
        # logma.info(f"Set Height {set_height} Min {min_height} Max {max_height}")
        # logma.info(f"Current Height {self.min_height} {self.max_height} {set_height}")
        # logma.info(f"Current Height {self.size().height()}")
        if set_height == "auto":
            return self
        if min_height is None:
            min_height = 10
        min_height = int(min_height)
        if min_height < 15:
            min_height = 15
        if set_height is None:
            size = self.config.dikt.get("size", None)
            if isinstance(size, list):
                set_height = size[1]
            if set_height == "auto":
                current_height = self.size().height()
                # logma.info(f"Current Height {current_height}")
                if current_height >= min_height:
                    return self
            # logma.info(f"Set Height {set_height} Min {min_height}")
            if set_height is None:
                set_height = min_height

        # logma.info(f"Set Height {set_height} Min {min_height}")
        # if set_height != min_height:
        #     min_height = set_height

        if min_height is None:
            min_height = set_height
        self.min_height = min_height

        if max_height is None:
            max_height = set_height
        if max_height is None:
            max_height = min_height * 1.5
        self.max_height = max_height
        # logma.info(f"Set Height {self.min_height} {self.max_height}")
        if isinstance(self.min_height, str):
            return self
        self.setMinimumHeight(self.min_height)

        # Check if parent is a grid layout with stretch factors set
        # This allows buttons to expand in calculators while maintaining constraints elsewhere
        should_expand = self._should_expand_in_layout()

        if isinstance(self.max_height, str):
            return self

        if not should_expand:
            self.setMaximumHeight(self.max_height)
        # logma.off()
        return self

    def _should_expand_in_layout(self):
        """Check if this widget should expand to fill available space in its layout"""
        try:
            # Check if parent has a layout
            if hasattr(self, "parent") and self.parent is not None:
                parent_layout = self.parent.layout if hasattr(self.parent, "layout") else None

                # Check if it's a grid layout with stretch factors
                if parent_layout is not None and isinstance(parent_layout, pyqt.QGridLayout):
                    # Check if any rows or columns have stretch factors > 0
                    for row in range(parent_layout.rowCount()):
                        if parent_layout.rowStretch(row) > 0:
                            return True
                    for col in range(parent_layout.columnCount()):
                        if parent_layout.columnStretch(col) > 0:
                            return True
        except Exception:
            pass

        return False

    # def _set_height(self, set_height=None, min_height=None, max_height=None):
    #     """"""
    #     # logma.off()
    #     # logma.info(f"Set Height {set_height} Min {min_height} Max {max_height}")
    #     # logma.info(f"Current Height {self.min_height} {self.max_height} {set_height}")
    #     # logma.info(f"Current Height {self.size().height()}")
    #     if set_height == "auto":
    #         return self
    #     if min_height is None:
    #         min_height = 10
    #     min_height = int(min_height)
    #     if min_height < 15:
    #         min_height = 15
    #     if set_height is None:
    #         size = self.config.dikt.get("size", None)
    #         if isinstance(size, list):
    #             set_height = size[1]
    #         if set_height == "auto":
    #             current_height = self.size().height()
    #             # logma.info(f"Current Height {current_height}")
    #             if current_height >= min_height:
    #                 return self
    #         # logma.info(f"Set Height {set_height} Min {min_height}")
    #         if set_height is None:
    #             set_height = min_height
    #
    #     # logma.info(f"Set Height {set_height} Min {min_height}")
    #     # if set_height != min_height:
    #     #     min_height = set_height
    #
    #     if min_height is None:
    #         min_height = set_height
    #     self.min_height = min_height
    #
    #     if max_height is None:
    #         max_height = set_height
    #     if max_height is None:
    #         max_height = min_height * 1.5
    #     self.max_height = max_height
    #     # logma.info(f"Set Height {self.min_height} {self.max_height}")
    #     if isinstance(self.min_height, str):
    #         return self
    #     self.setMinimumHeight(self.min_height)
    #     if isinstance(self.max_height, str):
    #         return self
    #     self.setMaximumHeight(self.max_height)
    #     # logma.off()
    #     return self

    def _get_text_size(self, text):
        """

                font = pyqt.QFont(self.config.dikt["font"]["type"], self.config.dikt["font"]["size"])
        fm = pyqt.QFontMetrics(font)
        text_width = fm.horizontalAdvance(self.config.dikt.get("text", "Default Option"))
        if text_width > width < max_width:
            width = text_width
        if self.config.dikt["size"]:
            if isinstance(self.config.dikt["size"], int):
                width = self.config.dikt["size"]

        :param text:
        :return:
        """
        fm = pyqt.QFontMetrics(self.font())
        height = fm.height()
        min_height = 10
        if height > min_height:
            min_height = height * 1.05
        width = fm.horizontalAdvance(str(text))
        # logma.info(f"Width {width} Height {height}")
        min_width = 10
        if width > min_width:
            min_width = width * (1.4 - (0.5 * width**0.8) / 100)
        return int(min_width), int(min_height)

    def _set_widget_size(self, size=None):
        """"""
        min_height = 25
        cfg = {"size": [0, 0]}
        if size:
            cfg["size"][0] = size[0]
            cfg["size"][1] = size[1]
        else:
            entry_config = self.config.dikt.get("entry", None)
            logma.info(f"Entry {entry_config}")
            if entry_config.get("default_text", None) and self.value:
                entry_config["default_text"] = self.value
            size = self._get_text_size(entry_config.get("default_text", "Place entry text here."))
            logma.info(f"Size {size}")
            if entry_config.get("style", None):
                cfg["size"][1] = min_height
                self.style = "single"
                if entry_config.get("style", None) == "double":
                    cfg["size"][1] = cfg["size"][1] * 2
                    self.style = "double"
                elif entry_config.get("style", None) == "paragraph":
                    cfg["size"][1] = cfg["size"][1] * 5
                    self.style = "paragraph"
                elif entry_config.get("style", None) == "column":
                    cfg["size"][1] = min_height
                    self.style = "column"
                elif entry_config.get("style", None) == "row":
                    cfg["size"][1] = min_height
                    self.style = "row"
                elif entry_config.get("style", None) == "half_page":
                    cfg["size"][1] = min_height
                    self.style = "half_page"
                elif entry_config.get("style", None) == "page":
                    cfg["size"][1] = min_height
                    self.style = "page"
        return cfg

    def __getstate__(self):
        """"""
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        if state.get("unpickable_attribute", False):
            del state["unpicklable_attribute"]
        return state

    def __setstate__(self, state):
        """"""


class NchantdWidget(NchantdWidgetMixin, pyqt.QWidget):
    """"""

    # NOTE: Mixin comes before QWidget in MRO, but we must call QWidget.__init__ directly
    # to ensure Qt initialization. The mixin provides application logic, QWidget provides
    # the Qt widget functionality. Using super().__init__() would skip QWidget init.

    def __init__(self, parent=None, cfg=None):
        """ """
        # Explicitly call QWidget.__init__ to ensure proper Qt initialization
        # This fixes: RuntimeError: libshiboken: 'init' method of object's base class not called
        pyqt.QWidget.__init__(self)
        self.config = condor.Instruct(pxcfg).select("NchantdWidget")
        # logma.info(f"Init NchantdWidget Config {self.config}")
        self.parent = parent
        self.init_variables()
        self.config.override(cfg)
        self.layout = None

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        if hasattr(self.parent, "context_menu"):
            self.context_menu = self.parent.context_menu
        else:
            self.initialize_context_menu()
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

    def initTriggers(self):
        """ """
        logma.info(f"Init Triggers")
        try:
            self.doubleClicked.connect(self.onLeftDoubleClick)
        except Exception as e:
            pass
        try:
            self.expanded.connect(self.onExpand)
        except Exception as e:
            pass
        try:
            self.clicked.connect(self.onLeftClick)
        except Exception as e:
            pass
        return self


class NchantdSideBar(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdSideBar")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdSideBar, self).__init__(self.parent, self.config)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        self.setMaximumWidth(300)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


def buildPane(parent, cfg, offsetcol=0):
    """ """
    expandCFG(cfg)
    for row in cfg["seq"].keys():
        for col, wdgt in cfg["seq"][row].items():
            key = list(wdgt.keys())[0]
            cfg["widget"] = lookupWidget(key)
            widget = loadWidget(parent, cfg)
            parent.layout.addWidget(widget, int(row), int(col) + offsetcol)


def expandCFG(cfg):
    """Expand Configuration Details to all child wigets within config"""
    dcfg = condor.Instruct(pxcfg).select("expandCFG").override(cfg).dikt
    fonts, styles = dcfg["fonts"], dcfg["styles"]
    for row in dcfg["seq"].keys():
        for col, wCFG in dcfg["seq"][row].items():
            widget = list(wCFG.keys())[0]
            cfg["seq"][row][col][widget] = expandFonts(wCFG[widget], fonts)
            cfg["seq"][row][col][widget] = expandStyles(wCFG[widget], styles)
    return cfg


def expandFonts(cfg, fonts):
    """ """
    if "font" in cfg:
        font = cfg["font"]
    else:
        font = "default"
    cfg["font"] = fonts[font]
    return cfg


def expandStyles(cfg, styles):
    """ """
    if "style" in cfg.keys():
        style = cfg["style"]
    else:
        style = "default"
    cfg["style"] = styles[style]
    return cfg


def loadWidget(parent, cfg=None):  # , panestyle=None):
    """Load the defined widget from its parameters or from a list of registered
    widgets
    Load Source for Daynamically building the tabset for the pane"""
    if cfg is None:
        cfg = {}
    cfg = condor.Instruct(pxcfg).override(cfg).dikt
    logma.info(f"Load Widget Config {cfg}")
    if cfg.get("widget", None):
        try:
            # app = cfg.get("app", "nchantrs")
            # logma.info(f"{app}.{cfg['widget']}")
            # widget = thingify(f"{app}.{cfg['widget']}", None, None, True)(parent, cfg)
            logma.info(f"{cfg['widget']}")
            widget = thingify(f"{cfg['widget']}", None, None, True)(parent, cfg)
        except Exception as e:
            logma.info(f"Load Widget Exception {e}")
            # Try fallback apps if specified
            apps = cfg.get("apps", [])
            widget = None
            if apps:  # TODO: not sure if we should keep this process long term
                for app in set(apps):
                    try:
                        logma.info(f"{app}.{cfg['widget']}")
                        widget = thingify(f"{app}.{cfg['widget']}", None, None, True)(parent, cfg)
                        if widget:
                            break
                    except Exception as e:
                        logma.warning(f"{app}.{cfg['widget']}")
                        logma.warning(e)

            if widget is None:
                # No fallback apps or all failed, re-raise the original exception
                logma.warning(f"Failed to load widget: {cfg['widget']}")
                raise
    else:
        registered_widget = lookupWidget(list(cfg.keys())[0])
        widget = condor.Factory.object(registered_widget, parent.app.model.parents)(parent, cfg)
        widget.initWidget(parent.newInstance)
    return widget


def lookupWidget(key):
    """ """
    return condor.Instruct(pxcfg).select("RegisteredWidgets").dikt[key]


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
