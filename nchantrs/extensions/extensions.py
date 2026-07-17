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
from typing import Optional, Dict, List, Any, Tuple
import datetime as dt

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.extensions.install import NchantdExtensionLoader
from nchantrs.widgets.groups import NchantdHScrollGroupBox, NchantdVScrollGroupBox

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "extensions.yaml")

#
# class NchantdExtensionsManager(object):
#     """"""
#
#     def __init__(self, parent, cfg=None) -> None:
#         """"""
#         self.app = parent
#         self.config = kahndor.Instruct(pxcfg).select("NchantdExtensionsManager").override(cfg)


class NchantdExtensionsManager(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        super().__init__(parent)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdExtensionManagerTab").override(cfg))
        self.primary_settings_group = None
        self.extension_loader = NchantdExtensionLoader()

    def initModel(self) -> None:
        """"""
        super().initModel()
        return self

    def initView(self) -> None:
        """
        Show each extension that is currently installed and its status
        have a button to launch a temp tab that loads any specific information or settings for the selected extension

        :return:
        """
        super().initView()
        self.primary_settings_group = NchantdVScrollGroupBox()
        self.primary_settings_group.setTitle("Extensions")
        self.layout.addLayout(self.primary_settings_group.layout)
        # Create UI components
        # self.extension_list = NchantdList()
        # cfg = {"text": "Load Extensnion"}
        # self.load_button = NchantdButton(self, cfg)
        #
        # # Populate the list with available extensions
        # for ext in self.extension_loader.list_extensions():
        #     self.extension_list.addItem(ext)
        #
        # self.layout.addWidget(self.extension_list)
        # self.layout.addWidget(self.load_button)
        #
        # # Connect signal
        # self.load_button.clicked.connect(self.load_selected_extension)
        return self

    def load_selected_extension(self) -> None:
        """"""
        ext_name = self.extension_list.currentItem().text()
        self.extension_loader.load_extension(ext_name)


def load_extension():
    """use the wizard class"""


def load_extensions(dir_):
    """"""
    plugins = []
    for filename in listdir(dir_):
        if filename.endswith(".py"):
            spec = importlib.util.spec_from_file_location(filename[:-3], join(dir_, filename))
            plugin = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin)
            plugins.append(plugin)
    return plugins


def decompress_extension():
    """"""


def register_extension():
    """register the extension"""


def remove_extension():
    """use the wizard class"""


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
