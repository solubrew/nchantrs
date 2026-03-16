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
from typing import Optional, Dict, List, Any, Tuple
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from nchantrs.models.models import NchantdInstance

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
debug = True

# ====================================================================================================================||
pxcfg = join(here, "_data_", "db.yaml")


class DBUpdate(object):
    """"""

    def __init__(self, parent, cfg=None) -> None:
        """"""
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("DBUpdate").override(cfg)
        self.versions = self.config.select("versions")
        self.current_version = None
        self.version = None
        self.hold_data = {}
        self.app = parent

    def backup_db(self, db="db") -> None:
        """"""
        data = self.parent.app.model.get_instance(db)
        logma.info(f"Instance: {data}")
        if data.empty:
            raise Exception("No Instance Found")
        data = data.loc[0].to_dict()
        instance = NchantdInstance(self, data)
        logma.info(f"Instance: {instance}")
        self.parent.app.model.set_instance_active(instance)
        logma.info(f"Instance Active: {self.parent.app.model.instance}")
        name = self.parent.model.store.backup_database(self.parent.app.model.instance, db)
        return name

    def check_version(self, current_v) -> None:
        """"""
        logma.info(f"Checking Version {current_v}")
        latest_v = self.get_latest_version()
        logma.info(f"Latest Version: {latest_v}")

        current_parts = self._parse_version_parts(current_v)
        latest_parts = self._parse_version_parts(latest_v)

        for i, (current_level, latest_level) in enumerate(zip(current_parts, latest_parts)):
            logma.info(f"Checking Level {i} {current_level}")
            if current_level == latest_level:
                continue
            return current_level < latest_level

        return False

    def get_data(self, table, db="db") -> None:
        """"""
        return self.parent.app.model.store.get_table(table, None, db)

    def get_latest_version(self) -> None:
        """"""
        self.current_version = self.parent.model.get_current_version()
        max_version = 0
        logma.info(f"Current Version: {self.current_version}")
        logma.info(f"Versions: {self.versions.dikt.keys()}")

        version_data = self.versions.dikt.get(self.current_version)
        if isinstance(version_data, dict):
            for version_key in version_data.keys():
                version_number = int(version_key.replace(".", ""))
                if version_number > max_version:
                    max_version = version_number
        else:
            return self.current_version

        return ".".join([x for x in str(max_version)])[:-1]

    def insert_data(self, table, data, db="db", column_map=None) -> None:
        """"""
        if column_map:
            data = self.map_columns(data, column_map)
        self.parent.app.model.store_records(table, data, db)
        return True

    def map_columns(self, data, column_map) -> None:
        """"""
        for column in column_map.keys():
            data[column_map[column]] = data[column]
            del data[column]
        return data

    def reload_table(self, table, keep, map_, filters, db="db") -> None:
        """"""
        return self.parent.app.model.reload_table(table, keep, map_, filters, db)

    def restore_backup(self, db) -> None:
        """"""
        self.parent.app.model.store.restore_backup(db)
        return True

    def run_updates(self, db) -> None:
        """"""
        current_v = self.parent.model.get_current_version()
        version = current_v
        logma.info(f"Current Version: {current_v}")

        if not self.check_version(current_v):
            logma.info("No updates needed")
            return version

        logma.info("Running Updates")
        updates = self.versions.select(current_v).dikt

        for version_key in updates.keys():
            update_data = updates[version_key]
            if not self._process_single_version_update(version_key, update_data, db):
                break
            version = version_key

        return version

    def run_update_indexes(self, indexes, db="db") -> None:
        """"""
        if indexes is None:
            return True
        # for index, cmd in indexes.items():
        #     self.parent.model.store.create_index(index, cmd, db)
        return True

    def run_update_tables(self, tables, db="db") -> None:
        """"""
        if tables is None:
            return True

        for table, params in tables.items():
            logma.info(f"Updating Table: {table}")

            if not self._process_table_operations(table, params, db):
                return False

        return True

    def run_update_views(self, views, db="db") -> None:
        """"""
        if views is None:
            return True
        for view, cmd in views.items():
            self.parent.store.update_view(view, cmd, db)
        return True

    def update_data(self, update, column, value, db="db") -> None:
        """"""
        self.parent.app.model.store.update_record(update, column, value, db)
        return True

    def _execute_update_step(self, step_name, step_function, step_data, db) -> None:
        """Execute a single update step with error handling and rollback."""
        logma.info(f"Update {step_name}")
        if not step_function(step_data, db):
            logma.error(f"{step_name} failed, restoring backup")
            self.restore_backup(db)
            if debug:
                raise Exception(f"Update Failed: {step_name}")
            return False
        return True

    def _parse_version_parts(self, version_string) -> None:
        """Parse version string into comparable integer parts."""
        logma.info(f"Parsing Version: {version_string}")
        return [part for part in version_string.split(".")]

    def _process_single_version_update(self, version, update_data, db) -> None:
        """Process updates for a single version."""
        logma.info(f"Processing Version {version}")
        if update_data is None:
            return True

        self.backup_db(db)

        # Execute each update step in sequence
        update_steps = [
            ("Tables", self.run_update_tables, update_data.get("tables")),
            ("Indexes", self.run_update_indexes, update_data.get("indexes")),
            ("Views", self.run_update_views, update_data.get("views")),
        ]

        for step_name, step_function, step_data in update_steps:
            if not self._execute_update_step(step_name, step_function, step_data, db):
                return False

        return True

    def _process_table_operations(self, table, params, db) -> None:
        """Process all operations for a single table."""
        # Handle reload operation
        if params.get("reload", False):
            logma.info(f"Reloading Table: {table}")
            map_ = params.get("column-map")
            filters = params.get("filters", {})
            if not self.reload_table(table, params.get("keep-records", False), map_, filters, db):
                if debug:
                    raise Exception("Reload Failed")
                return False

        # Handle update operations
        if params.get("update"):
            if not self._process_table_updates(table, params.get("update"), db):
                return False

        # Handle insert operations
        if params.get("insert"):
            logma.info(f"Inserting: {params.get('insert')}")
            if not self.insert_data(table, params.get("insert"), db):
                if debug:
                    raise Exception("Insert Failed")
                return False

        return True

    def _process_table_updates(self, table, updates, db) -> None:
        """Process update operations for a table."""
        for update in updates:
            logma.info(f"Updating: {update}")
            column = list(update["WHERE"].keys())[0]
            value = update["WHERE"][column]

            if not self.update_data({"table": {table: {"data": update["data"]}}}, column, value, db):
                if debug:
                    raise Exception("Update Failed")
                return False
        return True


