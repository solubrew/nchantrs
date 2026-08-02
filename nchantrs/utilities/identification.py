"""
---
<(META)>:
        docid:
        name: Nchantrs Identification Utilities
        description: >
                Utilities for creating unique identifiers for nchantrs applications.
                Currently generates UUIDv7 based identifiers.

        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""
from __future__ import annotations
import logging
from os.path import abspath, dirname, join
from typing import Optional
from kahndor import kahndor
from kahndor.logma import Logma
from subtrix import thing
here = join(dirname(__file__), '')
logma: Logma = Logma(__name__)
logma.off()
logger: logging.Logger = logging.getLogger(__name__)
pxcfg = join(here, '_data_', '.yaml')

def create_application_NCDRID() -> str:
    """Create a unique Nchantrs Registry ID (NCDRID).

    This is a mockup for now - it will need to be a service from somewhere.
    Could eventually use a UUIDv7 contract on ethereum with a fee,
    or setup a NchantdApplication registry.

    Returns:
            A unique identifier string
    """
    return thing.What().uuid().ruuid