from typing import Any, Dict, Tuple

"\n---\n<(META)>:\n    docid:\n    name:\n    description: >\n    version: 0.0.0.0.0.0\n    authority: filesystem\n    security: seclvl2\n    <(WT)>: -32\n"
from os.path import abspath, dirname, join
import datetime as dt
import json as j
import math
from kahndor import kahndor
from nchantrs.libraries import pyqt
from kahndor.logma import Logma
from kahndor.utils import thingify
from nchantrs.themes.colors import NchantdColor
from nchantrs.utilities.utils import lookup
from nchantrs.widgets.controls.menus import NchantdMenu, NchantdContextMenu

here = join(dirname(__file__), "")
debug = True
log = True
logma = Logma(__name__)
if not log:
    logma.off()
pxcfg = join(abspath(here), "_data_", "widgets.yaml")


class NchantdAction(object):
    """"""

    def __init__(self, action_term, code_group="base", parent=None, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select("NchantdAction").override(cfg)
        self.app = None
        if parent is not None:
            self.parent = parent
            self.app = self.parent.app
        self.action = self.lookup_action(action_term, code_group)

    def get_lookup_code(self) -> Any:
        """"""
        return self.action["lookup_code_txt"]

    def get_name(self) -> Any:
        """"""
        return self.action["name_txt"]

    def get_description(self) -> Any:
        """"""
        return self.action["description_ltxt"]

    def get_UUID(self) -> Any:
        """"""
        return self.action["UUID"]

    def get_icon(self) -> Any:
        """"""
        return self.action["icon_txt"]

    def get_short_cut(self) -> Any:
        """"""
        return self.action["short_cut_txt"]

    def get_tip(self) -> Any:
        """"""
        return self.action["tip_txt"]

    def get_advanced_tip(self) -> Any:
        """"""
        return self.action["advanced_tip_ltxt"]

    def get_widget(self) -> Any:
        """"""
        return self.action["widget"]

    def get_parameters(self) -> Any:
        """"""
        return j.loads(self.action.get("parameters_dict", "{}").replace("'", '"').strip())

    def lookup_action(self, action_term, code_group="base") -> Any:
        """"""
        return lookup(self.app, action_term, {"code_group": code_group})


class NchantdWidgetMixin(pyqt.QObject):
    """"""

    def init_variables(self) -> Any:
        """"""
        self.app = None
        self.context_menu_name = "widget"
        if self.parent is not None and hasattr(self.parent, "app"):
            self.app = self.parent.app
        if self.parent is not None:
            current = self.parent
            visited = set()
            while current is not None:
                current_id = id(current)
                if current_id in visited:
                    break
                visited.add(current_id)
                if (
                    hasattr(current, "model")
                    and hasattr(current, "app")
                    and hasattr(current, "view")
                    and hasattr(current, "new_application")
                ):
                    if not hasattr(current, "rowCount"):
                        self.app = current
                        break
                current = getattr(current, "parent", None)
        if debug:
            if self.app is None:
                raise Exception(f"No Parent App {self.parent}")
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
        return self

    def initModel(self, objects=None, get_actions=True) -> Any:
        """"""
        self.init_variables()
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
        return self

    def initView(self, cfg={}) -> Any:
        """"""
        self.config.override(cfg)
        if self.config.dikt.get("layout", None) == "horizontal":
            self.layout = pyqt.QHBoxLayout()
        elif self.config.dikt.get("layout", None) == "grid":
            self.layout = pyqt.QGridLayout()
        else:
            self.layout = pyqt.QVBoxLayout()
        # if not self.config.dikt.get('fill', False):
        #     self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop | pyqt.Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)
        self.widget_initialized = True
        self.initialize_context_menu()
        return self

    def accpet(self) -> Any:
        """Backward-compat alias for `accept` (kept for callers using the typo)."""
        return self.accept()

    def accept(self) -> Any:
        """Accept the dialog — close with Accepted result."""
        try:
            return self.done(getattr(pyqt.QDialog, "Accepted", 1))
        except AttributeError:
            self.close()
            return self

    def initialize_context_menu(self, menu_name=None) -> Any:
        """"""
        if menu_name is None:
            menu_name = self.context_menu_name
        if hasattr(self, "app") and hasattr(self.app, "model") and hasattr(self.app.model, "get_menu"):
            try:
                menu_df = self.app.model.get_menu(menu_name)
                cfg = {"actions": {}}
                if not menu_df.empty:
                    cfg = {"actions": menu_df.to_dict("records")}
            except Exception as e:
                logma.warning(f"Failed to load menu '{menu_name}': {e}")
                if debug:
                    raise e
                cfg = {"actions": {}}
        else:
            logma.warning(f"No app model available for context menu")
            cfg = {"actions": {}}
        self.context_menu = NchantdContextMenu(self, cfg).initWidget()
        return self

    def contextMenuEvent(self, event) -> Any:
        """"""
        self.initialize_context_menu()
        logma.info(f"execute contextMenuEvent {self}")
        logma.info(f"Context Menu {self.context_menu}")
        logma.info(f"execute contextMenuEvent {self.context_menu.menu_data}")
        if debug:
            self.add_developer_menu(self.context_menu)
        self.context_menu.exec(event.globalPos())
        return self

    def developer_info(self) -> Dict[str, Any]:
        """Collect developer-facing metadata about this widget."""
        try:
            rect = self.geometry()
            geo = f"{rect.width()}x{rect.height()} @ ({rect.x()},{rect.y()})"
        except Exception:
            geo = "n/a"
        return {
            "class": type(self).__name__,
            "module": type(self).__module__,
            "name": getattr(self, "name", None),
            "object_name": self.objectName() or None,
            "file_path": getattr(self, "file_path", None),
            "context_menu": getattr(self, "context_menu_name", None),
            "parent": type(self.parent).__name__ if getattr(self, "parent", None) else None,
            "geometry": geo,
        }

    def add_developer_menu(self, menu) -> Any:
        """Append a debug-only 'Developer' submenu exposing widget metadata."""
        info = self.developer_info()
        text = "\n".join((f"{k}: {v}" for k, v in info.items()))
        menu.addSeparator()
        dev = menu.addMenu("🛠 Developer")
        for key, value in info.items():
            row = dev.addAction(f"{key}: {value}")
            row.setEnabled(False)
        dev.addSeparator()
        copy = dev.addAction("Copy widget info")
        copy.triggered.connect(lambda *_: pyqt.QApplication.clipboard().setText(text))
        log_it = dev.addAction("Log widget info")
        log_it.triggered.connect(lambda *_: logma.info(f"[developer] {info}"))
        return self

    def cmd_copy_selection(self, selection="") -> Any:
        """Copy current editor selection to clipboard."""
        editor = getattr(self, "editor", None)
        if editor is not None and hasattr(editor, "copy"):
            editor.copy()
        else:
            pyqt.QApplication.clipboard().setText(selection or "")
        return self

    def cmd_cut_selection(self, selection="") -> Any:
        """Cut current editor selection to clipboard."""
        editor = getattr(self, "editor", None)
        if editor is not None and hasattr(editor, "cut"):
            editor.cut()
        return self

    def cmd_delete_selection(self, selection="") -> Any:
        """Delete current editor selection (preserve formatting if QTextEdit)."""
        editor = getattr(self, "editor", None)
        if editor is not None and hasattr(editor, "textCursor"):
            cursor = editor.textCursor()
            if cursor.hasSelection():
                cursor.removeSelectedText()
                editor.setTextCursor(cursor)
        return self

    def cmd_paste_selection(self, selection="") -> Any:
        """Paste clipboard content into editor at cursor."""
        editor = getattr(self, "editor", None)
        if editor is not None and hasattr(editor, "paste"):
            editor.paste()
        return self

    def cmd_paste_selection_formatting(self, selection="") -> Any:
        """Paste clipboard content WITH source formatting (HTML if available)."""
        editor = getattr(self, "editor", None)
        if editor is not None and hasattr(editor, "paste"):
            clipboard = pyqt.QApplication.clipboard()
            if clipboard.mimeData().hasHtml():
                editor.insertHtml(clipboard.mimeData().html())
            else:
                editor.paste()
        return self

    def cmd_paste_selection_formula(self, selection="") -> Any:
        """Paste clipboard content as a formula string (text only, no formatting)."""
        editor = getattr(self, "editor", None)
        if editor is not None and hasattr(editor, "insertPlainText"):
            clipboard = pyqt.QApplication.clipboard()
            editor.insertPlainText(clipboard.text())
        return self

    def cmd_paste_selection_values(self, selection="") -> Any:
        """Paste clipboard content as plain values (strip formatting markers)."""
        editor = getattr(self, "editor", None)
        if editor is not None and hasattr(editor, "insertPlainText"):
            clipboard = pyqt.QApplication.clipboard()
            text = clipboard.text()
            if text.startswith("="):
                text = text[1:]
            editor.insertPlainText(text)
        return self

    def cmd_set_bold(self, selection="") -> Any:
        fmt = self.editor.currentCharFormat()
        if fmt.fontWeight() > pyqt.QFont.Normal:
            fmt.setFontWeight(pyqt.QFont.Normal)
        else:
            fmt.setFontWeight(pyqt.QFont.Bold)
        self.editor.setCurrentCharFormat(fmt)
        return self

    def cmd_set_file_path(self, path) -> Any:
        """"""
        if path is None:
            path = self.config.dikt.get("path", None)
        self.file_path = path
        return self

    def cmd_set_font(self, selection="") -> Any:
        """Open a font picker dialog and apply the chosen font to the editor selection."""
        editor = getattr(self, "editor", None)
        if editor is None:
            return self
        font, ok = pyqt.QFontDialog.getFont(editor.currentFont(), editor)
        if ok:
            editor.setCurrentFont(font)
        return self

    def cmd_set_font_color(self, selection="") -> Any:
        """"""
        color = pyqt.QColorDialog.getColor()
        fmt = self.editor.currentCharFormat()
        fmt.setForeground(pyqt.QColor(color))
        self.editor.setCurrentCharFormat(fmt)
        return self

    def cmd_set_italic(self, selection="") -> Any:
        """"""
        fmt = self.editor.currentCharFormat()
        fmt.setFontItalic(not fmt.fontItalic())
        self.editor.setCurrentCharFormat(fmt)
        return self

    def cmd_set_underline(self, selection="") -> Any:
        fmt = self.editor.currentCharFormat()
        fmt.setFontUnderline(not fmt.fontUnderline())
        self.editor.setCurrentCharFormat(fmt)
        return self

    def cmd_set_background_color(self, selection="") -> Any:
        """Set the background color of the current selection (highlight)."""
        editor = getattr(self, "editor", None)
        if editor is None:
            return self
        color = pyqt.QColorDialog.getColor()
        if not color.isValid():
            return self
        fmt = editor.currentCharFormat()
        fmt.setBackground(pyqt.QBrush(color))
        editor.setCurrentCharFormat(fmt)
        return self

    def cmd_set_highlight_color(self, selection="") -> Any:
        """Apply a highlighter color to the selection (foreground highlight)."""
        editor = getattr(self, "editor", None)
        if editor is None:
            return self
        color = pyqt.QColorDialog.getColor()
        if not color.isValid():
            return self
        fmt = editor.currentCharFormat()
        fmt.setProperty(pyqt.QTextCharFormat.FullWidthSelection, True)
        fmt.setBackground(pyqt.QBrush(color))
        editor.setCurrentCharFormat(fmt)
        return self

    def cmd_set_number_format(self, selection="") -> Any:
        """Apply a numeric format to the current cell/selection."""
        editor = getattr(self, "editor", None)
        if editor is None:
            return self
        fmt = editor.currentCharFormat()
        fmt.setProperty(pyqt.QTextCharFormat.FontFamily, "monospace")
        editor.setCurrentCharFormat(fmt)
        return self

    def cmd_set_text_format(self, selection="") -> Any:
        """Apply a plain-text format to the current cell/selection."""
        editor = getattr(self, "editor", None)
        if editor is None:
            return self
        fmt = editor.currentCharFormat()
        fmt.setProperty(pyqt.QTextCharFormat.FontFamily, "")
        editor.setCurrentCharFormat(fmt)
        return self

    def cmd_set_size(self, selection="") -> Any:
        """Open a font-size picker and apply the chosen size to the selection."""
        editor = getattr(self, "editor", None)
        if editor is None:
            return self
        sizes = pyqt.QFontDatabase.standardSizes()
        current = editor.currentFont().pointSize() or 10
        size, ok = pyqt.QInputDialog.getInt(editor, "Font Size", "Point size:", current, min(sizes), max(sizes))
        if ok:
            fmt = editor.currentCharFormat()
            fmt.setFontPointSize(size)
            editor.setCurrentCharFormat(fmt)
        return self

    def cmd_set_superscript(self, selection="") -> Any:
        """Toggle superscript alignment on the current selection."""
        editor = getattr(self, "editor", None)
        if editor is None:
            return self
        fmt = editor.currentCharFormat()
        align = fmt.verticalAlignment()
        fmt.setVerticalAlignment(
            pyqt.QTextCharFormat.AlignNormal
            if align == pyqt.QTextCharFormat.AlignSuperScript
            else pyqt.QTextCharFormat.AlignSuperScript
        )
        editor.setCurrentCharFormat(fmt)
        return self

    def cmd_set_subscript(self, selection="") -> Any:
        """Toggle subscript alignment on the current selection."""
        editor = getattr(self, "editor", None)
        if editor is None:
            return self
        fmt = editor.currentCharFormat()
        align = fmt.verticalAlignment()
        fmt.setVerticalAlignment(
            pyqt.QTextCharFormat.AlignNormal
            if align == pyqt.QTextCharFormat.AlignSubScript
            else pyqt.QTextCharFormat.AlignSubScript
        )
        editor.setCurrentCharFormat(fmt)
        return self

    def cmd_set_strikeout(self, selection="") -> Any:
        fmt = self.editor.currentCharFormat()
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())
        self.editor.setCurrentCharFormat(fmt)
        return self

    def defocus(self) -> Any:
        """Release keyboard focus from this widget (clear focus + notify app)."""
        self.clearFocus()
        if getattr(self, "parent", None) is not None and hasattr(self.parent, "setFocus"):
            self.parent.setFocus()
        return self

    def focusInEvent(self, event) -> Any:
        super().focusInEvent(event)
        logma.info(f"Focus In")
        return self

    def focusOutEvent(self, event) -> Any:
        super().focusOutEvent(event)
        logma.info(f"Focus Out")
        return self

    def getAlignment(self, justify) -> Any:
        """"""
        # Preserve original semantics: unknown justify -> implicit None.
        return self._ALIGNMENT_FLAGS.get(justify.lower())

    def get_viewport_size(self) -> Any:
        """Return the viewport size as (width, height) for layout calculations.

        Returns the inner viewport (for scrollable widgets) when one is
        available; falls back to the widget's frame size otherwise.
        """
        viewport = getattr(self, "viewport", None)
        if viewport is not None and hasattr(viewport, "size"):
            size = viewport.size()
        else:
            size = self.size()
        return (size.width(), size.height())

    def keyPressEvent(self, event) -> Any:
        """Exit fullscreen mode when ESC key is pressed."""
        if self.isFullScreen() and event.key() in {27}:
            self.showNormal()
        super().keyPressEvent(event)
        return self

    def mousePressEvent(self, event) -> Any:
        """"""
        logma.info("Mouse Press Event")
        if event.button() == pyqt.Qt.MouseButton.LeftButton:
            self.onLeftClick(event)
        elif event.button() == pyqt.Qt.MouseButton.RightButton:
            self.onRightClick(event)
        elif event.button() == pyqt.Qt.MouseButton.MiddleButton:
            self.onMiddleClick(event)
        else:
            pass
        super().mousePressEvent(event)
        return self

    def on_widget_changed(self) -> Any:
        """"""
        self.app.model.has_changed = True
        return self

    def onLeftClick(self, signal=None) -> Any:
        """"""
        logma.info(f"Left Click {signal}")
        logma.info(f"Left Click")
        return self

    def onRightClick(self, signal=None) -> Any:
        """ """
        logma.info(f"Right Click")
        return self

    def onExpand(self) -> Any:
        """Handle expand event — propagate to app model as a structure change."""
        if getattr(self, "app", None) is not None and hasattr(self.app, "model"):
            self.app.model.has_changed = True
        return self

    def onLeftDoubleClick(self, signal) -> Any:
        logma.info(f"Left Double Click")
        return self

    def onMiddleClick(self, signal=None) -> Any:
        """ """
        logma.info(f"Middle Click")
        return self

    def onSelection(self, fx, mod=None) -> None:
        """On selection of tree node load data for tabs in center widget"""
        event.on_clickleft_press(fx)
        return

    def onDeselection(self, fx, mod=None) -> None:
        """On deslection of tree node save any changes to node options"""
        event.on_clickleft_release(fx)
        return

    def onEnter(self, fx, mod=None) -> None:
        """Need to build if a node was selected an enter create a new sibling
        node. shift-enter creates a new child node, ctrl-enter creates
        a new tab in the node"""
        event.on_enter_kp(fx, mod)
        return

    def onDelete(self, fx, mod=None) -> None:
        logma.info(f"onDelete called")
        return self

    def reject(self) -> Any:
        """Reject the dialog — close with Rejected result."""
        try:
            return self.done(getattr(pyqt.QDialog, "Rejected", 0))
        except AttributeError:
            self.close()
            return self

    def run_size_control(self) -> Any:
        """Apply min/max size policy from config; emit changed if size was forced."""
        min_size = self.config.dikt.get("min_size", None)
        max_size = self.config.dikt.get("max_size", None)
        if isinstance(min_size, (list, tuple)) and len(min_size) == 2:
            self.setMinimumSize(int(min_size[0]), int(min_size[1]))
        if isinstance(max_size, (list, tuple)) and len(max_size) == 2:
            self.setMaximumSize(int(max_size[0]), int(max_size[1]))
        self.updateGeometry()
        return self

    def save(self, *args, **kwargs) -> Any:
        """Persist current widget state via the application store (no-op if no app)."""
        store = None
        if getattr(self, "app", None) is not None and hasattr(self.app, "model") and hasattr(self.app.model, "store"):
            store = self.app.model.store
        if store is None:
            logma.info("save() called without an app store — nothing to persist")
            return self
        params = {"widget_id": getattr(self, "UUID", None)}
        cfg = {}
        try:
            store.write(params, cfg)
        except Exception as e:
            logma.info(f"save() skipped: store.write raised {e!r}")
        return self

    def set_background(self, color=None, hex=None) -> Any:
        """"""
        logma.info(f"Set Background {color} {hex}")
        if color is not None:
            cfg = {"unit": {"color": color, "style": "name"}}
            color = NchantdColor(cfg).load_unit()
        if hex is not None:
            cfg = {"unit": {"color": hex, "style": "hex"}}
            color = NchantdColor(cfg).load_unit()
        logma.info(f"Set Background {color.get_hex()}")
        self.setStyleSheet(f"background-color: {color.get_hex()}; color: {color.calculate_text_color()}")
        return self

    def set_font(self) -> Any:
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

    def set_changed(self) -> Any:
        """"""
        self.changed = True
        return self

    def set_handler(self, handler=None, params=None) -> Any:
        """"""
        self.handler = handler
        return self

    def set_size(
        self, set_width=None, set_height=None, min_width=10, min_height=10, max_width=None, max_height=None
    ) -> Any:
        """"""
        self._set_width(set_width, min_width, max_width)
        self._set_height(set_height, min_height, max_height)
        self.updateGeometry()
        return self

    def change_label_text(self, label) -> None:
        """Change text of label"""
        label.setText("Text changed!")

    def change_label_color(self, label) -> None:
        """Change color of label"""
        label.setStyleSheet("color: red; background-color: yellow;")

    def change_button_style(self, button) -> None:
        """Change style of button"""
        button.setStyleSheet("background-color: lightblue; border: 2px solid blue;")

    _ALIGNMENT_FLAGS = {
        "left": pyqt.Qt.AlignmentFlag.AlignLeft,
        "center": pyqt.Qt.AlignmentFlag.AlignCenter,
        "right": pyqt.Qt.AlignmentFlag.AlignRight,
        "top": pyqt.Qt.AlignmentFlag.AlignTop,
        "bottom": pyqt.Qt.AlignmentFlag.AlignBottom,
        "top_left": pyqt.Qt.AlignmentFlag.AlignTop | pyqt.Qt.AlignmentFlag.AlignLeft,
        "top_right": pyqt.Qt.AlignmentFlag.AlignRight | pyqt.Qt.AlignmentFlag.AlignTop,
        "bottom_left": pyqt.Qt.AlignmentFlag.AlignBottom | pyqt.Qt.AlignmentFlag.AlignLeft,
        "bottom_right": pyqt.Qt.AlignmentFlag.AlignBottom | pyqt.Qt.AlignmentFlag.AlignRight,
    }
    # Lookup table mapping justify string -> Qt alignment flag combo.

    def _set_alignment(self) -> Any:
        """"""
        justify = self.config.dikt.get("justify", None)
        flag = self._ALIGNMENT_FLAGS.get(justify)
        if flag is not None:
            self.layout.setAlignment(flag)
        return self

    def _set_width(self, set_width=None, min_width=None, max_width=None) -> Any:
        """"""
        # Resolve set_width: 'auto' short-circuits; otherwise pick from size or fallback.
        if set_width is None:
            size = self.config.dikt.get("size", None)
            if isinstance(size, list):
                set_width = size[0]
        if set_width == "auto":
            return self
        # Coalesce min_width: default to 10, floor at 15.
        if min_width is None:
            min_width = 10
        min_width = max(int(min_width), 15)
        # If caller still didn't pick a width, mirror min_width.
        if set_width is None:
            set_width = min_width
        elif set_width != min_width:
            min_width = set_width
        # Compute max_width default.
        if max_width is None:
            max_width = set_width
        self.min_width = min_width
        self.max_width = max_width
        if isinstance(self.max_width, str):
            return self
        self.setMinimumWidth(self.min_width)
        return self

    def _set_height(self, set_height=None, min_height=None, max_height=None) -> Any:
        """"""
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
                if current_height >= min_height:
                    return self
            if set_height is None:
                set_height = min_height
        if min_height is None:
            min_height = set_height
        self.min_height = min_height
        if max_height is None:
            max_height = set_height
        if max_height is None:
            max_height = min_height * 1.5
        self.max_height = max_height
        if isinstance(self.min_height, str):
            return self
        self.setMinimumHeight(self.min_height)
        should_expand = self._should_expand_in_layout()
        if isinstance(self.max_height, str):
            return self
        if not should_expand:
            self.setMaximumHeight(self.max_height)
        return self

    def _should_expand_in_layout(self) -> bool:
        """Check if this widget should expand to fill available space in its layout"""
        try:
            if hasattr(self, "parent") and self.parent is not None:
                parent_layout = self.parent.layout if hasattr(self.parent, "layout") else None
                if parent_layout is not None and isinstance(parent_layout, pyqt.QGridLayout):
                    for row in range(parent_layout.rowCount()):
                        if parent_layout.rowStretch(row) > 0:
                            return True
                    for col in range(parent_layout.columnCount()):
                        if parent_layout.columnStretch(col) > 0:
                            return True
        except Exception:
            pass
        return False

    def _get_text_size(self, text) -> Tuple[int, int]:
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
        min_width = 10
        if width > min_width:
            min_width = width * (1.4 - 0.5 * width**0.8 / 100)
        return (int(min_width), int(min_height))

    def _set_widget_size(self, size=None) -> Any:
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

    def __getstate__(self) -> Any:
        """"""
        state = self.__dict__.copy()
        if state.get("unpickable_attribute", False):
            del state["unpicklable_attribute"]
        return state

    def __setstate__(self, state) -> None:
        """"""


