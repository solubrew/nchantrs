# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name:
	description: >
		upgrades will need to work with a live nid system this will require the handling of appnodes differently than
		usernodes
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
from typing import Optional, Dict, List, Any, Tuple

import logging


logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import pyqt
from ogma.logma import Logma

# Optional imports for pull_updates - may not be available
try:
    from squirl.orgnql.fonql import RestAPI
except ImportError:
    RestAPI = None

# Constants for upgrade status
DONE = "done"

# Security level constants
SEC_LEVEL_5 = "seclvl5"
SEC_LEVEL_4 = "seclvl4"
SEC_LEVEL_3 = "seclvl3"
SEC_LEVEL_2 = "seclvl2"
SEC_LEVEL_1 = "seclvl1"
SEC_LEVEL_0 = "seclvl0"

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "upgrades.yaml")


def version_check() -> None:
    """"""
    pass
    # [DONE] connect to a service/contract and check for the most recent version


#   #  offer to upgrade if a newer version is available


class UpgradeManager(object):
    """"""

    def __init__(self, parent=None, cfg=None):
        """"""
        self.config = condor.instruct(pxcfg).select("").override(cfg)
        self.parent = parent
        self.current_version = None
        self.app = pyqt.QApplication.instance()

    def check_for_updates(self) -> None:
        """"""
        upgrades = self.send_request()
        if "security" in upgrades:
            self.run_upgrade_security_protocol(upgrades["security"])
        elif "general" in upgrades:
            self.run_upgrade_protocol(upgrades["general"])
        elif "paid" in upgrades:
            self.run_upgrade_paid_protocl(upgrades["paid"])

    def pull_updates(self) -> None:
        """"""
        if RestAPI is None:
            logma.warning("RestAPI not available for pull_updates")
            return
        url = "https://api.nchantrs.com/"
        src = RestAPI(url)
        updates = src.get("/updates")
        if updates:
            data = updates["preupdate"]["data"]
            if data is None:
                self.app.store.update_data(data)
            if updates["application"] is True:
                self.app.update(updates)
            data = updates["postupdate"]["data"]
            if data is None:
                self.app.store.update_data(data)

    def run_upgrade_protocol(self, upgrades: dict) -> None:
        """"""
        self._begin_upgrade()
        # download upgrades
        # create temporary directory for the application
        # copy current program to temp directory
        # restart program from the temp directory
        # remove the standard program
        # copy upgraded program to standard location
        # restart from new program from standard location
        # verify everything is functional
        # remove temp directory
        self._finalize_upgrade()

    def run_upgrade_unpaid_protocol(self, upgrades: dict) -> None:
        """"""

    def run_upgrade_paid_protocol(self, upgrades: dict) -> None:
        """"""

    def run_upgrade_security_protocol(self, upgrades: dict) -> None:
        """"""
        if upgrades["security"] == SEC_LEVEL_5:
            # [DONE] stop all functions related to web traffic even with nchantrs servers
            pass
        elif upgrades["security"] == SEC_LEVEL_4:
            # [DONE] stop all functions except connections to nchantrs servers
            pass
        elif upgrades["security"] == SEC_LEVEL_3:
            # [DONE]
            pass
        elif upgrades["security"] == SEC_LEVEL_2:
            # [DONE]
            pass
        elif upgrades["security"] == SEC_LEVEL_1:
            # [DONE] wait for low usage period below 50% of standard
            pass
        elif upgrades["security"] == SEC_LEVEL_0:
            # [DONE] wait for limited usage period below 25% of standard
            pass

    def run_protocol(self, upgrades: dict) -> bool:
        """"""
        lock = False
        if upgrades["code"]:
            if UpgradeCode().run(upgrades["code"]):
                lock = True
        if lock:
            lock = False
            if upgrades["file"]:
                if UpgradeFile().run(upgrades["file"]):
                    lock = True
        if lock:
            lock = False
            if upgrades["database"]:
                if UpgradeDatabase().run(upgrades["database"]):
                    lock = True
        if lock:
            lock = False
            if upgrades["table"]:
                if UpgradeDatabaseTable().run(upgrades["table"]):
                    lock = True
        if lock:
            lock = False
            if upgrades["view"]:
                if UpgradeDatabaseView().run(upgrades["view"]):
                    lock = True
        if lock:
            lock = False
            if upgrades["data"]:
                if UpgradeDatabaseData().run(upgrades["data"]):
                    lock = True

    def send_request(self) -> dict:
        """"""
        upgrades = {}
        {"upgrades": self.current_version}
        return upgrades

    def _begin_upgrade(self) -> None:
        """"""
        self.app.model.store_history()

    def _finalize_upgrade(self) -> None:
        """"""
        # Finalize the upgrade process
        pass


class UpgradeCode(object):
    """Upgrade code need to investigate general upgrade process of python"""

    def __init__(self):
        """"""
        pass

    def run(self, code):
        """Execute upgrade code"""
        return True

    def download_new_code(self):
        """"""
        pass

    def unzip_downloaded_code(self):
        """"""
        pass

    def run_unzipped_executable(self):
        """"""

    def move_old_code(self):
        """"""
        pass

    def verify_new_code(self):
        """"""
        pass

    def remove_old_code(self):
        """"""
        pass


class UpgradeDatabaseData(object):
    """"""

    def __init__(self):
        """"""
        self.appnodes = []
        self.usernodes = []
        self.virtualnodes = []

    def add_appnode(self, appnode):
        """"""
        pass

    def add_tab(self, tab):
        """"""
        pass

    def add_usernode(self, usernode):
        """"""
        pass

    def add_virtualnode(self, virtualnode):
        """"""
        pass

    def remove_appnode(self, appnode):
        """"""
        pass

    def remove_tab(self, tab):
        """"""
        pass

    def remove_usernode(self, usernode):
        """"""
        pass

    def remove_virtualnode(self, virtualnode):
        """"""
        pass


class UpgradeDatabase(object):
    """Upgrade database allowing for replacement of the sqlite db file and/or upgrading to a different database"""

    def __init__(self):
        """"""
        pass

    def backup_database(self):
        """"""
        pass

    def collect_table_structure(self):
        """"""
        pass

    def replicate_table_structure(self):
        """"""
        pass

    def copy_data(self):
        """"""
        pass

    def verify_data(self):
        """"""
        pass

    def remove_backup(self):
        """"""
        pass


class UpgradeFile(object):
    """Change the location on disk and/or contents of static files used in the Nchantrs application"""

    def __init__(self):
        """"""
        pass


class UpgradeIndex(object):
    """Add and/or Remove an Index from the database/s used by the Nchantrs application"""

    def __init__(self):
        """"""
        pass


class UpgradeKey(object):
    """"""

    def __init__(self):
        """"""
        pass


class UpgradeDatabaseTable(object):
    """Add, Remove and/or Modify a Table from the database/s used by the Nchantrs application."""

    def __init__(self, name=None):
        """"""
        self.name = name

    def run(self, data):
        """Execute table upgrade"""
        return True

    def add_column(self):
        """"""
        pass

    def remove_column(self):
        """"""
        pass

    def rename_column(self):
        """"""
        pass

    def rename_table(self):
        """"""
        pass


class UpgradeDatabaseView(object):
    """Add and/or Remove a View from the database/s used by the Nchantrs application"""

    def __init__(self):
        """"""

    def copy_view_statement(self):
        """"""
        pass

    def delete_view(self):
        """"""
        pass

    def create_view(self):
        """"""
        pass

    def verify_view(self):
        """"""
        pass

    def remove_view_statement(self):
        """"""
        pass


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
