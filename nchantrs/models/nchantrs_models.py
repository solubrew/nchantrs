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
from os.path import abspath, dirname, join, exists, getmtime, expanduser
from os import listdir
import inspect
import json as j
import base64

import logging
from typing import Any, Optional


logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||
from pandas import DataFrame
from uuid_extensions import uuid7
import re
import datetime as dt

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

# from squirl.squirl import SQuiRL
# from squirl.orgnql import fonql, conql
from subtrix.subtrix import Mechanism
from subtrix.utilities import uuid
from nchantrs.utilities.models import combine_records
from pycurity.pytime import PyTime
from pycurity.pyhash import encode64, text_hashing_function
from micromole.storage import MicroStash

# ====================================================================================================================||
here = join(dirname(__file__), "")
log = False
debug = True
logma = Logma(__name__)
if log:
    logma.off()

# ====================================================================================================================||
# Constants to avoid magic numbers
DEFAULT_USER_ID: str = "default_user"
MAX_BACKUP_COUNT: int = 5
MAX_ARCHIVE_VERSIONS: int = 3
REMOVE_PATH_FLAGS: int = 3213  # Flag for fonql.removePath()
SETUP_RESET_FLAG: int = 3333  # Flag for setup reset

# Valid operation types
VALID_OPERATIONS: list = ["INSERT", "UPDATE", "DEACTIVATE", "DELETE", "ARCHIVE"]

# Window policy patterns
WINDOW_PATTERN_STR: str = r"(\d+)(DAYS|WEEKS|MONTHS|YEARS)"
WINDOW_UNITS: dict = {"DAYS": "days", "WEEKS": "weeks", "MONTHS": "months", "YEARS": "years"}

# ====================================================================================================================||
pxcfg = join(here, "_data_", "models.yaml")


# OPTIMIZATION 1: Centralized table name resolution with caching
class TableNameResolver:
    """Resolves table names with instance-aware naming - improves maintainability"""

    def __init__(self) -> None:
        self._cache: dict = {}

    def get_table_name(self, base_name: str, instance: Optional["NchantdInstance"] = None) -> str:
        """Get instance-aware table name with caching"""
        cache_key = (base_name, getattr(instance, "alias", None) if instance else None)

        if cache_key in self._cache:
            return self._cache[cache_key]

        if instance is not None and instance.is_independent:
            table_name = f"vwt_{base_name}_{instance.alias}"
        else:
            table_name = f"vw_{base_name}"

        self._cache[cache_key] = table_name
        return table_name

    def clear_cache(self) -> None:
        """Clear cache when instance changes"""
        self._cache.clear()


# OPTIMIZATION 2: Payload validation factory
class PayloadBuilder:
    """Factory for building payloads - eliminates repetitive validation"""

    # Valid operations mapped to default payload structures
    VALID_OPERATIONS: dict = {
        "INSERT": list,
        "UPDATE": list,  # List of dicts
        "DEACTIVATE": list,
        "DELETE": list,
        "ARCHIVE": list,
    }

    @staticmethod
    def validate_and_get_operation(operation: str) -> str:
        """Validate operation and return operation type"""
        if operation not in PayloadBuilder.VALID_OPERATIONS:
            raise ValueError(f"{operation} is not supported. Use: {', '.join(PayloadBuilder.VALID_OPERATIONS.keys())}")
        return operation

    @staticmethod
    def build_cfg_payload(table: str, records: list, columns: Optional[list] = None) -> dict:
        """Build standardized payload config"""
        cfg = {"table": {table: {"records": records}}}
        if columns:
            cfg["table"][table]["columns"] = columns
        return cfg


class WindowPolicyParser:
    """Optimized window policy parser with compiled regex and cached results"""

    WINDOW_PATTERN = re.compile(r"(\d+)(DAYS|WEEKS|MONTHS|YEARS)")
    UNIT_MAP = {"DAYS": "days", "WEEKS": "weeks", "MONTHS": "months", "YEARS": "years"}

    def __init__(self, time_util: Any) -> None:
        self.time = time_util
        self._cache: dict = {}

    def parse(self, window: str) -> tuple:
        """Parse window string once and cache result"""
        if window in self._cache:
            return self._cache[window]

        match = self.WINDOW_PATTERN.match(window)
        if not match:
            raise ValueError(f"Window {window} is not valid. Expected format: 30DAYS, 2WEEKS, etc.")

        value, unit = match.groups()
        result = (int(value), self.UNIT_MAP[unit])
        self._cache[window] = result
        return result

    def check_window_policy(self, timestamp: dt.datetime, window: str) -> bool:
        """Vectorizable window check"""
        value, unit = self.parse(window)
        kwargs = {unit: value}
        return self.time.check_window(timestamp, **kwargs)


class NchantdInstance(object):
    """"""

    def __init__(self, parent: Optional[Any] = None, cfg: Optional[dict] = None) -> None:
        """"""
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdInstance").override(cfg)
        self.alias: Optional[str] = None
        self.application_NCD = parent.app.application_NCD
        self.application_path = parent.app.model.application_path
        self.db_instance_id: Optional[str] = None
        self.dbc_instance_id: Optional[str] = None
        self.description: Optional[str] = None
        self.name = self.config.dikt.get("name_txt", None)
        self.is_independent: bool = False
        self.instance_id: Optional[str] = None
        self.instance_path: Optional[str] = None
        self.is_new: bool = False
        self.is_primary: bool = False
        self.internal: bool = True
        self.set_instance_id(self.config.dikt.get("instance_id_txt", None))
        self.set_instance_path(self.config.dikt.get("instance_path_txt", None))
        self.meta_data: dict = {}
        self.version = self.parent.app.model.get_current_version()

    def get_file_path(self, db: str = "db") -> str:
        """"""
        logma.info(f"get_file_path {self.instance_path}")
        logma.info(f"get_file_path {self.instance_id}")
        if db == "db":
            return join(self.instance_path, f"{self.parent.app.model.slug}{self.parent.app.model.store.EXTENSION}")
        return join(self.instance_path, f"{self.instance_id}{self.parent.app.model.store.EXTENSION}")

    def set_name(self, name: Optional[str] = None) -> "NchantdInstance":
        """"""
        self.name = name
        return self

    def set_instance_id(self, instance_id: Optional[str] = None) -> "NchantdInstance":
        """"""
        if instance_id is None:
            instance_id = uuid()
            self.is_new = True
        self.instance_id = instance_id
        self.db_instance_id = f"dbi_{instance_id}"
        self.dbc_instance_id = f"dbci_{instance_id}"
        self.alias = f"db{instance_id[-len(instance_id) + 10 :].replace('-', '')}"
        return self

    def set_independent(self, state: bool = True) -> "NchantdInstance":
        """"""
        self.is_independent = state
        return self

    def set_instance_path(self, path: Optional[str] = None) -> "NchantdInstance":
        """"""
        if path is None:
            logma.info(f"Get Application Path {self.config.dikt}")
            path = join(expanduser("~"), ".local", "share", self.parent.app.model.slug)
        self.instance_path = path
        logma.info(f"set_instance_path {self.instance_path}")
        return self

    def set_meta_data(self, meta_data: Optional[dict] = None) -> None:
        """"""

    def set_type_external(self) -> "NchantdInstance":
        """"""
        self.internal = False
        return self

    def set_type_internal(self) -> "NchantdInstance":
        """"""
        self.internal = True
        return self


