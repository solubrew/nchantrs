# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""  #																			||
---  #																			||
<(META)>:  #																	||
    docid:   #																	||
    name:   #																	||
    description: >  #															||
          #			||
    expirary: <[expiration]>  #													||
    version: <[version]>  #														||
    path: <[LEXIvrs]>  #														||
    outline: <[outline]>  #														||
    authority: document|this  #													||
    security: sec|lvl2  #														||
    <(WT)>: -32  #																||
"""  # ||
# -*- coding: utf-8 -*-#														||
# ===============================Core Modules====================================||
from os.path import abspath, dirname, join
import datetime as dt
from types import MethodType
import re

# ===============================================================================||
from condor import condor
from nchantrs.dialogs.files import NchantdFileOpenSigil
from nchantrs.libraries import pyqt
from nchantrs.utilities.formatting import getAlignment
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.media.images import NchantdImage
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from ogma.logma import Logma
from nchantrs.utilities.files import qimage_to_data_uri

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
logma.off()

# ===============================================================================||
pxcfg = join(abspath(here), "_data_", "editors.yaml")  # ||assign default config

class NchantdDocEditor(NchantdWidgetMixin, pyqt.QTextEdit):  # (pyqt.QsciScintillaBase):

    def __init__(self, parent=None, cfg=None):
        """Document editor widget built on top of QsciScintilla widget
        I believe this requires PyQt5, not sure what is available as a
        substitute for PySide2"""
        super().__init__()
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdDocEditor")
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.embeded_links = None

    def initModel(self):
        """ """
        super().initModel()
        self.embeded_links = []
        # self.name = self.config.dikt['tab']['name']
        # self.data = j.loads(self.config.dikt['tab']['widgdata'].replace("'", '"'))
        # self.setText(self.data.get('text'))
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        text = self.config.dikt.get("text", None)
        if text is None or text.lower() in ("none", ""):
            text = self.config.dikt.get("default_text", "Missing Text")
        logma.info(f"Background Color {self.config.dikt.get('background_color', None)}")
        #self.setOpenExternalLinks(False)
        #self.anchorClicked.connect(self.handle_link_click)
        self.set_background(self.config.dikt.get("background_color", "white"))
        self.setTabStopDistance(self.config.dikt.get("tab_length", 10))
        self.setText(text)
        # self.set_size()
        return self

    def initWidget(self):
        """ """
        self.initModel()
        self.initView()
        return self

    def add_action(self, name, func, shortcut=None):
        action = pyqt.QAction(name, self)
        action.triggered.connect(func)
        if shortcut:
            action.setShortcut(shortcut)
        self.toolbar.addAction(action)
        return self

    def apply_format_to_selected_text(self, format_to_apply):
        """Apply a `QTextCharFormat` modification to the currently selected text."""
        cursor = self.textCursor()
        if cursor.hasSelection():
            cursor.mergeCharFormat(format_to_apply)
        return self

    def canInsertFromMimeData(self, source) -> bool:
        # Advertise that we can handle image pastes, plus the default types
        return source.hasImage() or super().canInsertFromMimeData(source)

    def remove_leading_empty_block(self, text_edit):
        """Remove the first paragraph separator from the document."""
        doc = text_edit.document()
        block = doc.firstBlock()
        if not block.isValid():
            return
        # selectedText() replaces paragraph separators with U+2029; for an empty block it's ""
        cur = pyqt.QTextCursor(block)
        cur.select(pyqt.QTextCursor.SelectionType.BlockUnderCursor)
        if cur.selectedText().strip() == "":
            # Avoid adding to undo stack if you want a clean history
            was_undo = doc.isUndoRedoEnabled()
            doc.setUndoRedoEnabled(False)
            try:
                cur.removeSelectedText()
                # Remove the paragraph separator to merge with the next block
                cur.deleteChar()
            finally:
                doc.setUndoRedoEnabled(was_undo)

    def insertFromMimeData(self, source) -> None:
        """
        Paste handler:
        - If clipboard has an image, embed as <img src="data:image/png;base64,...">.
        - If clipboard has URLs pointing to images, load and embed those.
        - Otherwise, fall back to default rich text/HTML/plain-text handling.
        """
        # 1) Direct image (e.g., copied from an image editor or screenshot tool)
        if source.hasImage():
            img = source.imageData()
            if isinstance(img, pyqt.QImage) and not img.isNull():
                self._insert_image(img)
                return
        # 2) URLs (e.g., copying an image file from a file manager)
        if source.hasUrls():
            handled_any = False
            for url in source.urls():
                if url.isLocalFile():
                    local_path = url.toLocalFile()
                    img = pyqt.QImage(local_path)
                    if not img.isNull():
                        self._insert_image(img)
                        handled_any = True
                    else:
                        # If it's not an image file, let default flow handle it as text path, etc.
                        pass
                else:
                    # Remote URLs: prefer to keep original URL in HTML if desired, or skip.
                    # Basic safe approach: just insert the URL as text.
                    pass
            if handled_any:
                return
        # 3) Let QTextEdit handle HTML/RTF/plain text as usual
        super().insertFromMimeData(source)
        return self

    def _insert_image(self, img: pyqt.QImage):
        # Optional scaling before embedding to keep HTML compact or fit layout.
        if self.max_width and img.width() > self.max_width:
            img = img.scaledToWidth(self.max_width, Qt.SmoothTransformation)
        data_uri = qimage_to_data_uri(img, "PNG")
        if not data_uri:
            return
        # You can add width/height attributes to control layout if desired.
        # Example includes width attribute if max_width used.
        attrs = ""
        if self.max_width:
            attrs = f' width="{img.width()}"'
        html = f'<img src="{data_uri}"{attrs} />'
        cursor = self.textCursor()
        cursor.insertHtml(html)
        return self

    def change_font_size(self, size):
        """Change font size of selected text."""
        format_to_apply = pyqt.QTextCharFormat()
        format_to_apply.setFontPointSize(size)
        self.apply_format_to_selected_text(format_to_apply)
        return self

    def change_font_color(self):
        """Change font color of selected text."""
        color = pyqt.QColorDialog.getColor()
        if color.isValid():
            format_to_apply = pyqt.QTextCharFormat()
            format_to_apply.setForeground(color)
            self.apply_format_to_selected_text(format_to_apply)
        return self

    def change_highlight(self):
        """Change highlight color of selected text."""
        color = pyqt.QColorDialog.getColor()
        if color.isValid():
            format_to_apply = pyqt.QTextCharFormat()
            format_to_apply.setBackground(color)
            self.apply_format_to_selected_text(format_to_apply)
        return self

    def cmd_change_color(self):
        """"""
        return self

    def cmd_change_color_background(self):
        """"""
        return self

    def cmd_change_color_highlight(self):
        """"""
        return self

    def cmd_change_bold(self):
        """"""
        return self

    def cmd_change_italic(self):
        """"""
        return self

    def cmd_change_underline(self):
        """"""
        return self

    def cmd_change_underline_double(self):
        """"""
        return self

    def cmd_change_strike(self):
        """"""
        return self

    def cmd_change_subscript(self):
        """"""
        return self

    def cmd_change_superscript(self):
        """"""
        return self

    def create_bulleted_list(self):
        """"""
        cursor = self.textCursor()
        list_format = pyqt.QTextListFormat()
        if cursor.currentList():
            list_format.setIndent(cursor.currentList().format().indent() + 1)
        list_format.setStyle(pyqt.QTextListFormat.ListDisc)
        cursor.insertList(list_format)
        return self

    def convert_urls_to_links(self, text):
        """"""
        # Regular expression for finding URLs
        url_pattern = r"(https?://\S+)"
        # Replace URLs with HTML anchor tags
        self.embeded_links.append(re.sub(url_pattern, r'<a href="\1">\1</a>', text))
        return self

    def focusInEvent(self, event):
        """ """
        super().focusInEvent(event)
        logma.info(f"Focus In Event")
        return self

    def focusOutEvent(self, event):
        """ """
        # Check if the current text cursor position equals the timestamp's position
        current_text = self.toPlainText()
        # self.save()
        super().focusOutEvent(event)
        logma.info(f"Focus Out Event")
        return self

    def get_text(self):
        """"""
        text = self.toPlainText()
        return text

    def handle_link_click(self, url):
        """"""
        #super().handle_link_click(url)
        if "http?://" in url:
            self.add_new_browser_tab(url)
        elif "file:///" in url:
            self.add_new_script_tab(url)
        return self

    def insert_bullet(self):
        """"""
        return self

    def insert_code(self):
        """"""
        return self

    def insert_datetime(self, format_=None, prefix="", suffix=""):
        """"""
        if format_ is None:
            format_ = "%Y-%m-%d %H:%M:%S"
        timestamp = dt.datetime.now().strftime(format_)
        cursor = self.textCursor()
        #TODO check previous text for number of newline characters
        # at the top of the document keep no new lines
        # between each entry ensure 2 blank lines...3 new lines
        if self.toPlainText() == "":
            cursor.insertText(f"{prefix}{timestamp}{suffix}\n")
        else:
            cursor.insertText(f"\n\n{prefix}{timestamp}{suffix}\n")
        return self

    def insert_image(self):
        """
        Insert an image into the document.
        """
        cfg = {}
        sigil = NchantdFileOpenSigil(self, cfg).initWidget()
        file_path = sigil.getOpenFileName(self, "Insert Image", "", "Images (*.png *.jpg *.bmp)")
        if file_path:
            cursor = self.textCursor()
            cursor.insertImage(file_path)
        return self

    def insert_link(self, text):
        """"""
        #set text blue
        #set text underline
        cursor = self.textCursor()
        cursor.insertText(text)
        return self

    def insert_shape(self):
        """"""
        return self

    def insert_table(self, rows=2, columns=2):
        """
        Insert a table into the document at the cursor position.
        """
        cursor = self.textCursor()
        table_format = pyqt.QTextTableFormat()
        table_format.setAlignment(pyqt.Qt.AlignCenter)
        table_format.setCellPadding(4)
        table_format.setCellSpacing(2)
        cursor.insertTable(rows, columns, table_format)
        return self

    def insert_webpage(self):
        """"""
        return self

    def is_bold(self):
        """"""
        return self.fontWeight() == pyqt.QFont.Weight.Bold

    def is_italic(self):
        """"""
        return self.fontItalic()

    def is_underlined(self):
        """"""
        return self.fontUnderline()

    def is_strike(self):
        """"""
        return self.fontStrikeOut()

    def is_superscript(self):
        """"""
        return self.verticalAlignment() == pyqt.QTextCharFormat.AlignSuperScript

    def is_subscript(self):
        """"""
        return self.verticalAlignment() == pyqt.QTextCharFormat.AlignSubScript

    ## --- Helper Methods --- ##
    def merge_format_on_selection(self, fmt):
        """
        Merge the provided text format with the current selection.
        """
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.select(pyqt.QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(fmt)
        return self

    def modify_format(self, modify_fn):
        """Modify the format of the selected text based on a function."""
        cursor = self.textCursor()
        if cursor.hasSelection():
            current_format = cursor.charFormat()
            modify_fn(current_format)
            cursor.mergeCharFormat(current_format)
        return self

    def onEnterEvent(self):
        """Run a save of the doc editor data to the database"""
        return self

    def set_cursor_position(self, to=None):
        """"""
        cursor = self.textCursor()
        if to is None:
            to = pyqt.QTextCursor.End
        cursor.movePosition(to)
        self.setTextCursor(cursor)
        return self

    def set_background(self, color=None, hex=None):
        """"""
        super().set_background(color, hex)
        return self

    ## --- Editor Actions --- ##
    def set_font(self, font):
        """
        Set the font family for the selected text.
        """
        fmt = pyqt.QTextCharFormat()
        fmt.setFontFamily(font.family())
        self.merge_format_on_selection(fmt)
        return self

    def set_font_size(self, size):
        """
        Set the font size for the selected text.
        """
        fmt = pyqt.QTextCharFormat()
        fmt.setFontPointSize(float(size))
        self.merge_format_on_selection(fmt)

    def set_text_color(self):
        """
        Open a color picker dialog and set the selected text color.
        """
        color = pyqt.QColorDialog.getColor()
        if color.isValid():
            fmt = pyqt.QTextCharFormat()
            fmt.setForeground(color)
            self.merge_format_on_selection(fmt)
        return self

    def set_alignment(self, alignment):
        """
        Set the alignment for the current paragraph.
        """
        self.document_editor.setAlignment(alignment)
        return self


class NchantdEntryBox(NchantdWidgetMixin, pyqt.QLineEdit):
    """Standard Nchantd Entry Box"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__()
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdEntryBox")
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.can_save = False
        self.user_editted = None
        self.entry_data = None
        self.text_changed = False
        self.value = None

    def initModel(self, handler):
        """"""
        super().initModel()
        self.textChanged.connect(self.on_text_changed)
        self.textEdited.connect(self.on_text_edited)
        self.returnPressed.connect(self.on_return_pressed)
        # self.editingFinished.connect(self.on_editing_finished)
        self.selectionChanged.connect(self.on_selection_changed)
        self.cursorPositionChanged.connect(self.on_cursor_position_changed)
        self.value = self.config.dikt.get("value", self.config.dikt.get("default_text", ""))
        if self.config.dikt.get("get_value", None):
            self.value = self.config.dikt["get_value"]()
        return self

    def initView(self, cfg=None):
        """ """
        super().initView()
        if cfg is None:
            cfg = {}
        if "font" in cfg.keys():
            font = pyqt.QFont(cfg["font"], cfg["font"]["size"], pyqt.QFont.Bold)
            self.setFont(font)
        logma.info(f"Size {self.config.dikt.get('size', None)}")
        logma.info(f"Width {self.config.dikt.get('width', 'BLANK')}")
        value = self.config.dikt.get("value", self.config.dikt.get("default_text", ""))
        self.set_value(value)
        self.set_size()
        return self

    def refresh_view(self, cfg):
        """"""

    def initWidget(self, handler=None):
        """"""
        self.initModel(handler)
        self.initView()
        return self

    def on_text_changed(self, text):
        """"""
        logma.info(f"Text Changed {text}")
        self.user_editted = dt.datetime.now()
        self.can_save = True
        self.value = text
        self.entry_data = self.value
        logma.info(f"Text Changed {self.value} {self.entry_data}")
        logma.info(f"Parent {self.parent}")
        return self

    def on_text_edited(self, text):
        """on text entered it needs to be added to a data structure for
        assemblying an update record
        manually it would be easy wire the returnPressed event to an in
        class function but how to access it on selection of a submit button"""
        logma.info(f"Text Entered {text}")
        self.user_editted = dt.datetime.now()
        self.can_save = True
        self.value = text
        self.entry_data = self.value
        logma.info(f"Text Changed {self.value} {self.entry_data}")
        return self

    def on_return_pressed(self, text):
        """enter pressed"""
        print("Enter Pressed")
        self.user_editted = dt.datetime.now()
        self.can_save = True
        self.value = text
        return self

    def focusOutEvent(self, event=None):
        """Change in focus"""
        # super().focusOutEvent(event)
        # self.on_editing_finished()

    def on_editing_finished(self):
        """"""
        logma.info(f"Editing Finished {self.text()}")
        if self.text() != self.entry_data:
            self.entry_data = self.text()
            self.text_changed = True
        logma.info(f"Entry Data {self.entry_data}")
        return self

    def on_selection_changed(self, val=True):
        """User selecting"""

    def on_cursor_position_changed(self, position: int):
        """cursor movement"""

    def set_size(self, set_width=None, set_height=None, min_width=10, min_height=10, max_width=None, max_height=None):
        """"""
        super().set_size(set_width, set_height, min_width, min_height, max_width, max_height)
        if self.minimumWidth() < 100:
            self.setMinimumWidth(100)
        if self.minimumHeight() < 25:
            self.setMinimumHeight(25)
        return self

    def set_value(self, value):
        """"""
        logma.info(f"Set Value{value}")
        if isinstance(value, MethodType):
            value = value()
        self.value = value
        self.setText(str(value))
        return self
        # self._set_entry_box_size()


