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
from os.path import abspath, dirname, join, exists
from typing import Optional, Dict, List, Any, Tuple
from os import listdir
import datetime as dt
import json as j
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from nchantrs.libraries import pyqt
from kahndor.logma import Logma
from squirl.orgnql import yonql
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'install.yaml')

class NchantdExtensionLoader(pyqt.QObject):

    def __init__(self, parent=None, cfg=None) -> None:
        self.config = kahndor.Instruct(pxcfg).select('NchantdExtensionLoader').override(cfg)
        super().__init__()
        self.loaded_extensions = []
        self.extensions_path = self.config.dikt.get('extensions_path', None)
        if self.extensions_path is None:
            self.extensions_path = ''
        self.manifest = None
        logma.info(f'NchantdExtensionLoader initialized')

    def load_extension(self, name) -> None:
        """
        Load an extension given its name.
        """
        extension_path = join(self.extensions_path, name)
        manifest_path = join(extension_path, 'manifest.json')
        self.load_manifest(manifest_path)
        return self

    def load_manifest(self, manifest_path) -> None:
        """"""
        manifest = yonql.Doc(manifest_path)
        next(self.manifest.read())
        self.manifest = manifest.dikt
        return self

    def inject_script(self, js_code) -> None:
        """
        Inject JavaScript into the WebView.
        """
        self.browser.page().runJavaScript(js_code)

    def execute_background_script(self, js_code) -> None:
        """
        Execute a background script in the context of Python (as an event-driven task).
        """
        exec(js_code, globals())

    def list_extensions(self) -> None:
        """
        Return a list of available extensions.
        """
        return listdir(self.extensions_path)

    def validate_extension(self, name) -> None:
        """check to ensure file structure is valid and all required files are present"""
        if not exists(manifest_path):
            raise FileNotFoundError(f'Manifest not found for extension: {name}')
        with open(manifest_path, 'r') as f:
            manifest = j.load(f)
            self.loaded_extensions[name] = manifest
        if 'content_scripts' in manifest:
            for script in manifest['content_scripts']:
                script_path = join(extension_path, script)
                with open(script_path, 'r') as script_file:
                    js_code = script_file.read()
                    self.inject_script(js_code)
        if 'background' in manifest:
            bg_script_path = join(extension_path, manifest['background'])
            with open(bg_script_path, 'r') as script_file:
                js_code = script_file.read()
                self.execute_background_script(js_code)
        logger.info(f'Extension {name} loaded successfully!')

    def verify_extension(self, name) -> None:
        logma.info(f'verify_extension called')
        return self