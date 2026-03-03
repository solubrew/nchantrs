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
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
logma.off()
debug = True

# ====================================================================================================================||
pxcfg = join(here, "_data_", "models.yaml")


def combine_records(objects, object_type="table"):
    """"""
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