class NchantdLabeledEntry(NchantdWidget):
    """ """

    def __init__(self, parent=None, cfg={}):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdLabeledEntry"))
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.model = pyqt.QStandardItemModel(self)
        self.style = None
        self.label = None
        self.textbox = None
        self.entry_data = ""

    def initModel(self, handler):
        """"""
        super().initModel()
        self.entry_data = ""
        return self

    def initView(self, handler=None, size=None):
        """ """
        super().initView()
        if self.config.dikt.get("icon"):
            cfg = {"icon": self.config.dikt.get("icon"), "size": [40, 40]}
            self.label = NchantdImage(self, cfg).initWidget()
        else:
            cfg = {"text": self.config.dikt.get("label", "")}
            self.label = NchantdLabel(self, cfg).initWidget()
        self.layout.addWidget(self.label)
        style = "single"
        cfg = {"entrybox": {"style": style}}
        cfg["size"] = self.config.dikt.get("entrybox", {"size": ["auto", "auto"]}).get("size", None)
        self.textbox = NchantdEntryBox(self, self.config.override(cfg)).initWidget(handler)
        self.layout.addWidget(self.textbox)
        self.layout.setAlignment(getAlignment(self.config.dikt.get("justify", "left")))
        # self.setMaximumWidth((self.label.size().width() + self.textbox.size().width()) * 1.01)
        return self

    def initWidget(self, handler=None, size=None):
        """ """
        self.initModel(handler)
        self.initView(handler, size)
        return self

    def getEntry(self, row):
        """"""
        self.name, value = None, None
        try:
            self.name = self.item(row, 0).text()
        except:
            pass
        try:
            self.value = self.item(row, 1).text()
        except:
            pass
        return self.name, self.value

    def set_label(self, text):
        """"""
        self.label.setText(text)
        return self

    def setText(self, text):
        """"""
        logma.info(f"Set Text {text}")
        if self.textbox:
            self.textbox.set_value(text)
        self.entry_data = text
        return self

    def setPlaceholderText(self, text):
        self.textbox.setPlaceholderText(text)
        self.textbox.set_value(text)
        self.config.dikt["default_text"] = text
        return self

    def refresh_text_box(self):
        """"""
        logma.info("Refresh Text Box")
        self.textbox.initView()