class NchantdWidget(NchantdWidgetMixin, pyqt.QWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        pyqt.QWidget.__init__(self)
        self.config = kahndor.Instruct(pxcfg).select("NchantdWidget").override(cfg)
        self.parent = parent
        self.layout = None
        if not hasattr(self, "context_menu_name"):
            self.context_menu_name = "widget"

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        if hasattr(self.parent, "context_menu"):
            self.context_menu = self.parent.context_menu
        else:
            self.initialize_context_menu()
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

    def initTriggers(self) -> Any:
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

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdSideBar")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdSideBar, self).__init__(self.parent, self.config)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.setMaximumWidth(300)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


def buildPane(parent, cfg, offsetcol=0) -> None:
    """ """
    expandCFG(cfg)
    for row in cfg["seq"].keys():
        for col, wdgt in cfg["seq"][row].items():
            key = list(wdgt.keys())[0]
            cfg["widget"] = lookupWidget(key)
            widget = loadWidget(parent, cfg)
            parent.layout.addWidget(widget, int(row), int(col) + offsetcol)


def expandCFG(cfg) -> Any:
    """Expand Configuration Details to all child wigets within config"""
    dcfg = kahndor.Instruct(pxcfg).select("expandCFG").override(cfg).dikt
    fonts, styles = (dcfg["fonts"], dcfg["styles"])
    for row in dcfg["seq"].keys():
        for col, wCFG in dcfg["seq"][row].items():
            widget = list(wCFG.keys())[0]
            cfg["seq"][row][col][widget] = expandFonts(wCFG[widget], fonts)
            cfg["seq"][row][col][widget] = expandStyles(wCFG[widget], styles)
    return cfg


def expandFonts(cfg, fonts) -> Any:
    """ """
    if "font" in cfg:
        font = cfg["font"]
    else:
        font = "default"
    cfg["font"] = fonts[font]
    return cfg


def expandStyles(cfg, styles) -> Any:
    """ """
    if "style" in cfg.keys():
        style = cfg["style"]
    else:
        style = "default"
    cfg["style"] = styles[style]
    return cfg


def loadWidget(parent, cfg=None):
    """Load the defined widget from its parameters or from a list of registered
    widgets
    Load Source for Daynamically building the tabset for the pane"""
    if cfg is None:
        cfg = {}
    cfg = kahndor.Instruct(pxcfg).override(cfg).dikt
    logma.info(f"Load Widget Config {cfg}")
    if cfg.get("widget", None):
        try:
            logma.info(f"{cfg['widget']}")
            widget = thingify(f"{cfg['widget']}", None, None, True)(parent, cfg)
        except Exception as e:
            logma.info(f"Load Widget Exception {e}")
            apps = cfg.get("apps", [])
            widget = None
            if apps:
                for app in set(apps):
                    try:
                        logma.info(f"{app}.{cfg['widget']}")
                        widget = thingify(f"{app}.{cfg['widget']}", None, None, True)(parent, cfg)
                        if widget:
                            break
                    except Exception as e:
                        if log:
                            logma.warning(f"{app}.{cfg['widget']}")
                            logma.warning(e)
            if widget is None:
                logma.warning(f"Failed to load widget: {cfg['widget']}")
                raise
    else:
        registered_widget = lookupWidget(list(cfg.keys())[0])
        widget = kahndor.Factory.object(registered_widget, parent.app.model.parents)(parent, cfg)
        widget.initWidget(parent.newInstance)
    return widget


def lookupWidget(key) -> Any:
    """ """
    return kahndor.Instruct(pxcfg).select("RegisteredWidgets").dikt[key]