#
# class DBUpdate(object):
#     """"""
#
#     def __init__(self, parent, cfg=None) -> None:
#         """"""
#         self.parent = parent
#         self.config = condor.Instruct(pxcfg).select("DBUpdate").override(cfg)
#         self.versions = self.config.select("versions")
#         self.current_version = None
#         self.version = None
#         self.hold_data = {}
#         self.app = parent
#
#     def backup_db(self, db="db") -> None:
#         """"""
#         data = self.parent.app.model.get_instance(db)
#         logma.info(f"Instance: {data}")
#         if data.empty:
#             raise Exception("No Instance Found")
#         data = data.loc[0].to_dict()
#         instance = NchantdInstance(self, data)
#         logma.info(f"Instance: {instance}")
#         self.parent.app.model.set_instance_active(instance)
#         logma.info(f"Instance Active: {self.parent.app.model.instance}")
#         name = self.parent.model.store.backup_database(self.parent.app.model.instance, db)
#         return name
#
#     def check_version(self, current_v) -> None:
#         """"""
#         logma.info(f"Checking Version {current_v}")
#         latest_v = self.get_latest_version().split(".")
#         logma.info(f"Latest Version: {latest_v}")
#         for i, level in enumerate(current_v.split(".")):
#             logma.info(f"Checking Level {i} {level}")
#             if int(level) == int(latest_v[i]):
#                 continue
#             if int(level) < int(latest_v[i]):
#                 return True
#             elif int(level) > int(latest_v[i]):
#                 return False
#
#     def get_data(self, table, db="db") -> None:
#         """"""
#         return self.parent.app.model.store.get_table(table, None, db)
#
#     def get_latest_version(self) -> None:
#         """"""
#         self.current_version = self.parent.model.get_current_version()
#         # if self.current_version is None:
#         #     versions = list(self.versions.dikt.keys())
#         #     versions.sort()
#         #     self.current_version = versions[-1]
#         max = 0
#         logma.info(f"Current Version: {self.current_version}")
#         logma.info(f"Versions: {self.versions.dikt.keys()}")
#         if isinstance(self.versions.dikt[self.current_version], dict):
#             for y in self.versions.dikt[self.current_version].keys():
#                 if int(y.replace(".", "")) > max:
#                     max = int(y.replace(".", ""))
#         else:
#             return self.current_version
#         return ".".join([f"{x}." for x in str(max)])[:-1]
#
#     def insert_data(self, table, data, db="db", column_map=None) -> None:
#         """"""
#         if column_map:
#             data = self.map_columns(data, column_map)
#         self.parent.app.model.store_records(table, data, db)
#         return self
#
#     def map_columns(self, data, column_map) -> None:
#         """"""
#         for column in column_map.keys():
#             data[column_map[column]] = data[column]
#             del data[column]
#         return data
#
#     def reload_table(self, table, keep, map_, filters, db="db") -> None:
#         """"""
#         # # only reload app tables - this makes no sense often doc tables will have to be reloaded but with data keeping
#         # if "app_" != table[:4]:
#         #     return False
#         return self.parent.app.model.reload_table(table, keep, map_, filters, db)
#
#     def restore_backup(self, db) -> None:
#         """"""
#         self.parent.app.model.store.restore_backup(db)
#         return self
#
#     def run_updates(self, db) -> None:
#         """"""
#         current_v = self.parent.model.get_current_version()
#         version = current_v
#         logma.info(f"Current Version: {current_v}")
#         if self.check_version(current_v):
#             logma.info(f"Running Updates")
#             updates = self.versions.select(current_v).dikt
#             for version in updates.keys():
#                 logma.info(f"Checking Version {version}")
#                 update = updates[version]
#                 if update is None:
#                     continue
#                 self.backup_db(db)
#                 logma.info(f"Update Tables")
#                 if not self.run_update_tables(update.get("tables", None), db):
#                     self.restore_backup(db)
#                     if debug:
#                         raise Exception("Update Failed")
#                     break
#                 logma.info(f"Update Indexes")
#                 if not self.run_update_indexes(update.get("indexes", None), db):
#                     self.restore_backup(db)
#                     if debug:
#                         raise Exception("Update Failed")
#                     break
#                 logma.info(f"Update Views")
#                 if not self.run_update_views(update.get("views", None), db):
#                     self.restore_backup(db)
#                     if debug:
#                         raise Exception("Update Failed")
#                     break
#         #self.parent.model.set_current_version(version)
#         return version
#
#     def run_update_indexes(self, indexes, db="db") -> None:
#         """"""
#         if indexes is None:
#             return self
#         # for index, cmd in indexes.items():
#         #     self.parent.model.store.create_index(index, cmd, db)
#         return self
#
#     def run_update_tables(self, tables, db="db") -> None:
#         """"""
#         outcome = True
#         if tables is None:
#             return self
#         for table, params in tables.items():
#             logma.info(f"Updating Table: {table}")
#             if params.get("reload", False):
#                 logma.info(f"Reloading Table: {table}")
#                 map_ = params.get("column-map", None)
#                 filters = params.get("filters", {})
#                 outcome = self.reload_table(table, params.get("keep-records", False), map_, filters, db)
#                 if outcome is False:
#                     if debug:
#                         raise Exception("Reload Failed")
#                     break
#             if params.get("update", None):
#                 updates = params.get("update", None)
#                 for update in updates:
#                     logma.info(f"Updating: {update}")
#                     column = list(update["WHERE"].keys())[0]
#                     value = update["WHERE"][column]
#                     outcome = self.update_data({"table": {table: {"data": update["data"]}}}, column, value, db)
#                     if outcome is False:
#                         if debug:
#                             raise Exception("Update Failed")
#                         break
#             if params.get("insert", None):
#                 logma.info(f"Inserting: {params.get('insert', None)}")
#                 insert = params.get("insert", None)
#                 outcome = self.insert_data(table, insert, db)
#                 if outcome is False:
#                     if debug:
#                         raise Exception("Insert Failed")
#                     break
#         return outcome
#
#     def run_update_views(self, views, db="db") -> None:
#         """"""
#         if views is None:
#             return self
#         for view, cmd in views.items():
#             self.parent.store.update_view(view, cmd, db)
#         return self
#
#     def update_data(self, update, column, value, db="db") -> None:
#         """"""
#         self.parent.app.model.store.update_record(update, column, value, db)
#         return self

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