class NchantdEntryEditor(NchantdLabeledEntry):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select('NchantdEntryEditor'))
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
        logma.depricate("NchantdEntryEditor is deprecated. Use NchantdLabledEntry instead.")
        self.initModel()
        self.initView()
        return self


class NchantdEntryEditorActivator(NchantdEntryEditor):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdEntryEditorActivator")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self.parent, self.config)
        self.config.override(cfg)

    def initModel(self):
        """"""
        return self

    def initView(self):
        """"""
        super().initView()
        self.button = NchantdButton(self, self.config).initWidget()
        self.layout.addWidget(self.button)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdEntryListEditor(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdEntryListEditor")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdEntryListEditor, self).__init__(self.parent)

    def initModel(self):
        """"""
        return self

    def initView(self):
        """"""
        self.layout = pyqt.QVBoxLayout()
        group = pyqt.QGroupBox()
        self.entry_editor = NchantdEntryEditorActivator(self, self.config).initWidget()
        self.layout.addWidget(self.entry_editor)
        cfg = {}
        group.setTitle(self.config.dikt["label"])
        self.layout.addWidget(group)
        self.setLayout(self.layout)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdAppendOnlyEditor(NchantdDocEditor):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdAppendOnlyEditor")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.setPlaceholderText("Type here... Text will only be appended.\n")
        text_cursor = self.textCursor()
        text_cursor.movePosition(pyqt.QTextCursor.End)
        self.setTextCursor(text_cursor)  # Force cursor to the end
        self.user_input_locked = False  # Prevent backspaces and deletions

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def keyPressEvent(self, event):
        """
        Allow input only at the end of the editor, preventing deletions or editing.
        """
        cursor = self.textCursor()
        # Ensure the cursor is always at the end
        if cursor.position() < len(self.toPlainText()):
            self.set_cursor_position()
        if event.key() == pyqt.Qt.Key_Backspace:
            return None
        # Handle the user's keypress normally (appending only)
        super().keyPressEvent(event)
        return self

class NchantdScratchEditor(NchantdWidget):
    """Continous text editor that autosaves and restores has a clear button and
    a save tab which allows you to save a seperate document or as a tab"""

    def __init__(self, parent=None, cfg={}):
        """ """
        self.parent = parent
        if parent:
            cfg = self.parent.config
        self.config = condor.Instruct(pxcfg).select("NchantdScratchEditor")
        self.config.override(cfg)
        super().__init__(parent)
        self.editor = None
        self.button_export = None
        self.button_maketab = None
        # self.model = editormodels.NchantdScratchEditorModel(self)
        # #self.view = editorviews.NchantdScratchEditorView(self)

    def initModel(self):
        """ """
        super().initModel()
        # self.model.initModel()
        return self

    def initView(self):
        """ """
        super().initView({"layout": "grid"})
        self.createExportButton()
        self.layout.addWidget(self.button_export, 1, 1)
        self.createMakeTabButton()
        self.layout.addWidget(self.button_maketab, 1, 2)
        self.createEditor()
        self.layout.addWidget(self.editor, 2, 1, 1, 2)
        return self

    def initWidget(self):
        """ """
        self.initModel()
        self.initView()
        return self

    def createEditor(self):
        """ """
        self.editor = pyqt.QTextEdit(self)
        self.editor.setHorizontalScrollBarPolicy(pyqt.Qt.ScrollBarAlwaysOff)
        return self

    def createExportButton(self):
        """ """
        self.button_export = NchantdButton(self, {"name": "Export"}).initWidget()
        return self

    def createMakeTabButton(self):
        """ """
        self.button_maketab = NchantdButton(self, {"name": "Clear"}).initWidget()
        return self

    def clear(self):
        """ """

    def export(self):
        """ """

    def setTheme(self):
        """ """


class NchantdDocEditorView(pyqt.QListView):
    """ """

    def __init__(self, parent=None, cfg={}):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        if parent:
            cfg = parent.config
        self.config.override(condor.Instruct(pxcfg).select("NchantdEditorView"))
        self.config.override(cfg)

    def initView(self):
        """ """
        # self.layout = pyqt.QVBoxLayout()
        # self.layout.addWidget(self)
        self.buildEditor()
        return self

    def buildEditor(self):
        """ """
        return self

    def setTheme(self, theme):
        """ """
        self.setMarginsForegroundColor()
        self.setMarginsBackgroundColor()
        self.SendScintilla(
            pyqt.QsciScintillaBase.SCI_STYLESETBACK, pyqt.QsciScintillaBase.STYLE_DEFAULT, theme.Paper.Default
        )
        self.SendScintilla(
            pyqt.QsciScintillaBase.SCI_STYLESETBACK,
            pyqt.QsciScintillaBase.STYLE_LINENUMBER,
            theme.LineMargin.BackGround,
        )
        self.SendScintilla(pyqt.QsciScintillaBase.SCI_SETCARETFORE, theme.Cursor)

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
