"""
---
<(META)>:
        docid:
        name:
        description: >
                Setup connections for each outside data service that the Nchantrs system will use.  This will leverage the
                Worldbridge Stone system
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""
from os.path import abspath, dirname, join
from kahndor import kahndor
import logging
from kahndor.logma import Logma
logger = logging.getLogger(__name__)
here = join(dirname(__file__), '')
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')

class NchantdConnections(object):
    """"""

    def __init__(self) -> None:
        """"""
        self.connections = {}
        logma.info(f'NchantdConnections initialized')

    def connect_to_database(self, name: str=None) -> 'NchantdConnections':
        """Allow for adhoc connecting to multiple databases"""
        if 'db' not in self.connections:
            self.connections['db'] = {}
        return self

    def connect_to_google(self) -> 'NchantdConnections':
        logma.info(f'connect_to_google called')
        return self

    def connect_to_wikipedia(self) -> 'NchantdConnections':
        logma.info(f'connect_to_wikipedia called')
        return self

    def connect_to_wrlok(self) -> 'NchantdConnections':
        """Nchantrs native data source for a consolidated data experience"""
        if 'wrlok' not in self.connections:
            self.connections['wrlok'] = {}
        self.available_extensions = ['NchantdApplicationExport']
        return self