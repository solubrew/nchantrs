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
import json as j

import logging


logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from subtrix.utilities import uuid
from typing import Optional, Dict, List, Any, Tuple

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "policies.yaml")


class NchantdDataPolicy(object):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdDataPolicy").override(cfg)
        self.policies = None
        self.retention_polices = None

    def check_policies(self) -> None:
        """"""
        tables = self.parent.app.model.get_tables()
        for table in tables:
            retention_cutoff = self.check_retention_policy(table)
            if retention_cutoff is not None:
                self.clear_data(table, retention_cutoff)
                self.parent.app.model.store_app_event("running", "clear_data")

    def check_retention_policy(self, target) -> None:
        """"""
        policy_record = self.retention_polices[self.retention_polices["target"] == target]
        if not policy_record.empty():
            policy = j.loads(policy_record["policy"].values.tolist()[0])
            if policy.get("hold", "") == "indefinite":
                return
            if policy.get("hold", "") == "temporary":
                days = policy.get("days", 0)
                cutoff_date = dt.datetime.now() - dt.timedelta(days=days)
                return cutoff_date
            self.parent.app.model.store_app_event("running", "policy_unknown")

    def clear_data(self, target, cutoff_date) -> None:
        """"""
        self.parent.app.model.remove_data_by_date(target, cutoff_date, "before")

    def get_policies(self) -> None:
        """"""
        self.policies = self.parent.app.model.get_app_policies()
        self.retention_polices = self.policies[self.policies["type"] == "Data Retention Policy"]
        return self

    def init_policies(self, history_days=90) -> None:
        """"""
        self.set_app_collection_retention_policy(history_days)
        self.set_app_event_retention_policy(history_days)
        self.set_app_history_retention_policy(history_days)
        self.set_app_tag_retention_policy(history_days)
        self.set_app_tag_group_retention_policy(history_days)
        self.set_app_user_retention_policy(history_days)

    def set_app_collection_retention_policy(self, days=90) -> None:
        """"""
        policy = {"hold": "temporary", "days": days}
        record = [uuid(), "Data Retention Policy", "app_collection", j.dumps(policy)]
        self.parent.store_app_policy(record)

    def set_app_event_retention_policy(self, days=90) -> None:
        """"""
        policy = {"hold": "temporary", "days": days}
        record = [uuid(), "Data Retention Policy", "app_event", j.dumps(policy)]
        self.parent.store_app_policy(record)

    def set_app_history_retention_policy(self, days=90) -> None:
        """"""
        policy = {"hold": "temporary", "days": days}
        record = [uuid(), "Data Retention Policy", "app_history", j.dumps(policy)]
        self.parent.store_app_policy(record)

    def set_app_tag_retention_policy(self, days=90) -> None:
        """"""
        policy = {"hold": "temporary", "days": days}
        record = [uuid(), "Data Retention Policy", "app_tag", j.dumps(policy)]
        self.parent.store_app_policy(record)

    def set_app_tag_group_retention_policy(self, days=90) -> None:
        """"""
        policy = {"hold": "temporary", "days": days}
        record = [uuid(), "Data Retention Policy", "app_tag_group", j.dumps(policy)]
        self.parent.store_app_policy(record)

    def set_app_user_retention_policy(self, days=90) -> None:
        """"""
        policy = {"hold": "temporary", "days": days}
        record = [uuid(), "Data Retention Policy", "app_user", j.dumps(policy)]
        self.parent.store_app_policy(record)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
