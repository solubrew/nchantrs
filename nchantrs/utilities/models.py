# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name: Nchantrs Model Utilities
        description: >
                Utilities for combining and processing model records in nchantrs applications.

        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from __future__ import annotations

import logging
from os.path import abspath, dirname, join
import datetime as dt
from typing import Any, Optional

# ======================================3rd Party Library Modules======================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma: Logma = Logma(__name__)
logma.off()
debug: bool = True

# Configure module logger
logger: logging.Logger = logging.getLogger(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "models.yaml")


def combine_records(objects: dict[str, Any], object_type: str = "table") -> dict[str, Any]:
    """Combine records from multiple sources into a unified structure.

    Args:
            objects: Dictionary containing view, index, and object_type data
            object_type: The type of objects to combine (default: 'table')

    Returns:
            Dictionary with combined records
    """
    views = objects.get("view", {})
    index = objects.get("index", {})
    objects = objects.get(object_type, {})
    if objects is None:
        return {}
    for table in objects:
        logma.info(f"Table {table}")
        if table not in objects.keys():
            logma.warning(f"Table {table} not in objects")
            continue
        if not objects[table].get("records"):
            objects[table]["records"] = []
        objects[table]["records"] += objects[table].get("system_records", [])
    return {object_type: objects, "view": views, "index": index}


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