class NchantdStore(MicroStash):
    """
    The Nchantd Store Class is an Subclassof SQuiRL which allows for reading and writing of many different data
    storage formats including SQL, NoSQL, In-Memory, and File based.
    Nchantd Store acts as an interface between the Nchantd Application Model and the underlying data storage.
    Each data record is controlled via its existence,and its status represented by
    ACTIVE_BIT, ARCHIVE_BIT, and DELETE_BIT.
    All records are initialized as ACTIVE_BIT=1,ARCHIVE_BIT=0,DELETE_BIT=0
    All Deletions are completed via a DELETE_BIT flip to 1 there is a DELETE history cleanup process after x number of
    days
    Any Deletion of data marked as with an archive retion policy will be giving a ARCHIVE_BIT fip to 1 instead of
    DELETE_BIT. Records that are used for setting default or conditional values used within the application model will
    be marked as ACTIVE_BIT=1 or ACTIVE_BIT=0 depending on need
    ACTIVE_BIT is used for data that is known to be possibly used in the application at a future date typlically
    non-user data.

    """

    EXTENSION = ".nchnt"

    def __init__(self, name, parent, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("NchantdStore")
        if parent is not None:
            self.config.override(parent.config)
        super().__init__(name, self.config)
        self.config.override(cfg)
        self.parent = parent
        self.instance = self.parent.instance
        self.app = self.parent.app
        # self.application_path = None
        # self.config_path = None
        # self.instance_path = None
        # self.library_path = None
        # self.cache = conql.Doc()
        # self.instances = {}
        # self.resources = []
        # self.slug = None
        # self.time = PyTime()
        # self.user_FK = DEFAULT_USER_ID
        # self.is_verified = False
        self._window_parser = WindowPolicyParser(PyTime())
        self._table_resolver = TableNameResolver()

    # def append_cache(self, df, table):
    #     """"""
    #     self.cache.write_table(df, table, False)
    #     return self
    #
    # def archive_record(self, table, primary_key, db="db"):
    #     """"""
    #     payload = {"WHERE": {"EQUAL": {"UUID": primary_key}}}
    #     self._archive(table, payload, db)
    #     return self
    #
    # def archive_records(self, table, primary_key):
    #     """"""
    #     return self._archive(table, primary_key)
    #
    # def archive_table(self, table):
    #     """"""
    #     self._archive(table)
    #     return self

    # def attach_database(self, instance, objects, db="db"):
    #     """"""
    #     # attach each new database instance to the application database using the db_instance_id as alias
    #     # create a set of views for each attached database
    #     logma.info(f"Attach Database {instance.instance_id} to {db}")
    #     self.docs[db].attach(instance.get_file_path(), instance.alias)
    #     logma.info(f"Create Views {objects['view'].keys()}")
    #     self.create_objects(objects, db, False)
    #     return self
    #
    # def backup_database(self, instance, db="db"):
    #     """"""
    #     name = f".{instance.instance_id}_backup_{self.time.store_now().replace(" ", "")}{self.EXTENSION}"
    #     [DONE]
    #     self.copy_database(instance, name, db)
    #     self.clear_old_backups(instance)
    #     return name

    def cache_app_install(self, key, payload):
        """"""
        self.cache.write({key: payload})
        return self

    def cache_tabs(self, nid, tabn, tabW, dbc="dbc"):
        """"""
        self.docs[dbc].write({nid: {tabn: tabW}})
        return self

    def check_cache(self, table, filter=None):
        """"""
        df = next(self.cache.read(table))
        logma.info(f"DF {df}")
        return df

    def check_window_policy(self, row, window, db):
        """Optimized window policy check (FIX #2: String splitting)"""
        return self._window_parser.check_window_policy(row["MODON_DTTM"], window)

    def cleanup_application_database(self, clear_instances=True, db="db", dbc="dbc"):
        """"""
        self.docs[db].delete_marked()
        self.docs[dbc].clear_cache()
        # add a compaction step
        if clear_instances:
            for db_instance_id in self.docs.keys():
                self.cleanup_instance_database(db_instance_id)
        # self.store_app_event("maintenance", "cleanup_database")
        return self

    def cleanup_instance_database(self, db_instance_id):
        """"""
        self.docs[db_instance_id].delete_marked()
        self.docs[db_instance_id].clear_cache()
        # add a compaction step
        # self.store_app_event("maintenance", f"cleanup_instance_{db_instance_id}")
        return self

    def clear_old_backups(self, instance, keep_n=5):
        """"""
        backups = self.find_backup(instance, "all")
        delete = backups[keep_n:]
        for backup in delete:
            path = join(instance.instance_path, backup)
            if exists(path):
                fonql.removePath(path, REMOVE_PATH_FLAGS)
        return self

    def compact_instances(self):
        """"""

    # def compact_database(self, db="db"):
    #     """"""
    #     # self.backup_database(self.slug, db)
    #     # get each table with records marked as deleted and without a data policy of perm
    #     # sdf = self.get_view_marked_deleted(db)
    #     # if the window for those records is past then delete them from the database
    #     policies = self.get_app_policy({"policy": "Data Retention Policy"}, db)
    #     # policies.apply(self.compact_table, axis=1, args=(df, db))
    #     return self
    #
    # def compact_table(self, row, df, db="db"):
    #     """"""
    #     table = row["target_txt"]
    #     policy = j.loads(row["policy_dict"])
    #     df = df[df["table"] == table]
    #     window = policy.get("window", "30DAYS")
    #     df["remove"] = False
    #     df["remove"] = df.apply(self.check_window_policy, axis=1, args=(window, db))
    #     df = df[df["remove"] == True]
    #     self.docs[db].delete(table, {"WHERE": {"IN": {f"{table}_PK": df["PK"].values.tolist()}}})
    #     return self

    # def convert_database(self, version_from, version_to):
    #     """"""
    #     # Handle structure differences and switching to different database engines
    #     return self
    #
    # def copy_database(self, instance, db_name, db="db"):
    #     """"""
    #     # self.compact_database(db)
    #     logma.info(f"Copy Database {db_name} to {instance.alias}")
    #     logma.info(f"Path {instance.instance_path}")
    #     path = instance.instance_path
    #     # if path is None:
    #     #    path = self.parent.get_
    #     path = join(instance.instance_path, db_name)
    #     logma.info(f"Copy Database {path}")
    #     fonql.fileCopy(instance.get_file_path(), path)
    #     return self
    #
    # def copy_table(self, table, new_table, db="db"):
    #     """"""
    #     return self.docs[db].copy_table(table, new_table)
    #
    # def create_directories(self, path):
    #     """"""
    #     fonql.touch(f"{path}/")
    #     if exists(path):
    #         self.app.model.store.cache_app_install("install", ["create_directory", {"path": path}])
    #         return True
    #     return False

    # def create_objects(self, objects=None, dbs="db", combine=True):
    #     """"""
    #     if objects is None:
    #         logma.warning(f"No Objects")
    #         return self
    #     if not isinstance(dbs, list):
    #         dbs = [dbs]
    #     dbcs = ["dbc"]
    #     for db in dbs:
    #         if db != "db":
    #             dbcs.append(f"dbci_{db}")
    #             db = f"dbi_{db}"
    #         try:
    #             if combine is True and objects is not None:
    #                 objects = combine_records(objects)
    #             if objects is not None:
    #                 self.docs[db].write(objects)
    #         except Exception as e:
    #             logma.warning(e)
    #             if debug:
    #                 raise e
    #     self.clear_objects_config(dbcs, objects)
    #     self.config.override(objects)
    #     return self
    #
    # def clear_objects_config(self, dbcs, objects):
    #     """"""
    #     if objects.get("table", None):
    #         for table in objects.get("table", []):
    #             objects["table"][table]["records"] = []
    #             objects["table"][table]["system_records"] = []
    #     self.config.override({"dstruct": {"database": {"objects": objects}}})
    #     for dbc in dbcs:
    #         if objects.get("table", None):
    #             self.docs[dbc].clear(list(objects.get("table", {}).keys()))

    # def create_tables(self, db="db"):
    #     """"""
    #     return self
    #
    # def create_table(self, table, db="db"):
    #     """"""
    #     logma.info(f"Create Table {table}")
    #     objects = self.parent.config.dikt["dstruct"]["database"]["objects"]["table"]
    #     logma.info(f"Table {objects.keys()}")
    #     return self.docs[db].write({table: objects[table]})
    #
    # def create_views(self, db="db"):
    #     """"""
    #     return self
    #
    # def create_view(self, view, db="db"):
    #     """"""
    #     return self
    #
    # def delete_record(self, table, primary_key=None, uuid=None, column=None, db="db", flip=False):
    #     """"""
    #     if primary_key is not None:
    #         return self._delete_by_primary_key(table, primary_key, db, flip)
    #     if uuid is not None:
    #         return self._delete_by_uuid(table, uuid, column, db, flip)
    #     return None
    #
    # def delete_table(self, table, db="db"):
    #     """"""
    #     self.docs[db].drop(table, "table", 3333)
    #     return self
    #
    # def delete_views(self):
    #     """Delete all views for upgrade purposes"""
    #     views = self.get_views()
    #     views.apply(self.delete_view, axis=1)
    #     return self
    #
    # def delete_view(self, view):
    #     """"""
    #     return self

    # def disconnect(self):
    #     """"""
    #     return self

    def find_backup(self, instance, version):
        """"""
        backups = [x for x in listdir(instance.instance_path) if "_backup_" in x]
        backups.sort(reverse=True)
        if version == "latest":
            backup = backups[0]
        elif version == "all":
            backup = backups
        else:
            backup = [x for x in backups if version == x]
            if len(backup) > 0:
                backup = backups[0]
        return backup

    def gen_NID(self):
        """"""
        return str(uuid())

    # Replace these repetitive methods with the generic versions above:
    def get_app_action(self, cfg, db="db"):
        """Refactored using generic getter"""
        return self._get_app_view_table("app_action", cfg, db)

    def get_app_document_type(self, cfg, db="db"):
        """Refactored using generic getter"""
        return self._get_app_view_table("app_document_type", cfg, db)

    def get_app_event(self, cfg, db="db"):
        """Refactored using generic getter"""
        return self._get_app_view_table("app_event", cfg, db)

    def get_app_tab(self, params, db="db"):
        """Refactored using generic sorted getter"""
        return self._get_sorted_app_view_table("app_tab", params, ["pid_txt", "position_int"], db)

    def get_doc_tab(self, params, db="db"):
        """Refactored using generic sorted getter"""
        return self._get_sorted_app_view_table("doc_tab", params, ["pid_txt", "position_int"], db)

    def get_view_tab(self, cfg, db="db"):
        """Refactored using generic sorted getter"""
        return self

    # def get_app_action(self, cfg, db="db"):
    #     """"""
    #     table = "vw_app_action"
    #     if self.instance is not None:
    #         if self.instance.is_independent:
    #             table = f"vwt_app_action_{self.instance.alias}"
    #     return self.get_table(table, cfg, db)
    #
    # def get_app_document_type(self, cfg, db="db"):
    #     """"""
    #     table = "vw_app_document_type"
    #     if self.instance is not None:
    #         if self.instance.is_independent:
    #             table = f"vwt_app_document_type_{self.instance.alias}"
    #     return self.get_table(table, cfg, db)
    #
    # def get_app_event(self, cfg, db="db"):
    #     """"""
    #     table = "vw_app_event"
    #     if self.instance is not None:
    #         if self.instance.is_independent:
    #             table = f"vwt_app_event_{self.instance.alias}"
    #     return self.get_table(table, cfg, db)

    def get_app_instance(self, instance=None, most_recent=None, db="db"):
        """"""
        table = "vw_app_instance"
        if self.instance is not None:
            if self.instance.is_independent:
                table = f"vwt_app_instance_{self.instance.alias}"
        cfg = {"table": {table: {}}}
        if instance is not None:
            cfg["table"][table] = {"WHERE": {"EQUAL": {"instance_id_txt": instance}}}
        elif most_recent is not None:
            cfg["table"][table] = {"ORDER": {"MODON_DTTM": "DESC"}, "TOP": most_recent}
        else:
            cfg["table"][table] = {"WHERE": {"EQUAL": {"name_txt": db}}}
        df = self.get_table(table, cfg, db)
        return df

    # def get_app_menu(self, tag="app", db="db"):
    #     """"""
    #     table = "vw_app_menu"
    #     if self.instance is not None:
    #         if self.instance.is_independent:
    #             table = f"vwt_app_menu_{self.instance.alias}"
    #     tags = []
    #     tag_ = ""
    #     if "." in tag:
    #         for tg in tag.split("."):
    #             tag_ += f"{tg}"
    #             tags.append(tag_)
    #             tag_ += "."
    #     else:
    #         tags.append(tag)
    #     params = {"WHERE": {"IN": {"tag_txt": tags}}}
    #     return self.get_table(table, params, db)
    # OPTIMIZATION 3: Refactored get_app_menu - O(n) instead of O(n²)
    def get_app_menu(self, tag="app", db="db"):
        """"""
        table = self._table_resolver.get_table_name("app_menu", self.instance)

        # Efficient tag building - single pass O(n)
        tags = self._build_tag_hierarchy(tag)
        params = {"WHERE": {"IN": {"tag_txt": tags}}}
        return self.get_table(table, params, db)

    def get_app_option(self, tags, table="ANY", page_size=None, db="db"):
        """"""
        table = "vw_app_option"
        if self.instance is not None:
            if self.instance.is_independent:
                table = f"vwt_app_option_{self.instance.alias}"
        if not isinstance(tags, list):
            tags = list(tags)
        params = {"WHERE": {"IN": {"tag_txt": tags}, "EQUAL": {"table": table}}}
        reader = self.docs["db"].read(params)
        return next(reader).dikt[table]["df"]

    def get_app_option_key(self, cfg, db="db"):
        """"""
        table = "vw_app_option_key"
        if self.instance is not None:
            if self.instance.is_independent:
                table = f"vwt_app_option_key_{self.instance.alias}"
        return self.get_table(table, cfg, db)

    def get_app_policy(self, cfg, db="db"):
        """"""
        table = "vw_app_policy"
        if self.instance is not None:
            if self.instance.is_independent:
                table = f"vwt_app_policy_{self.instance.alias}"
        return self.get_table(table, cfg, db)

    def get_app_profile(self, db="db"):
        """"""
        cfg = {}
        table = "vw_app_profile"
        if self.instance is not None:
            table = f"vwt_app_profile_{self.instance.alias}"
        return self.get_table(table, cfg, db)

    def get_app_secure_store(self, cfg, db="db"):
        """"""
        caller = inspect.currentframe().f_back.f_back.f_code.co_name
        logma.info(f"Inspect {caller}")
        white_list = [""]
        if caller in white_list:
            table = "vw_app_secure_store"
            df = self.get_table(table, cfg, db)
            df = decrypt(df, self.user.get_password())
        else:
            raise Exception(f"Caller is not Authorized to get data from the secure store")
        return self

    # def get_app_tab(self, params, db="db"):
    #     """"""
    #     table = "vw_app_tab"
    #     if self.instance is not None:
    #         if self.instance.is_independent:
    #             table = f"vwt_app_tab_{self.instance.alias}"
    #     df = self.get_table(table, params, db)
    #     df = df.sort_values(by=["pid_txt", "position_int"])
    #     return df

    def get_app_tree_node(self, cfg, db="db"):
        """"""
        table = "vw_app_tree_node"
        if self.instance.is_independent:
            table = f"vwt_app_tree_node_{self.instance.alias}"
        return self.get_table(table, cfg, db)

    def get_app_user(self, cfg, db="db"):
        """"""
        table = "vw_app_user"
        if self.instance.is_independent:
            table = f"vwt_app_user_{self.instance.alias}"
        return self.get_table(table, cfg, db)

    def get_app_version(self):
        """"""
        table = "vw_app_instance"
        # if self.instance.is_independent:
        #     table = f"vwt_app_version_{self.instance.alias}"
        return self.get_table(table)

    def get_doc_media(self, recent_only=False, n=50, db="db"):
        """App document refers docucation instances"""
        table = "vw_doc_media"
        if self.instance.is_independent:
            table = f"vwt_doc_media_{self.instance.alias}"
        params = {}
        if recent_only:
            params = {f"TOP {n}"}
        return self.get_table(table, params, db)

    def get_doc_media_content(self, cfg, db="db"):
        """"""
        table = "vw_doc_media_content"
        if self.instance.is_independent:
            table = f"vwt_doc_media_content_{self.instance.alias}"
        return self.get_table(table, cfg, db)

    # def get_doc_tab(self, params, db="db"):
    #     """"""
    #     table = "vw_doc_tab"
    #     if self.instance is not None:
    #         if self.instance.is_independent:
    #             table = f"vwt_doc_tab_{self.instance.alias}"
    #     df = self.get_table(table, params, db)
    #     df = df.sort_values(by=["pid_txt", "position_int"])
    #     return df

    def get_doc_tree_node(self):
        """"""

    def get_doc_user(self):
        """"""

    # def get_links(self, name=None, description=None, type_=None, tag=None, url=None, db="db"):
    #     """"""
    #     table = "vw_link"
    #     if self.instance is not None:
    #         if self.instance.is_independent:
    #             table = f"vwt_link_{self.instance.alias}"
    #     cfg = {}
    #     if name is not None:
    #         if cfg.get("WHERE", None) is None:
    #             cfg["WHERE"] = {}
    #         cfg["WHERE"] = {"EQUAL": {"name_txt": name}}
    #     if description is not None:
    #         if cfg.get("WHERE", None) is None:
    #             cfg["WHERE"] = {}
    #         cfg["WHERE"]["LIKE"] = {"description_ltxt": description}
    #     if type_ is not None:
    #         if cfg.get("WHERE", None) is None:
    #             cfg["WHERE"] = {}
    #         if "EQUAL" not in cfg["WHERE"]:
    #             cfg["WHERE"]["EQUAL"] = {}
    #         cfg["WHERE"]["EQUAL"]["type_txt"] = type_
    #     if tag is not None:
    #         if cfg.get("WHERE", None) is None:
    #             cfg["WHERE"] = {}
    #         if "EQUAL" not in cfg["WHERE"]:
    #             cfg["WHERE"]["EQUAL"] = {}
    #         cfg["WHERE"]["EQUAL"]["tag_txt"] = tag
    #     if url is not None:
    #         if cfg.get("WHERE", None) is None:
    #             cfg["WHERE"] = {}
    #         if "LIKE" not in cfg["WHERE"]:
    #             cfg["WHERE"]["LIKE"] = {}
    #         cfg["WHERE"]["LIKE"]["url_ltxt"] = url
    #     return self.get_table(table, cfg, db)
    # OPTIMIZATION 4: Refactored get_links with DRY principle
    def get_links(self, name=None, description=None, type_=None, tag=None, url=None, db="db"):
        """"""
        table = self._table_resolver.get_table_name("link", self.instance)

        cfg = self._build_filter_config(
            [
                ("EQUAL", "name_txt", name),
                ("LIKE", "description_ltxt", description),
                ("EQUAL", "type_txt", type_),
                ("EQUAL", "tag_txt", tag),
                ("LIKE", "url_ltxt", url),
            ]
        )

        return self.get_table(table, cfg, db)

    # def get_table(self, table, parameters=None, db="db"):
    #     """"""
    #     table_cfg = {"table": [table]}
    #     if parameters is None:
    #         parameters = {}
    #     parameters["get_all_columns"] = True
    #     if db not in self.docs.keys():
    #         return DataFrame()
    #     # parameters["table"] = [table]
    #     rdr = self.docs[db].read(table_cfg, parameters)
    #     return next(rdr).dikt[table]["df"]

    def get_view_border_styles(self, cfg=None, db="db"):
        """"""
        table = "vw_border_styles"
        if self.instance is not None:
            if self.instance.is_independent:
                table = f"vwt_border_styles_{self.instance.alias}"
        return self.get_table(table, cfg, db)

    def get_view_colors(self, cfg, db="db"):
        """"""
        table = "vw_colors"
        if self.instance is not None:
            if self.instance.is_independent:
                table = f"vwt_colors_{self.instance.alias}"
        return self.get_table(table, cfg, db)

    def get_view_maintain_doc_media_content(self, cfg=None, db="db"):
        """"""
        table = "vw_maint_doc_media_content"
        if self.instance is not None:
            if self.instance.is_independent:
                table = f"vwt_maint_doc_media_content_{self.instance.alias}"
        return self.get_table(table, cfg, db)

    def get_view_marked_deleted(self, db="db"):
        """"""
        table = "vw_marked_deleted"
        if self.instance is not None:
            if self.instance.is_independent:
                table = f"vwt_marked_deleted_{self.instance.alias}"
        return self.get_table(table, db=db)

    def get_view_settings(self, cfg, db="db"):
        """"""
        table = "vw_settings"
        if self.instance is not None:
            if self.instance.is_independent:
                table = f"vwt_settings_{self.instance.alias}"
        return self.get_table(table, cfg, db)

    def get_view_settings_interface(self, cfg, db="db"):
        """"""
        table = "vw_settings_interface"
        if self.instance is not None:
            if self.instance.is_independent:
                table = f"vwt_settings_interface_{self.instance.alias}"
        return self.get_table(table, cfg, db)

    def get_view_settings_security(self, cfg, db="db"):
        """"""
        table = "vw_settings_security"
        if self.instance is not None:
            if self.instance.is_independent:
                table = f"vwt_settings_security_{self.instance.alias}"
        return self.get_table(table, cfg, db)

    def get_view_settings_storage(self, cfg, db="db"):
        """"""
        table = "vw_settings_storage"
        if self.instance is not None:
            if self.instance.is_independent:
                table = f"vwt_settings_storage_{self.instance.alias}"
        return self.get_table(table, cfg, db)

    def get_view_supported_os(self, cfg, db="db"):
        """"""
        table = "vw_supported_os"
        if self.instance is not None:
            if self.instance.is_independent:
                table = f"vwt_supported_os_{self.instance.alias}"
        return self.get_table(table, cfg, db)

    def get_view_tab(self, cfg, db="db"):
        """"""
        table = "vw_tab"
        if self.instance is not None:
            if self.instance.is_independent:
                table = f"vwt_tab_{self.instance.alias}"
        df = self.get_table(table, cfg, db)
        df = df.sort_values(by=["pid_txt", "position_int"])
        return df

    def get_view_tree_node(self, cfg, db="db"):
        """"""
        table = "vw_tree_node"
        if self.instance is not None:
            if self.instance.is_independent:
                table = f"vwt_tree_node_{self.instance.alias}"
        return self.get_table(table, cfg, db)

    def init_database_application(self, cfg=None):
        """Initializing the Database for the Nchantd Cloak application sets the
        primary data source for the application to the self.src model class
        attribute.  This source is set to an instance of a SQuiRL class from the SQuiRL module.
        should there be other options for the primary source?
        a cache is initially created to store all interaction data
        permanent storage and packup via a database will also be loaded/created
        """
        self.application_path = self.app.model.application_path
        self.library_path = self.app.model.library_path
        self.instance_path = self.app.model.instance_path
        self.config.override(cfg)
        reset = None
        extension = self.EXTENSION
        if self.config.dikt.get("args", None):
            reset = None if "setup" not in self.config.dikt.get("args", []) else SETUP_RESET_FLAG
        logma.info(f"Reset: {reset}")
        database_file_name = join(self.application_path, f"{self.name}{extension}")
        object_name = "db"
        document_type = "sonql"
        self.initDocument(object_name, document_type, database_file_name, self.config.dikt, reset)
        object_name = "dbc"
        document_type = "conql"
        self.initDocument(object_name, document_type)
        return self

    def init_database_instance(self, instance, attach=True, reset=None):
        """
        Need to add an attach process here to attach the instance database to the application database


        :param file_name:
        :param reset:
        :return:
        """
        logma.info(f"Instance {instance.instance_id}")
        logma.info(f"Instance {instance.instance_path}")
        document_type = "sonql"
        tables = self.config.dikt.get("tables").dikt
        self.initDocument(instance.db_instance_id, document_type, instance.get_file_path(), tables, reset)
        document_type = "conql"
        self.initDocument(instance.dbc_instance_id, document_type)
        if self.app.new_instance:
            self.policy.init_policies()
            self.store_doc_instance(instance.db_instance_id, f"dbi_{instance.db_instance_id}")
        return self

    def initDocument(self, name, doc_type, path=None, objects=None, reset=None):
        """"""
        self.objects = objects
        super().initDocument(name, doc_type, path, objects, reset)
        # self._load_application_configs()  [DONE]
        # self._load_password()
        return self

    def load_instance(self):
        """"""
        instances = self.get_app_instance()
        instances.sort_values(by=["CREON_DTTM"], inplace=True)
        instance = instances.loc[0].to_dict()
        logma.info(f"Wizard: create_instance: {instance}")
        instance = NchantdInstance(self, instance)
        self.app.model.instances = {x["instance_id_txt"]: x for x in instances.to_dict(orient="records")}
        instance.is_install_active = False
        logma.info(f"Install Active: {instance.is_install_active}")
        logma.info(f"Instance Id {instance.instance_id}")
        self.app.model.set_instance_active(instance)
        return self

    # def map_columns(self, map, df):
    #     """"""
    #     for column in map.keys():
    #         if map[column] is None:
    #             del df[column]
    #         else:
    #             df[map[column]] = df[column]
    #             del df[column]
    #     return df

    # def merge_table(self, old_table, new_table, map, filter_=None, db="db"):
    #     """"""
    #     df = self.get_table(old_table, db=db)
    #     if filter_ is not None:
    #         df = filter_.process(df)
    #     df.drop(f"{old_table}_PK", axis=1, inplace=True)
    #     df.drop(f"{new_table}_PK", axis=1, inplace=True)
    #     if map is not None:
    #         df = self.map_columns(map, df)
    #     self.docs[db].writeDF(df, new_table)
    #     return self.docs[db].checkTable(new_table, record_n=df.shape[0])
    #
    # def remove_record(self, table, column, value, db="db"):
    #     """"""
    #     return self
    #
    # def remove_records(self):
    #     """"""

    # def restore_backup(self, db, version="latest"):
    #     """"""
    #     path = self.find_backup(self.parent.model.instance, version)
    #     if exists(path):
    #         # remove live database
    #         fonql.removePath(self.parent.model.instance.get_file_path())
    #         # copy backup to active_instance_path
    #         fonql.fileCopy(path, self.parent.model.instance.get_file_path())
    #     return self
    #
    # def secure_write(self, key, value, db="db", how="INSERT"):
    #     """
    #     Store secure data
    #
    #     :param key:
    #     :param value:
    #     :return:
    #     """
    #     value = self._encrypt(value)
    #     payload = {"table": {"secure_store": {"records": [key, value]}, "columns": ["key", "value"]}}
    #     self.docs["db"].write(payload)
    #     return self
    def store_app_action(self, data, cfg=None, db="db", how="INSERT"):
        """Refactored with centralized validation and payload building"""
        operation = self._validate_operation(how)
        payload_cfg = self._build_store_payload("app_action", data, operation, cfg)
        self._store("app_action", payload_cfg.get("table", {}).get("app_action", {}).get("records", []), cfg)
        return self

    def store_app_document_type(self, data, cfg=None, db="db", how="INSERT"):
        """Refactored with centralized validation and payload building"""
        operation = self._validate_operation(how)
        payload_cfg = self._build_store_payload("app_document_type", data, operation, cfg)
        self._store("app_document_type", payload_cfg.get("table", {}).get("app_document_type", {}).get("records", []))
        return self

    # OPTIMIZATION 7: Batch operation support for memory efficiency
    def store_app_options_batch(self, options, tag=None, db="db"):
        """Store multiple options efficiently in batch"""
        if self.user is None:
            user_FK = DEFAULT_USER_ID
        else:
            user_FK = self.user.FK

        payloads = []
        for option in options:
            if isinstance(option, dict):
                payloads.append(
                    [
                        uuid(),
                        option.get("key"),
                        option.get("label"),
                        option.get("value"),
                        option.get("table"),
                        tag or option.get("tag"),
                        option.get("parent_id", 0),
                        user_FK,
                    ]
                )

        self._store("app_option", payloads)
        return self

    def store_links_batch(self, links, db="db"):
        """Store multiple links efficiently in batch"""
        payloads = []
        for link in links:
            payloads.append(
                [
                    uuid(),
                    link.get("name", ""),
                    link.get("type", ""),
                    link.get("description", ""),
                    link.get("url"),
                    link.get("tag", ""),
                ]
            )

        self._store("link", payloads)
        return self

    # def store_app_action(self, data, cfg=None, db="db", how="INSERT"):
    #     """
    #             columns: ['code_group_txt', 'lookup_code_txt', 'name_txt', 'description_ltxt', 'UUID', 'icon_txt',
    #               'short_cut_txt', 'tip_txt', 'advanced_tip_txt', 'widget_txt', 'parameters_dict']
    #     :return:
    #     """
    #     table = "app_action"
    #     if how == "INSERT":
    #         payload = []
    #     elif how == "UPDATE":
    #         payload = [{}]
    #     elif how == "DEACTIVATE":
    #         payload = []
    #     elif how == "DELETE":
    #         payload = []
    #     elif how == "ARCHIVE":
    #         payload = []
    #     else:
    #         raise Exception(f"{how} is not supported.")
    #     self._store(table, payload, cfg)
    #     return self
    #
    # def store_app_document_type(self, data, cfg=None, db="db", how="INSERT"):
    #     """
    #                 columns: ['UUID', 'file_type_txt', 'document_txt', 'name_txt', 'description_ltxt', 'widget_txt',
    #                   'parameters_dict', "sequence_int", "document_types", 'local_available_bit', 'feature_plan_int',
    #                   'google_available_bit', 'registered_bit']
    #     :return:
    #     """
    #     table = "app_document_type"
    #     if how == "INSERT":
    #         payload = []
    #     elif how == "UPDATE":
    #         payload = [{}]
    #     elif how == "DEACTIVATE":
    #         payload = []
    #     elif how == "DELETE":
    #         payload = []
    #     elif how == "ARCHIVE":
    #         payload = []
    #     else:
    #         raise Exception(f"{how} is not supported.")
    #     self._store(table, data)
    #     return self

    def store_app_event(self, state, eventtype, g_command="", db="db", how="INSERT"):
        """

        'UUID', 'state_txt', 'user_nm_txt', 'MAC', 'events_dttm', 'application_new_bit', 'instance_new_bit',
        'eventtype_txt', 'command_txt', 'instance_FK', 'application_NCD', 'device_dict'

        :param state:
        :param eventtype:
        :param g_command:
        :return:
        """
        table = "app_event"
        if how == "INSERT":
            payload = []
        elif how == "UPDATE":
            payload = [{}]
        elif how == "DEACTIVATE":
            payload = []
        elif how == "DELETE":
            payload = []
        elif how == "ARCHIVE":
            payload = []
        else:
            raise Exception(f"{how} is not supported.")
        return self
        # command = inspect.currentframe().f_back.f_back.f_code.co_name
        # command += f" - {inspect.currentframe().f_back.f_back.f_lineno}"
        # command += f" - {g_command}" if g_command != "" else ""
        # instance = self.instance
        # if instance is None:
        #     iid = self.app.application_NCD
        # else:
        #     iid = instance.instance_id
        #
        # data = [
        #     [
        #         uuid(),
        #         state,
        #         self.app.model.device.user,
        #         self.app.model.device.mac,
        #         self.time.store_now(),
        #         eventtype,
        #         command,
        #         iid,
        #         self.app.application_NCD,
        #         self.app.model.device.toStr(),
        #         "context",
        #     ]
        # ]
        # #        logma.info(f"Data {data}")
        # self._store(table, data, db)
        # if state in ("crashed", ""):  [DONE]
        #     self.app.model.send_notification()
        # return self

    def store_app_instance(self, instance, db="db", how="INSERT"):
        """
                    'columns': ['instance_id', 'name', 'is_new', 'application_NCD',
                        'application_path', 'instance_path']
        :return:
        """
        table = "app_instance"
        if how == "INSERT":
            payload = []
        elif how == "UPDATE":
            payload = [{}]
        elif how == "DEACTIVATE":
            payload = []
        elif how == "DELETE":
            payload = []
        elif how == "ARCHIVE":
            payload = []
        else:
            raise Exception(f"{how} is not supported.")
        if how == "INSERT":
            payload = [
                [
                    instance.instance_id,  # instance_id
                    instance.name,  # name
                    instance.description,
                    instance.is_primary,
                    instance.application_NCD,  # application_NCD
                    instance.application_path,  # application_path
                    instance.instance_path,  # instance_path
                    instance.version,
                    encode64(
                        j.dumps(instance.meta_data),
                    ),
                ]
            ]
            self._store(table, payload)
        elif how == "UPDATE":
            payload = [
                {
                    "name": instance.name,
                    "application_path": instance.application_path,
                    "instance_path": instance.instance_path,
                }
            ]
            column = "instance_id"
            values = [instance.instance_id]
            cfg = {"WHERE": {"IN": {column: values}}}
            self._store(table, payload, cfg)
        return self

    def store_app_media(self, document, db="db", how="INSERT"):
        """"""
        table = "app_media"
        if how == "INSERT":
            payload = []
        elif how == "UPDATE":
            payload = [{}]
        elif how == "DEACTIVATE":
            payload = []
        elif how == "DELETE":
            payload = []
        elif how == "ARCHIVE":
            payload = []
        else:
            raise Exception(f"{how} is not supported.")
        payload = [
            [
                document["did"],
                document.get("compatibility", "pyffice"),
                document["document_type"],
                document["syntax"],
                document["name"],
                document["file_name"],
                document["description"],
                document["path"],
                document["location"],
                document["encoding"],
                "|".join(document["tags"]),
                document["version"],
                # document.get("pyffice_version", "0.0.1.0.1.0"),#TODO not valid for nchantrs but still haven't seperated the underlying table config files
                document["hash"],
                document["policy"],
                encode64(j.dumps(document.get("metadata", {}))),
            ]
        ]
        self._store(table, payload, db)
        # self._archive_versions(table, document["did"], "did", "did", 3)
        return document["did"]

    def store_app_media_content(self, content, db="db", how="INSERT"):
        """"""
        table = "app_media_content"
        if how == "INSERT":
            payload = []
        elif how == "UPDATE":
            payload = [{}]
        elif how == "DEACTIVATE":
            payload = []
        elif how == "DELETE":
            payload = []
        elif how == "ARCHIVE":
            payload = []
        else:
            raise Exception(f"{how} is not supported.")
        payload = [
            [
                content["uuid"],
                content["pUUID"],
                content["page"],
                content["entry"],
                content["version"],
                content["hash"],
                content["content"],
                content["context"],
            ]
        ]
        # set delete for all but the largest 3 versions
        self._store(table, payload, db)
        # self._archive_versions(table, content["pUUID"], "pUUID", "UUID", 3)
        return content["uuid"]

    def store_app_menu(self, db="db", how="INSERT"):
        """
            columns: ['UUID', 'pid_txt', 'name_txt', 'tag_txt', 'is_action_bit', 'application_ncd']
        :return:
        """
        return self

    def store_app_option(self, option, key=None, vtable=None, tag=None, option_FK = DEFAULT_USER_ID, db="db", how="INSERT"):
        """
                    'columns': [ 'UUID', 'key_txt', 'label_txt', 'value_txt', 'table_txt', 'tag_ltxt',
                         'parameters_ltxt', 'description_ltxt', 'parent_UUID', 'table_FK', 'instance_FK',
                         'user_FK' ]
        :param option:
        :param key:
        :param vtable:
        :param tag:
        :param option_FK:
        :return:
        """
        table = "app_option"
        if how == "INSERT":
            payload = []
        elif how == "UPDATE":
            payload = [{}]
        elif how == "DEACTIVATE":
            payload = []
        elif how == "DELETE":
            payload = []
        elif how == "ARCHIVE":
            payload = []
        else:
            raise Exception(f"{how} is not supported.")
        if self.user is None:
            user_FK = DEFAULT_USER_ID
        else:
            user_FK = self.user.FK
        payload = []
        if isinstance(option, list):
            for op in option:
                if isinstance(op, list):
                    if len(op) == 5:
                        option_FK = op[4]
                    payload.append([uuid(), op[0], op[1], op[2], op[3], option_FK, self.instance_FK, user_FK])
                elif isinstance(op, dict):
                    payload.append([uuid(), op["key"], op["label"], op["option"], op["table"], tag, option_FK, user_FK])
        else:
            payload = [[uuid(), key, option, vtable, tag, option_FK, self.instance_FK, user_FK]]
        self._store(table, payload)
        return self

    def store_app_option_key(self, db="db", how="INSERT"):
        """
                    'columns': ['UUID', 'app_option_FK_0', 'virtual_table_txt', 'table_txt', 'app_option_FK_1', 'instance_FK', 'user_FK']
        :return:
        """
        if how == "INSERT":
            payload = []
        elif how == "UPDATE":
            payload = [{}]
        elif how == "DEACTIVATE":
            payload = []
        elif how == "DELETE":
            payload = []
        elif how == "ARCHIVE":
            payload = []
        else:
            raise Exception(f"{how} is not supported.")
        return self

    def store_app_policy(self, record, db="db", how="INSERT"):
        """
                    columns: ["UUID", "type", "target", "policy"]
        :param record:
        :return:
        """
        table = "app_policy"
        if how == "INSERT":
            payload = []
        elif how == "UPDATE":
            payload = [{}]
        elif how == "DEACTIVATE":
            payload = []
        elif how == "DELETE":
            payload = []
        elif how == "ARCHIVE":
            payload = []
        else:
            raise Exception(f"{how} is not supported.")
        self._store("app_policy", [record])
        return self

    def store_app_profile(self, record, db="db", how="INSERT"):
        """"""
        return self

    def store_app_secure_store(self, db="db", how="INSERT"):
        """
                    columns: ['UUID', 'userUUID', 'key', 'value']
        :return:
        """
        table = "app_secure_store"
        if how == "INSERT":
            payload = []
        elif how == "UPDATE":
            payload = [{}]
        elif how == "DEACTIVATE":
            payload = []
        elif how == "DELETE":
            payload = []
        elif how == "ARCHIVE":
            payload = []
        else:
            raise Exception(f"{how} is not supported.")
        cfg = {"table": table}
        reader = self.docs["db"].read(cfg)
        df = next(reader).dikt[table]["df"]
        return self

    def store_app_tab(self, row, instance=None, db="db", how="INSERT"):
        """
                    'columns': ['name_txt', 'widget_txt', 'widgdata_dict', 'pid_txt', 'did_txt', 'position_int',
                                'document_type_txt', 'tabset_type_txt', 'readonly_bit', 'editable_bit', 'visible_bit',
                                'moveable_bit', 'UUID']
        :param row:
        :param instance:
        :return:
        """
        table = "app_tab"
        if how == "INSERT":
            payload = []
        elif how == "UPDATE":
            payload = [{}]
        elif how == "DEACTIVATE":
            payload = []
        elif how == "DELETE":
            payload = []
        elif how == "ARCHIVE":
            payload = []
        else:
            raise Exception(f"{how} is not supported.")
        payload = [row]
        self._store(table, payload)
        # self.store_app_event("system_interaction", "store_app_tab", "".join(str(x) for x in row))
        return self

    # TODO edit name
    def store_app_tree_nodes(self, data, db="db", how="INSERT"):
        """
                    columns: ['nid', 'icon', 'name', 'ntype', 'parentid', 'position', 'parameters', 'source',
                      'treeid', 'readonly', 'editable', 'visible', 'moveable',
                      'pregnable', 'isparent', 'expanded', 'tabfocus']
        :param data:
        :return:
        """
        if how == "INSERT":
            payload = []
        elif how == "UPDATE":
            payload = [{}]
        elif how == "DEACTIVATE":
            payload = []
        elif how == "DELETE":
            payload = []
        elif how == "ARCHIVE":
            payload = []
        else:
            raise Exception(f"{how} is not supported.")
        if isinstance(data, DataFrame):
            self._store_df(self.nodetable, data, {"how": "IF NOT EXISTS", self.nodetable: "nid"})
        elif isinstance(data, list):
            self._store(self.nodetable, data, {"how": "IF NOT EXISTS", self.nodetable: "nid"})
        return self

    def store_app_tree_node(self, name, ntype, pid, pos, parameters=None, tree="left", db="db", how="INSERT"):
        """"""
        if how == "INSERT":
            payload = []
        elif how == "UPDATE":
            payload = [{}]
        elif how == "DEACTIVATE":
            payload = []
        elif how == "DELETE":
            payload = []
        elif how == "ARCHIVE":
            payload = []
        else:
            raise Exception(f"{how} is not supported.")
        icon = ""
        nid = self.gen_NID()
        if parameters is None:
            parameters = {"focus": "office"}
        if isinstance(parameters, dict):
            parameters = j.dumps(parameters)
        row = [nid, icon, name, ntype, pid, str(pos), parameters] + self.app.view.panes[tree].tree.model.nodebase
        data = {
            "app_tree_node": {
                "records": [row],
                "columns": self.app.view.panes[tree].tree.model.nodecolumns,
            }
        }
        self.docs["db"].write(data)
        return nid, row

    def store_app_user(self, user, db="db", how="INSERT"):
        """
                    'columns': ['UUID', 'mac_hash', 'user_nm_txt', 'password_txt', 'saltUUID', 'iterations_txt', 'address_txt',
                        'public_key_txt', 'is_private_bit', 'is_secure_bit', 'instance_FK', 'application_new_bit',
                        'instance_new_bit']
        :param user:
        :param db:
        :return:
        """
        table = "app_user"
        if how == "INSERT":
            payload = []
        elif how == "UPDATE":
            payload = [{}]
        elif how == "DEACTIVATE":
            payload = []
        elif how == "DELETE":
            payload = []
        elif how == "ARCHIVE":
            payload = []
        else:
            raise Exception(f"{how} is not supported.")
        payload = [
            [
                user.uuid,  # UUID
                text_hashing_function(user.parent.device.mac),  # MAC Hash
                user.parent.device.user,  # user_nm_txt
                encode64(user.hash),  # password_txt
                encode64(user.salt),  # saltUUID
                encode64(str(user.iters)),  # iterations_txt
                encode64(user.address),  # address_txt
                encode64(user.rsa_key),  # public_key_txt
                self.app.model.is_private,  # is_private_bit
                self.app.model.is_secure,  # is_secure_bit
                self.app.model.instance.instance_id,  # instanceFK
                # self.app.new_application,  # application_new_bit
                # self.app.new_instance,  # instance_new_bit
            ]
        ]
        FK = self._store(table, payload, db)
        return FK, payload[0]

    def store_doc_media(self, db="db", how="INSERT"):
        """"""
        if how == "INSERT":
            payload = []
        elif how == "UPDATE":
            payload = [{}]
        elif how == "DEACTIVATE":
            payload = []
        elif how == "DELETE":
            payload = []
        elif how == "ARCHIVE":
            payload = []
        else:
            raise Exception(f"{how} is not supported.")

    def store_doc_media_content(self, db="db", how="INSERT"):
        """"""
        if how == "INSERT":
            payload = []
        elif how == "UPDATE":
            payload = [{}]
        elif how == "DEACTIVATE":
            payload = []
        elif how == "DELETE":
            payload = []
        elif how == "ARCHIVE":
            payload = []
        else:
            raise Exception(f"{how} is not supported.")

    def store_doc_tab(self, row, instance, db="db", how="INSERT"):
        """
            'columns': ['name_txt', 'widget_txt', 'widgdata_dict', 'pid_txt', 'did_txt', 'position_int', 'document_type_txt',
                        'tabset_type_txt', 'readonly_bit', 'editable_bit', 'visible_bit', 'moveable_bit', 'UUID']
        :param row:
        :param instance:
        :return:
        """
        table = "doc_tab"
        if how == "INSERT":
            payload = []
        elif how == "UPDATE":
            payload = [{}]
        elif how == "DEACTIVATE":
            payload = []
        elif how == "DELETE":
            payload = []
        elif how == "ARCHIVE":
            payload = []
        else:
            raise Exception(f"{how} is not supported.")
        payload = [row]
        logma.info(f"Table {table} {payload} {db}")
        self._store(table, payload, db)
        # self.store_app_event("user_interaction", "store_doc_tab", "".join(str(x) for x in row))
        return self

    def store_doc_tree_node(self, name, ntype, pid, pos, parameters=None, tree="left", db="db", how="INSERT"):
        """"""
        if how == "INSERT":
            payload = []
        elif how == "UPDATE":
            payload = [{}]
        elif how == "DEACTIVATE":
            payload = []
        elif how == "DELETE":
            payload = []
        elif how == "ARCHIVE":
            payload = []
        else:
            raise Exception(f"{how} is not supported.")
        icon = ""
        nid = self.gen_NID()
        if parameters is None:
            parameters = {"focus": "office"}
        if "recent_tab" not in parameters.keys():
            parameters["recent_tab"] = {"center": 0, "right": 0}
        if isinstance(parameters, dict):
            parameters = j.dumps(parameters)
        row = [nid, icon, name, ntype, pid, str(pos), parameters] + self.app.view.panes[tree].tree.model.nodebase
        data = {
            "doc_tree_node": {
                "records": [row],
                "columns": self.app.view.panes[tree].tree.model.nodecolumns,
            }
        }
        self.docs["db"].write(data)
        return nid, row

    def store_doc_user(self, db="db", how="INSERT"):
        """
                    'columns': ['UUID', 'MAC', 'user_nm_txt', 'password_txt', 'saltUUID', 'iterations_txt', 'address_txt',
                        'public_key_txt', 'is_private_bit', 'is_secure_bit', 'instance_FK', 'application_new_bit',
                        'instance_new_bit']
        :return:
        """
        if how == "INSERT":
            payload = []
        elif how == "UPDATE":
            payload = [{}]
        elif how == "DEACTIVATE":
            payload = []
        elif how == "DELETE":
            payload = []
        elif how == "ARCHIVE":
            payload = []
        else:
            raise Exception(f"{how} is not supported.")
        return self

    def store_link(self, url, name="", type_="", description="", tag="", db="db", how="INSERT"):
        """
                    columns: ["UUID", "name", "type", "description", 'url_ltxt', "tag_txt"]
        :return:
        """
        if how == "INSERT":
            payload = []
        elif how == "UPDATE":
            payload = [{}]
        elif how == "DEACTIVATE":
            payload = []
        elif how == "DELETE":
            payload = []
        elif how == "ARCHIVE":
            payload = []
        else:
            raise Exception(f"{how} is not supported.")
        table = "link"
        if not isinstance(url, list):
            url = [url]
        for url_ in url:
            payload = [[uuid(), name, type_, description, url_, tag]]
            self._store(table, payload)
        return self

    def _build_filter_config(self, filters):
        """Build WHERE clause from filter list - eliminates repetitive if statements"""
        cfg = {}
        where = {}

        for op_type, field, value in filters:
            if value is None:
                continue

            if op_type not in where:
                where[op_type] = {}
            where[op_type][field] = value

        if where:
            cfg["WHERE"] = where

        return cfg

    def _build_store_payload(self, table, data, operation, cfg=None):
        """Standardized payload building for store operations"""
        self._validate_operation(operation)

        if operation == "INSERT":
            if isinstance(data, list):
                payload = data if data else []
            else:
                payload = [data]
        elif operation == "UPDATE":
            payload = [data] if isinstance(data, dict) else data
        else:  # DEACTIVATE, DELETE, ARCHIVE
            payload = []

        return {"table": {table: {"records": payload}}}

    def _build_tag_hierarchy(self, tag: str) -> list:
        """Build tag hierarchy efficiently - O(n) instead of O(n²)"""
        if "." not in tag:
            return [tag]

        tags = []
        parts = tag.split(".")
        for i in range(len(parts)):
            tags.append(".".join(parts[: i + 1]))
        return tags

    # OPTIMIZATION 8: Lazy loading for heavy operations
    @property
    def _db_objects(self):
        """Lazy-load db objects configuration once"""
        if not hasattr(self, "_db_objects_cache"):
            self._db_objects_cache = self.config.dikt.get("dstruct", {}).get("database", {}).get("objects", {})
        return self._db_objects_cache

    def _get_table_columns(self, table):
        """Get table columns from config with lazy loading"""
        tables = self._db_objects.get("table", {})
        return tables.get(table, {}).get("columns", [])

    # OPTIMIZATION 5: Generic getter methods to replace 20+ similar methods
    def _get_app_view_table(self, view_name, cfg=None, db="db"):
        """Generic method to eliminate repetitive get_app_* methods"""
        table = self._table_resolver.get_table_name(view_name, self.instance)
        return self.get_table(table, cfg, db)

    def _get_sorted_app_view_table(self, view_name, cfg=None, sort_by=None, db="db"):
        """Get and sort app view table"""
        df = self._get_app_view_table(view_name, cfg, db)
        if sort_by and not df.empty:
            df = df.sort_values(by=sort_by)
        return df

    # OPTIMIZATION 6: Refactored store methods with DRY principle
    def _validate_operation(self, operation):
        """Centralized operation validation"""
        return PayloadBuilder.validate_and_get_operation(operation)

    # def store_records(self, table, records, db="db"):
    #     """"""
    #     self._store(table, records, db)
    #     return self
    #
    # def update_record(self, data, column, value, db):
    #     """"""
    #     # logma.inspect_caller()
    #     if not isinstance(value, list):
    #         value = [value]
    #     logma.info(f"Update Record {data} {column} {value} {db}")
    #     cfg = {"WHERE": {"IN": {column: value}}}
    #     self._write(data, cfg, "UPDATE", db)
    #     return self
    #
    # def write_secure(self, user, key, value=None):
    #     """"""
    #     if not user.is_verified and (self.parent.is_private or self.parent.is_secure):
    #         return False
    #     db_objects = self.config.dikt["dstruct"]["database"]["objects"]
    #     logma.info(f"Write Secure {db_objects["table"].keys()}")
    #     if db_objects is None:
    #         return
    #     if isinstance(key, list):
    #         payload = []
    #         for item in key:
    #             [k], [v] = item.keys(), item.values()
    #             payload.append([str(uuid7()), user.uuid, k, base64.b64encode(v).decode()])
    #     else:
    #         payload = [[str(uuid7()), user.uuid, key, base64.b64encode(value)]]
    #     cfg = {
    #         "app_secure_store": {
    #             "records": payload,
    #             "columns": db_objects["table"]["app_secure_store"]["columns"],
    #         }
    #     }
    #     self.app.model.store.docs["db"].write(cfg)
    #
    # def _activate(self, table, primary_keys, db="db", flip=False):
    #     """"""
    #     if not isinstance(primary_keys, list):
    #         primary_keys = [primary_keys]
    #     bit = 1
    #     if flip is True:
    #         bit = 0
    #     cfg = {"WHERE": {"IN": {f"{table}_PK": primary_keys}}}
    #     data = {"table": {table: {"ACTIVE_BIT": bit, "MODON_DTTM": self.time.store_now(), "MODBY_FK": self.user_FK}}}
    #     self._write(data, cfg, db)
    #     return self
    #
    # def _archive(self, table, primary_keys=None, db="db", flip=False):
    #     """"""
    #     cfg = {}
    #     if primary_keys is None:
    #         if not isinstance(primary_keys, list):
    #             primary_keys = [primary_keys]
    #         cfg = {"WHERE": {"IN": {f"{table}_PK": primary_keys}}}
    #     bit = 1
    #     if flip is True:
    #         bit = 0
    #     data = {"table": {table: {"ARCHIVE_BIT": bit, "MODON_DTTM": self.time.store_now(), "MODBY_FK": self.user_FK}}}
    #     self._write(data, cfg, db)
    #     return self
    #
    # def _decrypt(self, key, db="db"):
    #     """"""
    #     data = next(self.docs[db].read({"table": {"secure_store"}}))
    #     return self
    #
    # def _delete_by_primary_key(self, table, primary_keys, db="db", flip=False):
    #     """"""
    #     if not isinstance(primary_keys, list):
    #         primary_keys = [primary_keys]
    #     bit = 1
    #     if flip is True:
    #         bit = 0
    #     cfg = {"WHERE": {"IN": {f"{table}_PK": primary_keys}}}
    #     data = {
    #         "table": {
    #             table: {
    #                 "DELETE_BIT": bit,
    #                 "ACTIVE_BIT": bit,
    #                 "MODON_DTTM": self.time.store_now(),
    #                 "MODBY_FK": self.user_FK,
    #             }
    #         }
    #     }
    #     self._write(data, cfg, db)
    #     return self
    #
    # def _delete_table(self, table, db="db"):
    #     """This could be needed for upgrades but not sure it should be here in the standard store object"""
    #     return self
    #
    # def _delete_by_uuid(self, table, uuid, column="UUID", db="db", flip=False):
    #     """"""
    #     if not isinstance(uuid, list):
    #         uuid = [uuid]
    #     dbit = 1
    #     abit = 0
    #     if flip is True:
    #         dbit = 0
    #         abit = 1
    #     cfg = {"WHERE": {"IN": {column: uuid}}}
    #     data = {
    #         "table": {
    #             table: {
    #                 "data": {
    #                     "DELETE_BIT": dbit,
    #                     "ACTIVE_BIT": abit,
    #                     "MODON_DTTM": self.time.store_now(),
    #                     "MODBY_FK": self.user_FK,
    #                 }
    #             }
    #         }
    #     }
    #     logma.info(f"Delete {column} = {uuid} from {table} in {db}")
    #     logma.info(f"Data: {data}")
    #     self._write(data, cfg, "UPDATE", db)
    #     return self
    #
    # def _encrypt(self, val):
    #     """"""
    #     return val
    #
    # def _remove_table(self, table, db="db"):
    #     """"""
    #
    # def _remove_by_uuid(self, table, uuid, column="UUID", db="db", flip=False):
    #     """"""
    #
    # def _store(self, table, payload, db="db"):
    #     """"""
    #     db_objects = self.config.dikt["dstruct"]["database"]["objects"]
    #     if db_objects is None:
    #         logma.warning("Objects is None")
    #         return
    #     # logma.info(f"Objects {db_objects.keys()}")
    #     if db_objects.get("table", None):
    #         if table in db_objects.get("table", []):
    #             # logma.info(f"Table {table} {payload}")
    #             cfg = {"table": {table: {"records": payload, "columns": db_objects["table"][table]["columns"]}}}
    #             return self.docs[db].write(cfg)
    #         else:
    #             cfg = {"table": {table: {"records": payload}}}
    #             # logma.warning(f"No table named {table} Objects Config")
    #             return self.docs[db].write(cfg)
    #     else:
    #         logma.warning("No Table Objects")
    #     return self
    #
    # def _store_cache(self, key, payload, cache="dbc"):
    #     """"""
    #     self.docs[cache].write({key: payload})
    #     return self
    #
    # def _store_df(self, table, df, params=None, db="db"):
    #     """"""
    #     if params is None:
    #         params = {}
    #     self.docs[db].write({table: df}, params)
    #     return self
    #
    # def _update(self, table, payload, cfg):
    #     """"""
    #     self.docs["db"].update(table, payload, cfg)
    #     return self
    #
    # def _write(self, data, cfg, func="INSERT", db="db"):
    #     """"""
    #     return self.docs[db].write(data, cfg, func)


def get_node_base(nodetype, treeid=0, tabfocus=0):
    """"""
    if nodetype == "appnode":
        base = [1, 0, 1, 0, 1, 1, 1]
    elif nodetype == "datanode":
        base = [1, 0, 1, 0, 1, 1, 0]
    elif nodetype == "usernode":
        base = [1, 0, 1, 0, 1, 1, 0]
    return treeid + base + tabfocus


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
