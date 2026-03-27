# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Distortion Test App
	description: >
		Example of distortion (L2) entry point - complex single widget dialog
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
import sys
from os.path import dirname, join

# Add nchantrs to path
here = join(dirname(__file__), "")
sys.path.insert(0, here)

from nchantrs.nchantrs import distortion


class TestComplexWidget:
    """Complex test widget for distortion"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.widget = None
    
    def initWidget(self):
        """Initialize a complex widget with multiple elements"""
        from nchantrs.libraries import pyqt
        from PySide6 import QtWidgets
        
        # Create a container widget
        container = pyqt.QWidget()
        layout = pyqt.QVBoxLayout()
        
        # Add title
        title = pyqt.QLabel("Distortion Test - L2 Entry Point")
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Add some input fields
        input_layout = pyqt.QHBoxLayout()
        input_layout.addWidget(pyqt.QLabel("Name:"))
        name_input = pyqt.QLineEdit()
        name_input.setPlaceholderText("Enter name...")
        input_layout.addWidget(name_input)
        layout.addLayout(input_layout)
        
        # Add a button
        button = pyqt.QPushButton("Click Me")
        button.setStyleSheet("padding: 10px; margin: 10px;")
        layout.addWidget(button)
        
        # Add some text
        info = pyqt.QLabel("Distortion supports complex single widget dialogs with multiple controls.")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        container.setLayout(layout)
        self.widget = container
        return self.widget


if __name__ == "__main__":
    print("="*60)
    print("Testing Distortion (L2 Entry Point)")
    print("="*60)
    
    # Create widget class for distortion
    widget = TestComplexWidget
    
    # Call distortion entry point
    distortion(
        name="Test Distortion",
        args=sys.argv,
        widget=widget,
        instance=None,
        cfg={"title": "Distortion Test"}
    )
    
    print("Distortion complete")
