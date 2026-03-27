# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""#																			||
---  #																			||
<(META)>:  #																	||
        DOCid:   #																	||
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
from os.path import abspath, dirname, exists, join

# ===============================================================================||
from condor import condor

import logging
import os
import pty
import array
import fcntl
import termios
from nchantrs.libraries import pyqt

logger = logging.getLogger(__name__)
from nchantrs.widgets.widgets import NchantdWidget

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
version = "0.0.1"  # ||
# ===============================================================================||
pxcfg = f"{here}_data_/embeds.yaml"
pxcfg = {}


class NchantdTerminalView(pyqt.QPlainTextEdit):
    """
    A simple terminal emulator widget using QPlainTextEdit and pty.
    """

    def __init__(self, parent=None):
        super(NchantdTerminalView, self).__init__(parent)
        self.setReadOnly(False)
        self.setLineWrapMode(pyqt.QPlainTextEdit.NoWrap)

        # Set a monospaced font
        font = pyqt.QFont("Monospace", 10)
        font.setStyleHint(pyqt.QFont.Monospace)
        self.setFont(font)

        # Terminal process setup
        self.master_fd, self.slave_fd = pty.openpty()
        self.process = pyqt.QProcess(self)
        self.process.setProcessChannelMode(pyqt.QProcess.MergedChannels)

        self.notifier = pyqt.QSocketNotifier(self.master_fd, pyqt.QSocketNotifier.Read, self)
        self.notifier.activated.connect(self.handle_read)

        self.process.finished.connect(self.on_finished)

    def start_shell(self, shell="/bin/bash"):
        """Starts the terminal shell."""
        env = pyqt.QProcessEnvironment.systemEnvironment()
        env.insert("TERM", "xterm")  # Basic xterm emulation
        self.process.setProcessEnvironment(env)

        # To make it work with QProcess and pty on Linux:
        self.process.setProgram(shell)
        self.process.setArguments(["-i"])  # Interactive mode
        # self.process.setChildProcessModifier(self._setup_pty)
        self.process.start()

    def _setup_pty(self):
        os.setsid()
        os.dup2(self.slave_fd, 0)
        os.dup2(self.slave_fd, 1)
        os.dup2(self.slave_fd, 2)

        # Close all other FDs
        import resource

        max_fd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
        if max_fd == resource.RLIM_INFINITY:
            max_fd = 1024
        for i in range(3, max_fd):
            try:
                os.close(i)
            except OSError:
                pass

        # Set the controlling terminal
        fcntl.ioctl(0, termios.TIOCSCTTY, 0)

    def handle_read(self):
        """Reads from pty and displays in the widget."""
        try:
            data = os.read(self.master_fd, 4096)
            if data:
                # Handle backspaces and basic carriage returns
                text = data.decode("utf-8", errors="replace")

                # Move cursor to end before inserting
                cursor = self.textCursor()
                cursor.movePosition(pyqt.QTextCursor.End)

                # Simple backspace and ANSI escape code filtering
                # We filter out common ANSI escape sequences like [?2004h (bracketed paste)
                import re

                ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
                text = ansi_escape.sub("", text)

                if "\b" in text:
                    for char in text:
                        if char == "\b":
                            cursor.deletePreviousChar()
                        else:
                            cursor.insertText(char)
                else:
                    cursor.insertText(text)

                self.setTextCursor(cursor)
                # Scroll to bottom
                self.ensureCursorVisible()
        except OSError:
            pass

    def keyPressEvent(self, event):
        """Captures key events and writes to pty."""
        text = event.text()
        if not text:
            # Handle special keys
            key = event.key()
            if key == pyqt.Qt.Key_Enter or key == pyqt.Qt.Key_Return:
                text = "\n"
            elif key == pyqt.Qt.Key_Backspace:
                text = "\b"
            elif key == pyqt.Qt.Key_Tab:
                text = "\t"
            elif key == pyqt.Qt.Key_Escape:
                text = "\x1b"
            # Add more as needed (Up, Down, etc. for bash history)
            elif key == pyqt.Qt.Key_Up:
                text = "\x1b[A"
            elif key == pyqt.Qt.Key_Down:
                text = "\x1b[B"
            elif key == pyqt.Qt.Key_Right:
                text = "\x1b[C"
            elif key == pyqt.Qt.Key_Left:
                text = "\x1b[D"

        if text:
            os.write(self.master_fd, text.encode("utf-8"))

    def on_finished(self):
        self.insertPlainText("\n[Process finished]\n")
        self.setReadOnly(True)

    def resizeEvent(self, event):
        """Handle terminal resizing."""
        super(NchantdTerminalView, self).resizeEvent(event)
        self._update_pty_size()

    def _update_pty_size(self):
        # Calculate rows and cols based on widget size and font metrics
        metrics = self.fontMetrics()
        width = self.viewport().width()
        height = self.viewport().height()

        cols = max(1, width // metrics.horizontalAdvance("W"))
        rows = max(1, height // metrics.lineSpacing())

        buf = array.array("h", [rows, cols, 0, 0])
        try:
            fcntl.ioctl(self.master_fd, termios.TIOCSWINSZ, buf)
        except OSError:
            pass


class NchantdTerminalEmbed(NchantdWidget):
    """ """

    def __init__(self, app, cfg, parent=None):
        """'"""
        super(NchantdTerminalEmbed, self).__init__(parent, cfg)
        self.app = app
        self.initWidget()

    def initModel(self):
        """ """
        return self

    def initView(self):
        """ """
        return self

    def initWidget(self):
        """ """
        self.layout = pyqt.QVBoxLayout()
        self.terminal = NchantdTerminalView(self)
        self.layout.addWidget(self.terminal)
        self.setLayout(self.layout)

        # Start the shell
        shell = self.config.dikt.get("shell", "/bin/bash")
        self.terminal.start_shell(shell)
        return self
