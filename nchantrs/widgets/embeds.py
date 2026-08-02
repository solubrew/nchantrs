from typing import Any
'#\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n---  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n<(META)>:  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        DOCid:   #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        name:   #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        description: >  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n                  #\t\t\t||\n        expirary: <[expiration]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        version: <[version]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        path: <[LEXIvrs]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        outline: <[outline]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        authority: document|this  #\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        security: sec|lvl2  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        <(WT)>: -32  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n'
from os.path import abspath, dirname, exists, join
from kahndor import kahndor
import logging
import os
import pty
import array
import fcntl
import termios
from nchantrs.libraries import pyqt
logger = logging.getLogger(__name__)
from nchantrs.widgets.widgets import NchantdWidget
here = join(dirname(__file__), '')
version = '0.0.1'
pxcfg = join(here, '_data_', 'embeds.yaml')

class NchantdTerminalView(pyqt.QPlainTextEdit):
    """
    A simple terminal emulator widget using QPlainTextEdit and pty.
    """

    def __init__(self, parent=None) -> None:
        super(NchantdTerminalView, self).__init__(parent)
        self.setReadOnly(False)
        self.setLineWrapMode(pyqt.QPlainTextEdit.NoWrap)
        font = pyqt.QFont('Monospace', 10)
        font.setStyleHint(pyqt.QFont.Monospace)
        self.setFont(font)
        self.current_format = pyqt.QTextCharFormat()
        self._set_default_format()
        self.master_fd, self.slave_fd = pty.openpty()
        self.process = pyqt.QProcess(self)
        self.process.setProcessChannelMode(pyqt.QProcess.MergedChannels)
        self.notifier = pyqt.QSocketNotifier(self.master_fd, pyqt.QSocketNotifier.Read, self)
        self.notifier.activated.connect(self.handle_read)
        self.process.finished.connect(self.on_finished)
        logma.info(f'NchantdTerminalView initialized')

    def _set_default_format(self) -> None:
        self.current_format = pyqt.QTextCharFormat()
        self.current_format.setForeground(pyqt.QColor('white'))
        self.current_format.setBackground(pyqt.QColor('black'))

    def start_shell(self, shell='/bin/bash') -> None:
        """Starts the terminal shell."""
        env = pyqt.QProcessEnvironment.systemEnvironment()
        env.insert('TERM', 'xterm-256color')
        env.insert('COLORTERM', 'truecolor')
        self.process.setProcessEnvironment(env)
        self.process.setProgram(shell)
        self.process.setArguments(['-i'])
        self.process.start()

    def _setup_pty(self) -> None:
        os.setsid()
        os.dup2(self.slave_fd, 0)
        os.dup2(self.slave_fd, 1)
        os.dup2(self.slave_fd, 2)
        import resource
        max_fd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
        if max_fd == resource.RLIM_INFINITY:
            max_fd = 1024
        for i in range(3, max_fd):
            try:
                os.close(i)
            except OSError:
                pass
        fcntl.ioctl(0, termios.TIOCSCTTY, 0)

    def handle_read(self) -> None:
        """Reads from pty and displays in the widget."""
        try:
            data = os.read(self.master_fd, 4096)
            if data:
                text = data.decode('utf-8', errors='replace')
                self._process_text(text)
        except OSError:
            pass

    def _process_text(self, text) -> None:
        cursor = self.textCursor()
        cursor.movePosition(pyqt.QTextCursor.End)
        import re
        ansi_regex = re.compile('(\\x1B\\[[0-?]*[ -/]*[@-~])')
        parts = ansi_regex.split(text)
        for part in parts:
            if not part:
                continue
            if part.lower().startswith('\x1b['):
                self._handle_ansi_sequence(part, cursor)
            else:
                self._insert_text(part, cursor)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()

    def _insert_text(self, text, cursor) -> None:
        if '\x08' in text:
            for char in text:
                if char == '\x08':
                    cursor.deletePreviousChar()
                else:
                    cursor.insertText(char, self.current_format)
        elif '\r' in text:
            for char in text:
                if char == '\r':
                    cursor.movePosition(pyqt.QTextCursor.StartOfBlock, pyqt.QTextCursor.MoveAnchor)
                else:
                    cursor.insertText(char, self.current_format)
        else:
            cursor.insertText(text, self.current_format)

    def _handle_ansi_sequence(self, seq, cursor) -> None:
        """Handles basic ANSI escape sequences."""
        if not seq.endswith('m') and (not seq.endswith('J')) and (not seq.endswith('K')) and (not seq[2:-1].isdigit()):
            pass
        code = seq[-1]
        params = seq[2:-1].split(';')
        params = [int(p) if p else 0 for p in params]
        if code == 'm':
            self._handle_sgr(params)
        elif code == 'J':
            if params[0] == 2:
                self.clear()
                cursor.movePosition(pyqt.QTextCursor.End)
        elif code == 'K':
            if params[0] == 0:
                cursor.movePosition(pyqt.QTextCursor.EndOfBlock, pyqt.QTextCursor.KeepAnchor)
                cursor.removeSelectedText()

    def _handle_sgr(self, params) -> None:
        """Handles SGR (Select Graphic Rendition) parameters."""
        if not params:
            params = [0]
        i = 0
        while i < len(params):
            p = params[i]
            if p == 0:
                self._set_default_format()
            elif p == 1:
                self.current_format.setFontWeight(pyqt.QFont.Bold)
            elif p == 3:
                self.current_format.setFontItalic(True)
            elif p == 4:
                self.current_format.setFontUnderline(True)
            elif 30 <= p <= 37:
                self.current_format.setForeground(self._get_color(p - 30, bright=False))
            elif 40 <= p <= 47:
                self.current_format.setBackground(self._get_color(p - 40, bright=False))
            elif 90 <= p <= 97:
                self.current_format.setForeground(self._get_color(p - 90, bright=True))
            elif 100 <= p <= 107:
                self.current_format.setBackground(self._get_color(p - 100, bright=True))
            elif p == 38 or p == 48:
                if i + 2 < len(params) and params[i + 1] == 5:
                    color = self._get_256_color(params[i + 2])
                    if p == 38:
                        self.current_format.setForeground(color)
                    else:
                        self.current_format.setBackground(color)
                    i += 2
            i += 1

    def _get_color(self, index, bright=False) -> Any:
        colors = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
        color_name = colors[index]
        if bright:
            if color_name == 'black':
                return pyqt.QColor('gray')
            return pyqt.QColor(f'light{color_name}')
        return pyqt.QColor(color_name)

    def _get_256_color(self, n) -> Any:
        if n < 8:
            return self._get_color(n, bright=False)
        elif n < 16:
            return self._get_color(n - 8, bright=True)
        return pyqt.QColor('white')

    def keyPressEvent(self, event) -> None:
        """Captures key events and writes to pty."""
        text = event.text()
        if not text:
            key = event.key()
            if key == pyqt.Qt.Key_Enter or key == pyqt.Qt.Key_Return:
                text = '\n'
            elif key == pyqt.Qt.Key_Backspace:
                text = '\x08'
            elif key == pyqt.Qt.Key_Tab:
                text = '\t'
            elif key == pyqt.Qt.Key_Escape:
                text = '\x1b'
            elif key == pyqt.Qt.Key_Up:
                text = '\x1b[A'
            elif key == pyqt.Qt.Key_Down:
                text = '\x1b[B'
            elif key == pyqt.Qt.Key_Right:
                text = '\x1b[C'
            elif key == pyqt.Qt.Key_Left:
                text = '\x1b[D'
        if text:
            os.write(self.master_fd, text.encode('utf-8'))

    def on_finished(self) -> None:
        self.insertPlainText('\n[Process finished]\n')
        self.setReadOnly(True)

    def resizeEvent(self, event) -> None:
        """Handle terminal resizing."""
        super(NchantdTerminalView, self).resizeEvent(event)
        self._update_pty_size()

    def _update_pty_size(self) -> None:
        metrics = self.fontMetrics()
        width = self.viewport().width()
        height = self.viewport().height()
        cols = max(1, width // metrics.horizontalAdvance('W'))
        rows = max(1, height // metrics.lineSpacing())
        buf = array.array('h', [rows, cols, 0, 0])
        try:
            fcntl.ioctl(self.master_fd, termios.TIOCSWINSZ, buf)
        except OSError:
            pass

class NchantdTerminalEmbed(NchantdWidget):
    """ """

    def __init__(self, app, cfg, parent=None) -> None:
        """'"""
        super(NchantdTerminalEmbed, self).__init__(parent, cfg)
        self.app = app
        self.initWidget()

    def initModel(self) -> Any:
        super().initModel()
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> Any:
        super().initView()
        logma.info(f'initView {{type(self).__name__}}')
        return self

    def initWidget(self) -> Any:
        """ """
        self.layout = pyqt.QVBoxLayout()
        self.terminal = NchantdTerminalView(self)
        self.layout.addWidget(self.terminal)
        self.setLayout(self.layout)
        shell = self.config.dikt.get('shell', '/bin/bash')
        self.terminal.start_shell(shell)
        return self