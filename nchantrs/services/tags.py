"""
---
<(META)>:
        docid:
        name:
        description: >
                Create a system that manages and creates tags that will be used for various organization within the Nchantrs
                Application System
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""
from os.path import abspath, dirname, join
from kahndor import kahndor
import logging
from pandas import DataFrame
from nchantrs.libraries import qpandas
logger = logging.getLogger(__name__)
from kahndor.logma import Logma
import subtrix
here = join(dirname(__file__), '')
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'tags.yaml')

class TagGroup:
    """"""

    def __init__(self, name: str, description: str='', uuid: str=None) -> None:
        """"""
        self.name = name
        self.description = description
        self.uuid = uuid
        if self.uuid is None:
            self.uuid = subtrix.uuid_generator()
        self.tags = {}

class Tag:
    """"""

    def __init__(self, name: str, description: str='', uuid: str=None) -> None:
        """"""
        self.name = name
        self.description = description
        self.uuid = uuid
        if self.uuid is None:
            self.uuid = subtrix.uuid_generator()

    def rename(self, name: str) -> 'Tag':
        """Rename the tag and return self for chaining."""
        logma.info(f'rename called: {self.name} -> {name}')
        self.name = name
        return self

    def storage(self) -> 'qpandas.DataFrame':
        """"""
        columns = ['name', 'description', 'uuid']
        df = DataFrame([[self.name, self.description, self.uuid]], columns=columns)
        return df