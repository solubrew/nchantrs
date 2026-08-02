from typing import Any
'\n---\n<(META)>:\n    docid:\n    name:\n    description: >\n    version: 0.0.0.0.0.0\n    authority: filesystem\n    security: seclvl2\n    <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.media.editors.editors import NchantdDocEditor
from nchantrs.widgets.groups import NchantdVScrollGroupBox, NchantdCollapsableGroup
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
if not log:
    logma.off()
pxcfg = join(here, '_data_', 'lists.yaml')

class NchantdList(NchantdWidgetMixin, pyqt.QListWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent)
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdList').override(parent.config).override(cfg)
        self.init_variables()
        self.item_list = None
        self.data = None

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        self.data = self.config.dikt.get('data', [])
        logma.info(f'Items {self.data}')
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        self.set_data()
        return self

    def initWidget(self, cfg=None) -> Any:
        """"""
        self.config.override(cfg)
        self.initModel()
        self.initView()
        return self

    def set_data(self, data=None) -> Any:
        """
        Populate the QListWidget with files from the given directory.
        :param directory: The directory path to scan for files.
        """
        if data is not None:
            self.data = data
        self.clear()
        data = sorted(self.data)
        logma.info(f'Data {data}')
        for row in data:
            logma.info(f'Row {row}')
            item = pyqt.QListWidgetItem(str(row), self)
            self.addItem(item)
        return self

class NchantdListWidget(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(self)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdListWidget').override(parent.config).override(cfg))
        self.list = None

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> None:
        """"""
        super().initView(cfg)
        cfg = {}
        self.list = NchantdList(self, cfg).initWidget()
        self.layout.addWidget(self.list)

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdListEditor(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(self)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('Nchantd'))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        cfg = {}
        self.label = NchantdLabel(self, cfg).initWidget()
        self.layout.addWidget(self.label)
        cfg = {}
        self.list = NchantdList(self, cfg).initWidget()
        self.layout.addWidget(self.list)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdBulletedList(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdBulletedList').override(cfg))

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.layout = pyqt.QVBoxLayout()
        self.setLayout(self.layout)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdInteractiveBulletedList(NchantdBulletedList):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdBulletedList').override(cfg))

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.document = NchantdDocEditor(self, self.config).initWidget()
        layout = pyqt.QHBoxLayout()
        cfg = {'label': 'Add Bullet', 'layout': 'horizontal'}
        self.entry_bar = NchantdEntryEditor(self, cfg).initWidget()
        layout.addWidget(self.entry_bar)
        button = NchantdSaveButton(self, cfg).initWidget(None)
        layout.addWidget(button)
        self.layout.addLayout(layout)
        self.setLayout(self.layout)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdCollapsableList(NchantdCollapsableGroup):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdCollapsableList'))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self, cfg=None) -> Any:
        """"""
        self.data = self.config.dikt.get('data', [])
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        cfg = {'data': self.data}
        self.list = NchantdList(self, cfg).initWidget()
        self.addWidget(self.list)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdTextList(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('Nchantd')
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        logma.info(f'NchantdTextList initialized')

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText('Your bulleted list will appear here...')
        layout.addWidget(self.text_edit)
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('Enter text for the bullet...')
        layout.addWidget(self.input_field)
        self.add_button = QPushButton('Add to Bulleted List')
        self.add_button.clicked.connect(self.add_bullet)
        layout.addWidget(self.add_button)
        self.list_group = NchantdVScrollGroupBox(self, self.config)
        self.list_group.setTitle('Image Directories')
        self.textedit = pyqt.QTextEdit()
        self.create_bulleted_list()
        self.list_group.addWidget(self.textedit)
        self.layout.addLayout(self.list_group.layout)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def add_bullet(self) -> None:
        """
        Adds text from the input field to the bulleted list in the QTextEdit.
        """
        text = self.input_field.text()
        if not text:
            return
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        list_format = QTextListFormat()
        list_format.setStyle(QTextListFormat.ListDisc)
        current_list = cursor.currentList()
        if not current_list:
            cursor.insertList(list_format)
        else:
            cursor.insertText('')
        cursor.insertText(text)
        self.input_field.clear()

    def create_bulleted_list(self) -> None:
        cursor = self.textedit.textCursor()
        list_format = pyqt.QTextListFormat()
        if cursor.currentList():
            list_format.setIndent(cursor.currentList().format().indent() + 1)
        list_format.setStyle(pyqt.QTextListFormat.ListDisc)
        cursor.insertList(list_format)

    def setTitle(self, title) -> Any:
        """"""
        self.list_group.setTitle(title)
        return self