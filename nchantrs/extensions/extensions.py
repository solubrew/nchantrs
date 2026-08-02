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
from os.path import abspath, dirname, join
from typing import Optional, Dict, List, Any, Tuple
import datetime as dt
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.extensions.install import NchantdExtensionLoader
from nchantrs.widgets.groups import NchantdHScrollGroupBox, NchantdVScrollGroupBox
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'extensions.yaml')

class NchantdExtensionsManager(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        super().__init__(parent)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdExtensionManagerTab').override(cfg))
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
        self.primary_settings_group.setTitle('Extensions')
        self.layout.addLayout(self.primary_settings_group.layout)
        return self

    def load_selected_extension(self) -> None:
        """"""
        ext_name = self.extension_list.currentItem().text()
        self.extension_loader.load_extension(ext_name)

def load_extension() -> None:
    logma.info(f'load_extension called')
    return self

def load_extensions(dir_) -> Any:
    """"""
    plugins = []
    for filename in listdir(dir_):
        if filename.endswith('.py'):
            spec = importlib.util.spec_from_file_location(filename[:-3], join(dir_, filename))
            plugin = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin)
            plugins.append(plugin)
    return plugins

def decompress_extension() -> None:
    logma.info(f'decompress_extension called')
    return self

def register_extension() -> None:
    logma.info(f'register_extension called')
    return self

def remove_extension() -> None:
    logma.info(f'remove_extension called')
    return self