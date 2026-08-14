import sys

from kahndor import kahndor
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from nchantrs.widgets.embeds import NchantdTerminalEmbed


def main():
    app = QApplication(sys.argv)

    # Mock config
    cfg = {"shell": "/bin/bash", "paneviews": {}}

    window = QMainWindow()
    window.setWindowTitle("NchantdTerminalEmbed Demo")
    window.resize(800, 600)

    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    # We need a mock 'app' object if NchantdTerminalEmbed expects one with specific attributes
    class MockApp:
        def __init__(self):
            self.config = kahndor.Instruct({})

    mock_app = MockApp()

    terminal_embed = NchantdTerminalEmbed(mock_app, cfg)
    layout.addWidget(terminal_embed)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
