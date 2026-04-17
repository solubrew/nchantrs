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
from typing import Any, Dict, Optional

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from elv1r4.keys.keys import createPrivateKey
from kahndor.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class Bond:
    """"""

    def __init__(self) -> None:
        """"""
        logma.debug("Bond initialized")


class EthereumBond(Bond):
    """Leverage the Totems Project on Ethereum to ensure distributed consistency of software by providing
    hashes ideally the application will use multiple bonds across multiple L1 sources
    also integrate the NFT and public key setting function
    """

    def __init__(self, parent: Any, cfg: Optional[Dict[str, Any]] = None) -> None:
        """"""
        logma.info("Initializing EthereumBond")
        self.config = kahndor.Instruct(parent)
        if parent is not None:
            self.config.override(parent.config)
        self.parent = parent
        self.config.override(cfg)
        self._generate_nchantd_public_address()
        logma.info("EthereumBond initialized successfully")

    def _generate_nchantd_public_address(self) -> "EthereumBond":
        """"""
        logma.debug("Generating Ethereum public address")
        key, addr = createPrivateKey()
        self.parent.model.store.secure_write("ethereum_bond", {key: addr})
        logma.info(f"Ethereum bond created with address: {addr[:10]}...")
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
