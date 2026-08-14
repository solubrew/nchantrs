import os
import sys

from kahndor import kahndor
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

from nchantrs.widgets.embeds import NchantdTerminalEmbed


def main():
    app = QApplication(sys.argv)

    # Mock config
    cfg = {"shell": "/bin/bash", "paneviews": {}}

    window = QMainWindow()
    window.setWindowTitle("NchantdTerminal ANSI Test")
    window.resize(800, 600)

    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    class MockApp:
        def __init__(self):
            self.config = kahndor.Instruct({})

    mock_app = MockApp()

    terminal_embed = NchantdTerminalEmbed(mock_app, cfg)
    layout.addWidget(terminal_embed)

    def run_repro():
        repro_path = os.path.join(os.path.dirname(__file__), "repro_ansi.py")
        cmd = f"python3 {repro_path}\n"
        terminal_embed.terminal.master_fd
        os.write(terminal_embed.terminal.master_fd, cmd.encode())

    btn = QPushButton("Run ANSI Test")
    btn.clicked.connect(run_repro)
    layout.addWidget(btn)

    window.show()

    # If in headless environment, we might just want to check if it compiles and runs briefly
    if os.environ.get("QT_QPA_PLATFORM") == "offscreen":
        print("Running in offscreen mode, will exit after 2 seconds")
        from PySide6.QtCore import QTimer

        QTimer.singleShot(2000, run_repro)
        QTimer.singleShot(5000, app.quit)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
