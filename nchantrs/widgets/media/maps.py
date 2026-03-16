# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""  #																			||
---  #																			||
<(META)>:  #																	||
	docid:   #																	||
	name:	#																	||
	description: >  #															||

	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	path: <[LEXIvrs]>  #														||
	outline: <[outline]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
"""  # ||
# -*- coding: utf-8 -*-#														||
# ================================Core Modules===================================||
from os.path import abspath, dirname, join

# ===============================================================================||
from condor import condor

import logging
from ogma.logma import Logma

logger = logging.getLogger(__name__)

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ===============================================================================||
pxcfg = join(here, "_data_", "maps.yaml")
pxcfg = {}


class NchantdMap:
    """ """

    def __init__(self, item, nid, df=DataFrame(), parent=None):
        """ """
        self.parent = parent
        if parent:
            cfg = self.parent.config
        self.config = condor.Instruct(pxcfg).select("NchantdItem")
        self.config.override(cfg)
        super(NchantdItem, self).__init__(parent)
        self.model = NchantdMapModel(self)
        self.view = NchantdMapView(self)

    def initModel(self):
        """ """
        return self

    def initView(self):
        """ """
        self.view.initView(self)
        self.setLayout(self.view.layout)
        return self

    def initWidget(self):
        """ """
        self.model()
        self.view()
        return self


class NchantdMindMap:
    """Provide a Canvas area to place and arrange nodes for defining a mind map"""

    def __init__(self, item, nid, df=DataFrame(), parent=None):
        """ """
        self.parent = parent
        if parent:
            cfg = self.parent.config
        self.config = condor.Instruct(pxcfg).select("NchantdItem")
        self.config.override(cfg)
        super(NchantdItem, self).__init__(parent)
        self.model = NchantdMapModel(self)
        self.view = NchantdMapView(self)

    def initModel(self):
        """ """
        return self

    def initView(self):
        """ """
        self.view.initView(self)
        self.setLayout(self.view.layout)
        return self

    def initWidget(self):
        """ """
        self.model()
        self.view()
        return self


# ===========================Code Source Examples================================||
"""
"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
