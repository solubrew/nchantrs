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
from typing import Optional, Dict, List, Any, Tuple

import logging


logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import pyqt
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "files.yaml")


class NchantdFileOpenSigil(pyqt.QFileDialog):
    """"""

    def __init__(self, name, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent.app.main)
        name = "open"
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdFileOpenSigil")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.init_variables(name)
        self.file_selected = None

    def init_variables(self, name="generic") -> None:
        """"""
        self.layout = None
        self.pane = None
        self.ok = None
        self.buttons = None
        self.new = True
        self.open = False
        self.app = pyqt.QApplication.instance()
        self.dtop = self.config.dikt["gui"]["dialogs"].get(name, None)
        if self.dtop is None:
            self.dtop = self.config.dikt["gui"]["dialogs"]["base"]
        # self.model = self.parent.model
        self.new_form_field = None
        self.new_form_field_style = None
        self.add_field_button = None
        return self

    def initModel(self) -> None:
        """"""
        # super().initModel()
        # Set the dialog to open file mode
        self.setFileMode(pyqt.QFileDialog.ExistingFile)
        return self

    def initView(self) -> None:
        """"""
        # super().initView()
        self.setGeometry(150, 250, 1000, 600)
        # self.hide_title()
        self.setNameFilter("All Files (*)")
        return self

    def initWidget(self) -> None:
        """"""
        self.initModel()
        self.initView()
        self.run()
        return self

    def accept(self) -> None:
        """"""
        super().accept()
        self.set_ok()
        # super().accept_()
        if self.ok:
            self.file_selected = self.selectedFiles()[0]
            logma.info(f"{self.file_selected}")
        return self.file_selected

    def reject(self) -> None:
        """"""
        super().reject()

    def run(self) -> None:
        """"""
        self.exec()

    def set_filters_files(self, gfilters=None) -> None:
        """"""
        filters = []
        if gfilters is None:
            filters = ["All Files (*)"]
        else:
            for gfilter in gfilters:
                match gfilter:
                    case "txt":
                        filters.append("Text Files (*.txt)")
                    case "html":
                        filters.append("HTML Files (*.html)")
                    case "png":
                        filters.append("Images (*.png)")
                    case "jpg":
                        filters.append("Images (*.jpg)")
                    case "jpeg":
                        filters.append("Images (*.jpeg)")
                    case "py":
                        filters.append("Python Files (*.py)")
        self.setNameFilters(filters)
        return self

    def set_ok(self) -> None:
        """"""
        self.ok = True
        return self


class AskSaveDialog:
    """Ask to save when a user navigates away from a changed data point"""

    def __init__(self) -> None:
        """"""

    def initModel(self) -> None:
        """"""

    def initView(self) -> None:
        """"""

    def initWidget(self) -> None:
        """"""


class SaveAsDialog:
    """standard save as dialog to allow for the file to be create as a duplicate of the current file"""

    def __init__(self) -> None:
        """"""

    def initModel(self) -> None:
        """"""

    def initView(self) -> None:
        """"""

    def initWidget(self) -> None:
        """"""


class SaveCopy:
    """Allow a copy of the current file to be created but the current file stays open this is useful for
    archiving/versioning on the fly"""

    def __init__(self, parent, cfg=None) -> None:
        """"""
        self.config = condor.Instruct(pxcfg)
        if parent is not None:
            self.config.override(parent.config)
        self.parent = parent
        self.config.override(cfg)
        super().__init__(parent, self.config)

    def initModel(self) -> None:
        """"""

    def initView(self) -> None:
        """"""

    def initWidget(self) -> None:
        """"""


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
