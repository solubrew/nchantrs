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
from os.path import abspath, dirname, join, realpath
import sys
import hashlib
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from kahndor.logma import Logma
from squirl.orgnql.fonql import calculate_hash
here = join(dirname(__file__), '')
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'integrity.yaml')
HASH_VERIFY_SUCCESS = True
HASH_VERIFY_FAIL = False

def exectuableHash() -> 'None':
    """Calculate hash of the current executable."""
    start_dir = dirname(realpath(sys.executable))
    start_file_name = realpath(sys.executable)
    start_file_name_hash = calculate_hash(start_file_name)

class Integrity(object):
    """A class to check the integrity of files within the license chain to verify that the specific application is
    controlled by a known apikey for control of data and potentially verification of NFTs"""

    def __init__(self, cfg: None=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select('Integrity').override(cfg)
        self.interpreter_type = None
        self.interpreter_path = None
        self.interpreter_file = None
        self.interpreter_hash = None
        self.module_hashes = {}
        logma.info(f'Integrity initialized')

    def addModules(self) -> None:
        """Add Modules and their paths to the list of modules/files needing to be hashed use for both development and
        to leveraged in an addon system to allow the addons to verify their own code"""
        pass

    def hashInterpreter(self) -> None:
        """Hash the Python interpreter"""
        pass

    def hashFiles(self) -> None:
        module_hashes = {}
        for module, file_ in self.module_hashes.items():
            module_hashes[module] = {}
            for name, path in file_.items():
                module_hashes[module][name] = {'path': path}
                module_hashes[module][name]['hash'] = calculate_hash(path)
        self.module_hashes = module_hashes

    def verifyHashes(self) -> bool:
        """Verify stored hashes against current file hashes"""
        for module, files in self.module_hashes.items():
            for name, file_info in files.items():
                path = file_info['path']
                expected_hash = self.config.get(module, {}).get(name, {}).get('hash')
                if expected_hash:
                    actual_hash = calculate_hash(path)
                    if actual_hash != expected_hash:
                        return HASH_VERIFY_FAIL
        return HASH_VERIFY_SUCCESS