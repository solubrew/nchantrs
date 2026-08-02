from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.widgets.panes.panes import NchantdPane
from nchantrs.libraries import pyqt
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'chat.yaml')

class NchantdChat(NchantdPane):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdChat').override(cfg))
        self.display = None
        self.protocol = None
        self.text_input = None
        self.submit_button = None
        self.input = None
        logma.info(f'NchantdChat initialized')

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView({'layout': 'grid'})
        self.setDisplay()
        self.build_input()
        self.layout.addWidget(self.display)
        self.layout.addWidget(self.input)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def build_input(self) -> None:
        """Build the input widget for user messages"""
        layout = pyqt.QHBoxLayout()
        self.text_input = pyqt.QLineEdit(self)
        self.text_input.returnPressed.connect(self.send_message)
        self.submit_button = pyqt.QPushButton('Send', self)
        layout.addWidget(self.text_input)
        layout.addWidget(self.submit_button)
        self.input = pyqt.QWidget(self)
        self.input.setLayout(layout)

    def create_connection(self, connection) -> None:
        logma.info(f'create_connection called')
        return self

    def setDisplay(self) -> Any:
        """Initialize the display widget as a multiline text area"""
        cfg = {'text': '0'}
        self.config.dikt['width'] = None
        self.config.dikt['height'] = None
        self.config.dikt['size'] = None
        self.display = pyqt.QTextEdit(self)
        self.display.setReadOnly(True)
        self.display.setAlignment(pyqt.Qt.AlignmentFlag.AlignRight | pyqt.Qt.AlignmentFlag.AlignBottom)
        width = 300
        height = 800
        self.display.setMinimumSize(width, int(height * 0.1))
        font = self.display.font()
        font.setPointSize(font.pointSize() + 8)
        self.display.setFont(font)
        self.display.setStyleSheet('QTextEdit { background-color: black; color: white; padding: 5px; }')
        self.display.setFocusPolicy(pyqt.Qt.FocusPolicy.NoFocus)
        self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignCenter | pyqt.Qt.AlignmentFlag.AlignTop)
        self.display.setVerticalScrollBarPolicy(pyqt.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.display.setHtml('<div style="text-align: right;">0</div>')
        return self

    def set_protocol(self, protocol) -> None:
        """set the communication protocol"""
        self.protocol = protocol

    async def send_message(self) -> None:
        """"""
        message = self.text_input.text()
        self.text_input.setText('')
        self.protocol.send_message(message)

    async def receive_message(self) -> None:
        """"""
        await self.protocol.receive_message()
        return