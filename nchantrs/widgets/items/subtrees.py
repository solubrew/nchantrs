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
import logging
from os.path import dirname, join

from _work.subtreemodels import NchantdProjectSubTreeModel
from kahndor import kahndor

logger = logging.getLogger(__name__)
from typing import Any, Dict, List, Optional, Tuple

from kahndor.logma import Logma

here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')

class NchantdSubTree:
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdSubTree')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdSubTree, self).__init__(self.parent, self.config)

    def initModel(self) -> None:
        super().initModel()
        logma.info('initModel {type(self).__name__}')
        return self

    def initView(self) -> None:
        super().initView()
        logma.info('initView {type(self).__name__}')
        return self

    def initWidget(self) -> None:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdProjectSubTree(NchantdSubTree):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdProjectSubTree')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdProjectSubTree, self).__init__(self.parent, self.config)
        self.model = NchantdProjectSubTreeModel(self, self.config)

    def initModel(self) -> None:
        """"""
        self.model.initModel()
        return self

    def initView(self) -> None:
        super().initView()
        logma.info('initView {type(self).__name__}')
        return self

    def initWidget(self) -> None:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdFileSystemSubTree(NchantdSubTree):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdFileSystemSubTree')
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdFileSystemSubTree, self).__init__(self.parent, self.config)

    def initModel(self) -> None:
        super().initModel()
        logma.info('initModel {type(self).__name__}')
        return self

    def initView(self) -> None:
        super().initView()
        logma.info('initView {type(self).__name__}')
        return self

    def initWidget(self) -> None:
        """"""
        self.initModel()
        self.initView()
        return self
