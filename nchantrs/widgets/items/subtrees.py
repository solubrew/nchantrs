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
from os.path import dirname, join

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor

import logging
from _work.subtreemodels import NchantdProjectSubTreeModel

logger = logging.getLogger(__name__)
from kahndor.logma import Logma
from typing import Optional, Dict, List, Any, Tuple

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class NchantdSubTree:
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdSubTree")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdSubTree, self).__init__(self.parent, self.config)

    def initModel(self) -> None:
        """"""
        return self

    def initView(self) -> None:
        """"""
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
        self.config = kahndor.Instruct(pxcfg).select("NchantdProjectSubTree")
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
        """"""
        # self.view.initView()
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
        self.config = kahndor.Instruct(pxcfg).select("NchantdFileSystemSubTree")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdFileSystemSubTree, self).__init__(self.parent, self.config)

    def initModel(self) -> None:
        """"""
        return self

    def initView(self) -> None:
        """"""
        return self

    def initWidget(self) -> None:
        """"""
        self.initModel()
        self.initView()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
