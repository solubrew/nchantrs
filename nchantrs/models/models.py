"""
---
<(META)>:
    docid:
    name:
    description: >
        Integration module for embedding Glain tables inside NchantdStore database
    version: 0.0.0.0.0.0
    authority: filesystem
    security: seclvl2
    <(WT)>: -32
"""
from os.path import abspath, dirname, join, exists, getmtime, expanduser
from os import listdir
import inspect
import json
import base64
from typing import Any, Optional
from typing import Any, Dict, List, Optional
from pandas import DataFrame
import re
import datetime as dt
import sqlite3
from kahndor import kahndor
from kahndor.logma import Logma
from squirl.orgnql import fonql
from subtrix.utilities import uuid
from pycurity.pytime import PyTime
from pycurity.pyhash import encode64, text_hashing_function
from micromole.storage import MicroStash
here = join(dirname(__file__), '')
log = True
debug = True
logma = Logma(__name__)
if not log:
    logma.off()
DEFAULT_USER_ID: str = 'default_user'
MAX_BACKUP_COUNT: int = 5
MAX_ARCHIVE_VERSIONS: int = 3
VALID_OPERATIONS: list = ['INSERT', 'UPDATE', 'DEACTIVATE', 'DELETE', 'ARCHIVE']
WINDOW_PATTERN_STR: str = '(\\d+)(DAYS|WEEKS|MONTHS|YEARS)'
WINDOW_UNITS: dict = {'DAYS': 'days', 'WEEKS': 'weeks', 'MONTHS': 'months', 'YEARS': 'years'}
pxcfg = join(here, '_data_', 'models.yaml')

class TableNameResolver:
    """Resolves table names with instance-aware naming - improves maintainability"""

    def __init__(self) -> None:
        self._cache: dict = {}

    def get_table_name(self, base_name: str, instance: Optional['NchantdInstance']=None) -> str:
        """Get instance-aware table name with caching"""
        cache_key = (base_name, getattr(instance, 'alias', None) if instance else None)
        if cache_key in self._cache:
            return self._cache[cache_key]
        if instance is not None and instance.is_independent:
            table_name = f'vwt_{base_name}_{instance.alias}'
        else:
            table_name = f'vw_{base_name}'
        self._cache[cache_key] = table_name
        return table_name

    def clear_cache(self) -> None:
        """Clear cache when instance changes"""
        self._cache.clear()

class PayloadBuilder:
    """Factory for building payloads - eliminates repetitive validation"""
    VALID_OPERATIONS: dict = {'INSERT': list, 'UPDATE': list, 'DEACTIVATE': list, 'DELETE': list, 'ARCHIVE': list}

    @staticmethod
    def validate_and_get_operation(operation: str) -> str:
        """Validate operation and return operation type"""
        if operation not in PayloadBuilder.VALID_OPERATIONS:
            raise ValueError(f"{operation} is not supported. Use: {', '.join(PayloadBuilder.VALID_OPERATIONS.keys())}")
        return operation

    @staticmethod
    def build_cfg_payload(table: str, records: list, columns: Optional[list]=None) -> dict:
        """Build standardized payload config"""
        cfg = {'table': {table: {'records': records}}}
        if columns:
            cfg['table'][table]['columns'] = columns
        return cfg

class WindowPolicyParser:
    """Optimized window policy parser with compiled regex and cached results"""
    WINDOW_PATTERN = re.compile('(\\d+)(DAYS|WEEKS|MONTHS|YEARS)')
    UNIT_MAP = {'DAYS': 'days', 'WEEKS': 'weeks', 'MONTHS': 'months', 'YEARS': 'years'}

    def __init__(self, time_util: Any) -> None:
        self.time = time_util
        self._cache: dict = {}

    def parse(self, window: str) -> tuple:
        """Parse window string once and cache result"""
        if window in self._cache:
            return self._cache[window]
        match = self.WINDOW_PATTERN.match(window)
        if not match:
            raise ValueError(f'Window {window} is not valid. Expected format: 30DAYS, 2WEEKS, etc.')
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

    def __init__(self, parent: Optional[Any]=None, cfg: Optional[dict]=None) -> None:
        """"""
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdInstance').override(cfg)
        self.alias: Optional[str] = None
        self.application_NCD = parent.app.application_NCD
        self.application_path = parent.app.model.application_path
        self.db_instance_id: Optional[str] = None
        self.dbc_instance_id: Optional[str] = None
        self.description: Optional[str] = None
        self.name = self.config.dikt.get('name_txt', 'db')
        self.is_independent: bool = False
        self.instance_id: Optional[str] = None
        self.instance_path: Optional[str] = None
        self.is_new: bool = False
        self.is_primary: bool = False
        self.internal: bool = True
        self.set_instance_id(self.config.dikt.get('instance_id_txt', None))
        self.set_instance_path(self.config.dikt.get('instance_path_txt', None))
        self.meta_data: dict = {}
        self.version = self.parent.app.model.get_current_version()

    def get_file_path(self, db: str='db') -> str:
        """"""
        if db == 'db':
            return join(self.instance_path, f'{self.parent.app.model.slug}{self.parent.app.model.store.EXTENSION}')
        return join(self.instance_path, f'{self.instance_id}{self.parent.app.model.store.EXTENSION}')

    def set_name(self, name: Optional[str]=None) -> 'NchantdInstance':
        """"""
        self.name = name
        return self

    def set_instance_id(self, instance_id: Optional[str]=None) -> 'NchantdInstance':
        """"""
        if instance_id is None:
            instance_id = uuid()
            self.is_new = True
        self.instance_id = instance_id
        self.db_instance_id = f'dbi_{instance_id}'
        self.dbc_instance_id = f'dbci_{instance_id}'
        self.alias = f"db{instance_id[-len(instance_id) + 10:].replace('-', '')}"
        return self

    def set_independent(self, state: bool=True) -> 'NchantdInstance':
        """"""
        self.is_independent = state
        return self

    def set_instance_path(self, path: Optional[str]=None) -> 'NchantdInstance':
        """"""
        if path is None:
            path = join(expanduser('~'), '.local', 'share', self.parent.app.model.slug)
        self.instance_path = path
        return self

    def set_meta_data(self, meta_data: Optional[dict]=None) -> None:
        """"""
        self.meta_data = {}

    def set_type_external(self) -> 'NchantdInstance':
        """"""
        self.internal = False
        return self

    def set_type_internal(self) -> 'NchantdInstance':
        """"""
        self.internal = True
        return self

    def to_dict(self):
        """"""
        return {'instance_id_txt': self.instance_id, 'name_txt': self.name, 'description_ltxt': self.description, 'is_primary_bit': self.is_primary, 'application_NCD_txt': self.application_NCD, 'application_path_txt': self.application_path, 'instance_path_txt': self.instance_path, 'version_txt': self.version, 'meta_data_dict': json.dumps(self.meta_data)}

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
    EXTENSION = '.nchnt'

    def __init__(self, name, parent, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).select('NchantdStore')
        if parent is not None:
            self.config.override(parent.config)
        super().__init__(name, self.config)
        self.config.override(cfg)
        self.parent = parent
        #TODO integrate instance settings storage here
        self.app = self.parent.app
        self._window_parser = WindowPolicyParser(PyTime())
        self._table_resolver = TableNameResolver()

    def add_uuid(self, table, control_column, data_column, db='db'):
        """"""
        data = self.get_table(table, None, db, None)
        data[control_column].apply(lambda x: self.update_records({'table': {table: {data_column: str(uuid())}}}, {'WHERE': {control_column: x}}, db))
        return self

    def backup_database(self, instance, db='db'):
        """"""
        app_name = self.app.application_name.lower()
        if instance is None:
            instance = self.app.model.instance
        if instance is None:
            raise Exception('No Instance')
        in_name = instance.name
        if in_name is None:
            in_name = 'db'
        extension = self.EXTENSION
        input_path = join(instance.instance_path, f'{app_name}{extension}')
        name = f".{app_name}_{in_name}_backup_{self.app.model.store.time.store_now().replace(' ', '')}{extension}"
        output_path = instance.instance_path
        super().backup_database(input_path, output_path, name)
        return name

    def cache_app_install(self, key, payload):
        """"""
        self.cache.write({key: payload})
        return self

    def cache_tabs(self, nid, tabn, tabW, dbc='dbc'):
        """"""
        self.docs[dbc].write({nid: {tabn: tabW}})
        return self

    def check_cache(self, table, filter=None):
        """"""
        df = next(self.cache.read(table))
        return df

    def check_window_policy(self, row, window, db):
        """Optimized window policy check (FIX #2: String splitting)"""
        return self._window_parser.check_window_policy(row['MODON_DTTM'], window)

    def cleanup_application_database(self, clear_instances=True, db='db', dbc='dbc'):
        """"""
        self.docs[db].delete_marked()
        self.docs[dbc].clear_cache()
        if clear_instances:
            for db_instance_id in self.docs.keys():
                self.cleanup_instance_database(db_instance_id)
        return self

    def cleanup_instance_database(self, db_instance_id):
        """"""
        self.docs[db_instance_id].delete_marked()
        self.docs[db_instance_id].clear_cache()
        return self

    def clear_old_backups(self, instance, keep_n=5):
        """"""
        backups = self.find_backup(instance, 'all')
        delete = backups[keep_n:]
        for backup in delete:
            path = join(instance.instance_path, backup)
            if exists(path):
                fonql.removePath(path, 3213)
        return self

    def compact_instances(self):
        logma.info(f'compact_instances called')
        return self

    def create_directories(self, path):
        """"""
        fonql.touch(f'{path}/')
        if exists(path):
            self.app.model.store.cache_app_install('install', ['create_directory', {'path': path}])
            return True
        return False

    def create_index(self, index, db='db'):
        """"""
        objects = self.parent.config.dikt['dstruct']['database']['objects']['index']
        return super().create_index(index, objects[index]['cmd'], db)

    def create_table(self, table, db='db', insert_data=True):
        """"""
        objects = self.parent.config.dikt['dstruct']['database']['objects']['table']
        logma.info(f"Table {table} {objects[table]['columns']} {len(objects[table].get('records', []) or [])} {len(objects[table].get('system_records', []) or [])}")
        return super().create_table(table, objects[table], db, insert_data=insert_data)

    def create_view(self, view, db='db'):
        """"""
        objects = self.parent.config.dikt['dstruct']['database']['objects']['view']
        return super().create_view(view, objects[view]['cmd'], db)

    def delete_record(self, table, primary_key=None, uuid=None, column=None, db='db', flip=False):
        """"""
        if primary_key is not None:
            return self._delete_by_primary_key(table, primary_key, db, flip)
        if uuid is not None:
            return self._delete_by_uuid(table, uuid, column, db, flip)
        return None

    def delete_table(self, table, db='db'):
        """"""
        self.docs[db].drop(table, 'table', 3333)
        return self

    def delete_views(self):
        """Delete all views for upgrade purposes"""
        views = self.get_views()
        views.apply(self.delete_view, axis=1)
        return self

    def find_backup(self, instance, version):
        """"""
        if instance is None:
            instance_path = self.app.model.store.instance_path
        else:
            instance_path = instance.instance_path
        backups = [x for x in listdir(instance_path) if '_backup_' in x]
        backups.sort(reverse=True)
        if version == 'latest':
            backup = backups[0]
        elif version == 'all':
            backup = backups
        else:
            backup = [x for x in backups if version == x]
            if len(backup) > 0:
                backup = backups[0]
        return backup

    def gen_NID(self):
        """"""
        return str(uuid())

    def get_app_action(self, cfg, db='db'):
        """Refactored using generic getter"""
        return self._get_app_view_table('app_action', cfg, db)

    def get_app_document_type(self, cfg, db='db'):
        """Refactored using generic getter"""
        return self._get_app_view_table('app_document_type', cfg, db)

    def get_app_event(self, cfg, db='db'):
        """Refactored using generic getter"""
        return self._get_app_view_table('app_event', cfg, db)

    def get_app_tab(self, params, db='db'):
        """Refactored using generic sorted getter"""
        return self._get_sorted_app_view_table('app_tab', params, ['pid_txt', 'position_int'], db)

    def get_doc_tab(self, params, db='db'):
        """Refactored using generic sorted getter"""
        return self._get_sorted_app_view_table('doc_tab', params, ['pid_txt', 'position_int'], db)

    def get_view_tab(self, cfg, db='db'):
        logma.info(f'get_view_tab requested')
        return None

    def get_app_instance(self, instance=None, most_recent=None, db='db'):
        """"""
        table = 'vw_app_instance'
        if self.instance is not None:
            if self.instance.is_independent:
                table = f'vwt_app_instance_{self.instance.alias}'
        cfg = {'table': {table: {}}}
        if instance is not None:
            cfg['table'][table] = {'WHERE': {'EQUAL': {'instance_id_txt': instance}}}
        elif most_recent is not None:
            cfg['table'][table] = {'ORDER': {'MODON_DTTM': 'DESC'}, 'TOP': most_recent}
        else:
            cfg['table'][table] = {'WHERE': {'EQUAL': {'name_txt': db}}}
        logma.info(f'Table {table} {cfg} {db}')
        df = self.get_table(table, cfg, db)
        return df

    def get_app_menu(self, tag='app', db='db'):
        """"""
        table = self._table_resolver.get_table_name('app_menu', self.instance)
        data = DataFrame()
        if data.empty:
            tags = self._build_tag_hierarchy(tag)
            params = {'WHERE': {'IN': {'tag_txt': tags}}}
            data = self.get_table(table, params, db)
        return data

    def get_app_option(self, option_table, tags=None, page_size=None, db='db'):
        """"""
        table = 'vw_app_option'
        if self.instance is not None:
            if self.instance.is_independent:
                table = f'vwt_app_option_{self.instance.alias}'
        params = {'WHERE': {'EQUAL': {'table_txt': option_table}}}
        if tags is not None:
            if not isinstance(tags, list):
                tags = list(tags)
            params['WHERE']['IN'] = {'tag_txt': tags}
        data = self.get_table(table, params, db)
        return data

    def get_app_option_key(self, cfg, db='db'):
        """"""
        table = 'vw_app_option_key'
        if self.instance is not None:
            if self.instance.is_independent:
                table = f'vwt_app_option_key_{self.instance.alias}'
        return self.get_table(table, cfg, db)

    def get_app_policy(self, cfg, db='db'):
        """"""
        table = 'vw_app_policy'
        if self.instance is not None:
            if self.instance.is_independent:
                table = f'vwt_app_policy_{self.instance.alias}'
        return self.get_table(table, cfg, db)

    def get_app_profile(self, db='db'):
        """"""
        cfg = {}
        table = 'vw_app_profile'
        if self.instance is not None:
            table = f'vwt_app_profile_{self.instance.alias}'
        return self.get_table(table, cfg, db)

    def get_app_secure_store(self, cfg, db='db'):
        """"""
        caller = inspect.currentframe().f_back.f_back.f_code.co_name
        logma.info(f'Inspect {caller}')
        white_list = ['']
        if caller in white_list:
            table = 'vw_app_secure_store'
            df = self.get_table(table, cfg, db)
            df = decrypt(df, self.user.get_password())
        else:
            raise Exception(f'Caller is not Authorized to get data from the secure store')
        return self

    def get_app_tree_node(self, cfg, db='db'):
        """"""
        table = 'vw_app_tree_node'
        if self.instance.is_independent:
            table = f'vwt_app_tree_node_{self.instance.alias}'
        return self.get_table(table, cfg, db)

    def get_app_user(self, cfg, db='db'):
        """"""
        table = 'vw_app_user'
        if self.instance.is_independent:
            table = f'vwt_app_user_{self.instance.alias}'
        return self.get_table(table, cfg, db)

    def get_app_version(self):
        """"""
        table = 'vw_app_instance'
        return self.get_table(table)

    def get_doc_media(self, recent_only=False, n=50, db='db'):
        """App document refers docucation instances"""
        table = 'vw_doc_media'
        if self.instance.is_independent:
            table = f'vwt_doc_media_{self.instance.alias}'
        params = {}
        if recent_only:
            params = {f'TOP {n}'}
        return self.get_table(table, params, db)

    def get_doc_media_content(self, cfg, db='db'):
        """"""
        table = 'vw_doc_media_content'
        if self.instance.is_independent:
            table = f'vwt_doc_media_content_{self.instance.alias}'
        return self.get_table(table, cfg, db)

    def get_doc_tree_node(self):
        logma.info(f'get_doc_tree_node requested')
        return None

    def get_doc_user(self):
        logma.info(f'get_doc_user requested')
        return None

    def get_indexes(self, instance_name='db'):
        """"""
        objects = self.parent.config.dikt['dstruct']['database']['objects']['index']
        return objects

    def get_links(self, name=None, description=None, type_=None, tag=None, url=None, db='db'):
        """"""
        table = self._table_resolver.get_table_name('link', self.instance)
        cfg = self._build_filter_config([('EQUAL', 'name_txt', name), ('LIKE', 'description_ltxt', description), ('EQUAL', 'type_txt', type_), ('EQUAL', 'tag_txt', tag), ('LIKE', 'url_ltxt', url)])
        return self.get_table(table, cfg, db)

    def get_view_border_styles(self, cfg=None, db='db'):
        """"""
        table = 'vw_border_styles'
        if self.instance is not None:
            if self.instance.is_independent:
                table = f'vwt_border_styles_{self.instance.alias}'
        return self.get_table(table, cfg, db)

    def get_view_colors(self, cfg, db='db'):
        """"""
        table = 'vw_colors'
        if self.instance is not None:
            if self.instance.is_independent:
                table = f'vwt_colors_{self.instance.alias}'
        return self.get_table(table, cfg, db)

    def get_view_maintain_doc_media_content(self, cfg=None, db='db'):
        """"""
        table = 'vw_maint_doc_media_content'
        if self.instance is not None:
            if self.instance.is_independent:
                table = f'vwt_maint_doc_media_content_{self.instance.alias}'
        return self.get_table(table, cfg, db)

    def get_view_marked_deleted(self, db='db'):
        """"""
        table = 'vw_marked_deleted'
        if self.instance is not None:
            if self.instance.is_independent:
                table = f'vwt_marked_deleted_{self.instance.alias}'
        return self.get_table(table, db=db)

    def get_view_settings(self, cfg, db='db'):
        """"""
        table = 'vw_settings'
        if self.instance is not None:
            if self.instance.is_independent:
                table = f'vwt_settings_{self.instance.alias}'
        return self.get_table(table, cfg, db)

    def get_view_settings_interface(self, cfg, db='db'):
        """"""
        table = 'vw_settings_interface'
        if self.instance is not None:
            if self.instance.is_independent:
                table = f'vwt_settings_interface_{self.instance.alias}'
        return self.get_table(table, cfg, db)

    def get_view_settings_security(self, cfg, db='db'):
        """"""
        table = 'vw_settings_security'
        if self.instance is not None:
            if self.instance.is_independent:
                table = f'vwt_settings_security_{self.instance.alias}'
        return self.get_table(table, cfg, db)

    def get_view_settings_storage(self, cfg, db='db'):
        """"""
        table = 'vw_settings_storage'
        if self.instance is not None:
            if self.instance.is_independent:
                table = f'vwt_settings_storage_{self.instance.alias}'
        return self.get_table(table, cfg, db)

    def get_view_supported_os(self, cfg, db='db'):
        """"""
        table = 'vw_supported_os'
        if self.instance is not None:
            if self.instance.is_independent:
                table = f'vwt_supported_os_{self.instance.alias}'
        return self.get_table(table, cfg, db)

    def get_view_tree_node(self, cfg, db='db'):
        """"""
        table = 'vw_tree_node'
        if self.instance is not None:
            if self.instance.is_independent:
                table = f'vwt_tree_node_{self.instance.alias}'
        return self.get_table(table, cfg, db)

    def get_views(self, instance_name='db'):
        objects = self.parent.config.dikt['dstruct']['database']['objects']['view']
        return objects

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
        if self.config.dikt.get('args', None):
            reset = None if 'setup' not in self.config.dikt.get('args', []) else 3333
        logma.info(f'Reset: {reset}')
        database_file_name = join(self.application_path, f'{self.name}{extension}')
        object_name = 'db'
        document_type = 'sonql'
        self.initDocument(object_name, document_type, database_file_name, self.config.dikt, reset)
        object_name = 'dbc'
        document_type = 'conql'
        self.initDocument(object_name, document_type)
        return self

    def init_database_instance(self, instance, attach=True, reset=None):
        """
        Need to add an attach process here to attach the instance database to the application database


        :param file_name:
        :param reset:
        :return:
        """
        document_type = 'sonql'
        tables = self.config.dikt.get('tables').dikt
        self.initDocument(instance.db_instance_id, document_type, instance.get_file_path(), tables, reset)
        document_type = 'conql'
        self.initDocument(instance.dbc_instance_id, document_type)
        if self.app.new_instance:
            self.policy.init_policies()
            self.store_doc_instance(instance.db_instance_id, f'dbi_{instance.db_instance_id}')
        return self

    def initDocument(self, name, doc_type, path=None, objects=None, reset=None):
        """"""
        self.objects = objects
        logma.info(f'Initializing {name} {doc_type}')
        logma.info(f'Path: {path}')
        super().initDocument(name, doc_type, path, objects, reset)
        return self

    def store_app_action(self, data, cfg=None, db='db', how='INSERT'):
        """Refactored with centralized validation and payload building"""
        operation = self._validate_operation(how)
        payload_cfg = self._build_store_payload('app_action', data, operation, cfg)
        self._store('app_action', payload_cfg.get('table', {}).get('app_action', {}).get('records', []), cfg)
        return self

    def store_app_document_type(self, data, cfg=None, db='db', how='INSERT'):
        """Refactored with centralized validation and payload building"""
        operation = self._validate_operation(how)
        payload_cfg = self._build_store_payload('app_document_type', data, operation, cfg)
        self._store('app_document_type', payload_cfg.get('table', {}).get('app_document_type', {}).get('records', []))
        return self

    def store_app_options_batch(self, options, tag=None, db='db'):
        """Store multiple options efficiently in batch"""
        if self.user is None:
            user_FK = DEFAULT_USER_ID
        else:
            user_FK = self.user.FK
        payloads = []
        for option in options:
            if isinstance(option, dict):
                payloads.append([uuid(), option.get('key'), option.get('label'), option.get('value'), option.get('table'), tag or option.get('tag'), option.get('parent_id', 0), user_FK])
        self._store('app_option', payloads)
        return self

    def store_links_batch(self, links, db='db'):
        """Store multiple links efficiently in batch"""
        payloads = []
        for link in links:
            payloads.append([uuid(), link.get('name', ''), link.get('type', ''), link.get('description', ''), link.get('url'), link.get('tag', '')])
        self._store('link', payloads)
        return self

    def store_app_event(self, state, eventtype, g_command='', db='db', how='INSERT'):
        """

        'UUID', 'state_txt', 'user_nm_txt', 'MAC', 'events_dttm', 'application_new_bit', 'instance_new_bit',
        'eventtype_txt', 'command_txt', 'instance_FK', 'application_NCD', 'device_dict'

        :param state:
        :param eventtype:
        :param g_command:
        :return:
        """
        table = 'app_event'
        if how == 'INSERT':
            payload = []
        elif how == 'UPDATE':
            payload = [{}]
        elif how == 'DEACTIVATE':
            payload = []
        elif how == 'DELETE':
            payload = []
        elif how == 'ARCHIVE':
            payload = []
        else:
            raise Exception(f'{how} is not supported.')
        return self

    def store_app_instance(self, instance, db='db', how='INSERT'):
        """
                    'columns': ['instance_id', 'name', 'is_new', 'application_NCD',
                        'application_path', 'instance_path']
        :return:
        """
        table = 'app_instance'
        if how == 'INSERT':
            payload = []
        elif how == 'UPDATE':
            payload = [{}]
        elif how == 'DEACTIVATE':
            payload = []
        elif how == 'DELETE':
            payload = []
        elif how == 'ARCHIVE':
            payload = []
        else:
            raise Exception(f'{how} is not supported.')
        if how == 'INSERT':
            payload = [[instance.instance_id, instance.name, instance.description, instance.is_primary, instance.application_NCD, instance.application_path, instance.instance_path, instance.version, encode64(json.dumps(instance.meta_data))]]
            self._store(table, payload)
        elif how == 'UPDATE':
            payload = [{'name': instance.name, 'application_path': instance.application_path, 'instance_path': instance.instance_path, 'meta_data_enc64_dict': encode64(json.dumps(instance.meta_data))}]
            column = 'instance_id'
            values = [instance.instance_id]
            cfg = {'WHERE': {'IN': {column: values}}}
            self._store(table, payload, cfg)
        return self

    def store_app_media(self, document, db='db', how='INSERT'):
        """"""
        table = 'app_media'
        if how == 'INSERT':
            payload = []
        elif how == 'UPDATE':
            payload = [{}]
        elif how == 'DEACTIVATE':
            payload = []
        elif how == 'DELETE':
            payload = []
        elif how == 'ARCHIVE':
            payload = []
        else:
            raise Exception(f'{how} is not supported.')
        payload = [[document['did'], document.get('compatibility', 'pyffice'), document['document_type'], document['syntax'], document['name'], document['file_name'], document['description'], document['path'], document['location'], document['encoding'], '|'.join(document['tags']), document['version'], document['hash'], document['policy'], encode64(json.dumps(document.get('metadata', {})))]]
        self._store(table, payload, db)
        return document['did']

    def store_app_media_content(self, content, db='db', how='INSERT'):
        """"""
        table = 'app_media_content'
        if how == 'INSERT':
            payload = []
        elif how == 'UPDATE':
            payload = [{}]
        elif how == 'DEACTIVATE':
            payload = []
        elif how == 'DELETE':
            payload = []
        elif how == 'ARCHIVE':
            payload = []
        else:
            raise Exception(f'{how} is not supported.')
        payload = [[content['uuid'], content['pUUID'], content['page'], content['entry'], _coerce_doc_version(content.get('version')) + 1, content['hash'], content['content'], content['context']]]
        self._store(table, payload, db)
        return content['uuid']

    @staticmethod
    def _coerce_doc_version(raw) -> int:
        """Best-effort integer document-version coercion.

        The desktop app historically stored ``content["version"]`` as an
        int, but a few legacy record formats (e.g. older PDF/Sketch saves,
        hand-edited YAML records) carry version strings like ``"1.0.1.0"``
        or floats like ``0.0``. Treating those as integers raised::

            ValueError: invalid literal for int() with base 10: '1.0.1.0'
            TypeError: unsupported operand type(s) for +: 'float' and 'int'

        We keep the legacy behaviour (integer version) for new writes, but
        accept legacy / partial values by falling back to a hash-derived
        integer so the document still saves.
        """
        try:
            if raw is None or raw == '':
                return 0
            return int(raw)
        except (TypeError, ValueError):
            import hashlib
            digest = hashlib.md5(str(raw).encode('utf-8')).hexdigest()
            return int(digest[:8], 16) & 2147483647

    def store_app_menu(self, db='db', how='INSERT'):
        logma.info(f'store_app_menu called')
        return self

    def store_app_option(self, option, key=None, vtable=None, tag=None, option_FK=DEFAULT_USER_ID, db='db', how='INSERT'):
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
        table = 'app_option'
        if how == 'INSERT':
            payload = []
        elif how == 'UPDATE':
            payload = [{}]
        elif how == 'DEACTIVATE':
            payload = []
        elif how == 'DELETE':
            payload = []
        elif how == 'ARCHIVE':
            payload = []
        else:
            raise Exception(f'{how} is not supported.')
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
                    payload.append([uuid(), op['key'], op['label'], op['option'], op['table'], tag, option_FK, user_FK])
        else:
            payload = [[uuid(), key, option, vtable, tag, option_FK, self.instance_FK, user_FK]]
        self._store(table, payload)
        return self

    def store_app_option_key(self, db='db', how='INSERT'):
        """
                    'columns': ['UUID', 'app_option_FK_0', 'virtual_table_txt', 'table_txt', 'app_option_FK_1', 'instance_FK', 'user_FK']
        :return:
        """
        if how == 'INSERT':
            payload = []
        elif how == 'UPDATE':
            payload = [{}]
        elif how == 'DEACTIVATE':
            payload = []
        elif how == 'DELETE':
            payload = []
        elif how == 'ARCHIVE':
            payload = []
        else:
            raise Exception(f'{how} is not supported.')
        return self

    def store_app_policy(self, record, db='db', how='INSERT'):
        """
                    columns: ["UUID", "type", "target", "policy"]
        :param record:
        :return:
        """
        table = 'app_policy'
        if how == 'INSERT':
            payload = []
        elif how == 'UPDATE':
            payload = [{}]
        elif how == 'DEACTIVATE':
            payload = []
        elif how == 'DELETE':
            payload = []
        elif how == 'ARCHIVE':
            payload = []
        else:
            raise Exception(f'{how} is not supported.')
        self._store('app_policy', [record])
        return self

    def store_app_profile(self, record, db='db', how='INSERT'):
        logma.info(f'store_app_profile called')
        return self

    def store_app_secure_store(self, db='db', how='INSERT'):
        """
                    columns: ['UUID', 'userUUID', 'key', 'value']
        :return:
        """
        table = 'app_secure_store'
        if how == 'INSERT':
            payload = []
        elif how == 'UPDATE':
            payload = [{}]
        elif how == 'DEACTIVATE':
            payload = []
        elif how == 'DELETE':
            payload = []
        elif how == 'ARCHIVE':
            payload = []
        else:
            raise Exception(f'{how} is not supported.')
        cfg = {'table': table}
        reader = self.docs['db'].read(cfg)
        df = next(reader).dikt[table]['df']
        return self

    def store_app_tab(self, row, instance=None, db='db', how='INSERT'):
        """
                    'columns': ['name_txt', 'widget_txt', 'widgdata_dict', 'pid_txt', 'did_txt', 'position_int',
                                'document_type_txt', 'tabset_type_txt', 'readonly_bit', 'editable_bit', 'visible_bit',
                                'moveable_bit', 'UUID']
        :param row:
        :param instance:
        :return:
        """
        table = 'app_tab'
        if how == 'INSERT':
            payload = []
        elif how == 'UPDATE':
            payload = [{}]
        elif how == 'DEACTIVATE':
            payload = []
        elif how == 'DELETE':
            payload = []
        elif how == 'ARCHIVE':
            payload = []
        else:
            raise Exception(f'{how} is not supported.')
        payload = [row]
        self._store(table, payload)
        return self

    def store_app_tree_nodes(self, data, db='db', how='INSERT'):
        """
                    columns: ['nid', 'icon', 'name', 'ntype', 'parentid', 'position', 'parameters', 'source',
                      'treeid', 'readonly', 'editable', 'visible', 'moveable',
                      'pregnable', 'isparent', 'expanded', 'tabfocus']
        :param data:
        :return:
        """
        if how == 'INSERT':
            payload = []
        elif how == 'UPDATE':
            payload = [{}]
        elif how == 'DEACTIVATE':
            payload = []
        elif how == 'DELETE':
            payload = []
        elif how == 'ARCHIVE':
            payload = []
        else:
            raise Exception(f'{how} is not supported.')
        if isinstance(data, DataFrame):
            self._store_df(self.nodetable, data, {'how': 'IF NOT EXISTS', self.nodetable: 'nid'})
        elif isinstance(data, list):
            self._store(self.nodetable, data, {'how': 'IF NOT EXISTS', self.nodetable: 'nid'})
        return self

    def store_app_tree_node(self, name, ntype, pid, pos, parameters=None, tree='left', db='db', how='INSERT'):
        """"""
        if how == 'INSERT':
            payload = []
        elif how == 'UPDATE':
            payload = [{}]
        elif how == 'DEACTIVATE':
            payload = []
        elif how == 'DELETE':
            payload = []
        elif how == 'ARCHIVE':
            payload = []
        else:
            raise Exception(f'{how} is not supported.')
        icon = ''
        nid = self.gen_NID()
        if parameters is None:
            parameters = {'focus': 'office'}
        if isinstance(parameters, dict):
            parameters = json.dumps(parameters)
        row = [nid, icon, name, ntype, pid, str(pos), parameters] + self.app.view.panes[tree].tree.model.nodebase
        data = {'app_tree_node': {'records': [row], 'columns': self.app.view.panes[tree].tree.model.nodecolumns}}
        self.docs['db'].write(data)
        return (nid, row)

    def store_app_user(self, user, db='db', how='INSERT'):
        """
                    'columns': ['UUID', 'mac_hash', 'user_nm_txt', 'password_txt', 'saltUUID', 'iterations_txt', 'address_txt',
                        'public_key_txt', 'is_private_bit', 'is_secure_bit', 'instance_FK', 'application_new_bit',
                        'instance_new_bit']
        :param user:
        :param db:
        :return:
        """
        table = 'app_user'
        if how == 'INSERT':
            payload = []
        elif how == 'UPDATE':
            payload = [{}]
        elif how == 'DEACTIVATE':
            payload = []
        elif how == 'DELETE':
            payload = []
        elif how == 'ARCHIVE':
            payload = []
        else:
            raise Exception(f'{how} is not supported.')
        payload = [[user.uuid, text_hashing_function(user.parent.device.mac), user.parent.device.user, encode64(user.hash), encode64(user.salt), encode64(str(user.iters)), encode64(user.address), encode64(user.rsa_key), self.app.model.is_private, self.app.model.is_secure, self.app.model.instance.instance_id]]
        FK = self._store(table, payload, db)
        return (FK, payload[0])

    def store_doc_media(self, db='db', how='INSERT'):
        """"""
        if how == 'INSERT':
            payload = []
        elif how == 'UPDATE':
            payload = [{}]
        elif how == 'DEACTIVATE':
            payload = []
        elif how == 'DELETE':
            payload = []
        elif how == 'ARCHIVE':
            payload = []
        else:
            raise Exception(f'{how} is not supported.')

    def store_doc_media_content(self, db='db', how='INSERT'):
        """"""
        if how == 'INSERT':
            payload = []
        elif how == 'UPDATE':
            payload = [{}]
        elif how == 'DEACTIVATE':
            payload = []
        elif how == 'DELETE':
            payload = []
        elif how == 'ARCHIVE':
            payload = []
        else:
            raise Exception(f'{how} is not supported.')

    def store_doc_tab(self, row, instance, db='db', how='INSERT'):
        """
            'columns': ['name_txt', 'widget_txt', 'widgdata_dict', 'pid_txt', 'did_txt', 'position_int', 'document_type_txt',
                        'tabset_type_txt', 'readonly_bit', 'editable_bit', 'visible_bit', 'moveable_bit', 'UUID']
        :param row:
        :param instance:
        :return:
        """
        table = 'doc_tab'
        if how == 'INSERT':
            payload = []
        elif how == 'UPDATE':
            payload = [{}]
        elif how == 'DEACTIVATE':
            payload = []
        elif how == 'DELETE':
            payload = []
        elif how == 'ARCHIVE':
            payload = []
        else:
            raise Exception(f'{how} is not supported.')
        payload = [row]
        self._store(table, payload, db)
        return self

    def store_doc_tree_node(self, name, ntype, pid, pos, parameters=None, tree='left', db='db', how='INSERT'):
        """"""
        if how == 'INSERT':
            payload = []
        elif how == 'UPDATE':
            payload = [{}]
        elif how == 'DEACTIVATE':
            payload = []
        elif how == 'DELETE':
            payload = []
        elif how == 'ARCHIVE':
            payload = []
        else:
            raise Exception(f'{how} is not supported.')
        icon = ''
        nid = self.gen_NID()
        if parameters is None:
            parameters = {'focus': 'office'}
        if 'recent_tab' not in parameters.keys():
            parameters['recent_tab'] = {'center': 0, 'right': 0}
        if isinstance(parameters, dict):
            parameters = json.dumps(parameters)
        row = [nid, icon, name, ntype, pid, str(pos), parameters] + self.app.view.panes[tree].tree.model.nodebase
        data = {'doc_tree_node': {'records': [row], 'columns': self.app.view.panes[tree].tree.model.nodecolumns}}
        self.docs['db'].write(data)
        return (nid, row)

    def store_doc_user(self, db='db', how='INSERT'):
        """
                    'columns': ['UUID', 'MAC', 'user_nm_txt', 'password_txt', 'saltUUID', 'iterations_txt', 'address_txt',
                        'public_key_txt', 'is_private_bit', 'is_secure_bit', 'instance_FK', 'application_new_bit',
                        'instance_new_bit']
        :return:
        """
        if how == 'INSERT':
            payload = []
        elif how == 'UPDATE':
            payload = [{}]
        elif how == 'DEACTIVATE':
            payload = []
        elif how == 'DELETE':
            payload = []
        elif how == 'ARCHIVE':
            payload = []
        else:
            raise Exception(f'{how} is not supported.')
        return self

    def store_link(self, url, name='', type_='', description='', tag='', db='db', how='INSERT'):
        """
                    columns: ["UUID", "name", "type", "description", 'url_ltxt', "tag_txt"]
        :return:
        """
        if how == 'INSERT':
            payload = []
        elif how == 'UPDATE':
            payload = [{}]
        elif how == 'DEACTIVATE':
            payload = []
        elif how == 'DELETE':
            payload = []
        elif how == 'ARCHIVE':
            payload = []
        else:
            raise Exception(f'{how} is not supported.')
        table = 'link'
        if not isinstance(url, list):
            url = [url]
        for url_ in url:
            payload = [[uuid(), name, type_, description, url_, tag]]
            self._store(table, payload)
        return self

    # TODO edit name
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
            cfg['WHERE'] = where
        return cfg

    def _build_store_payload(self, table, data, operation, cfg=None):
        """Standardized payload building for store operations"""
        self._validate_operation(operation)
        if operation == 'INSERT':
            if isinstance(data, list):
                payload = data if data else []
            else:
                payload = [data]
        elif operation == 'UPDATE':
            payload = [data] if isinstance(data, dict) else data
        else:
            payload = []
        return {'table': {table: {'records': payload}}}

    def _build_tag_hierarchy(self, tag: str) -> list:
        """Build tag hierarchy efficiently - O(n) instead of O(n²)"""
        if '.' not in tag:
            return [tag]
        tags = []
        parts = tag.split('.')
        for i in range(len(parts)):
            tags.append('.'.join(parts[:i + 1]))
        return tags

    @property
    def _db_objects(self):
        """Lazy-load db objects configuration once"""
        if not hasattr(self, '_db_objects_cache'):
            self._db_objects_cache = self.config.dikt.get('dstruct', {}).get('database', {}).get('objects', {})
        return self._db_objects_cache

    def _find_node_by_nid(self, parent_item, target_nid):
        """"""
        for i in range(parent_item.childCount()):
            item = parent_item.child(i)
            item_nid = getattr(item, 'nid', None)
            if item_nid == target_nid:
                return item
            if item.childCount() > 0:
                found = self._find_node_by_nid(item, target_nid)
                if found:
                    return found
        return None

    def _get_table_columns(self, table):
        """Get table columns from config with lazy loading"""
        tables = self._db_objects.get('table', {})
        return tables.get(table, {}).get('columns', [])

    def _get_app_view_table(self, view_name, cfg=None, db='db'):
        """Generic method to eliminate repetitive get_app_* methods"""
        table = self._table_resolver.get_table_name(view_name, self.instance)
        return self.get_table(table, cfg, db)

    def _get_sorted_app_view_table(self, view_name, cfg=None, sort_by=None, db='db'):
        """Get and sort app view table"""
        df = self._get_app_view_table(view_name, cfg, db)
        if sort_by and (not df.empty):
            df = df.sort_values(by=sort_by)
        return df

    def _select_initial_node(self, instance):
        """"""
        home_node_nid = '067ca837-17f6-74e7-8000-f7de9b7927f1'
        last_node_nid = instance.meta_data.get('last_node_nid_txt') if instance.meta_data else None
        if last_node_nid:
            target_nid = last_node_nid
            logma.info(f'Restoring last selected node: {target_nid}')
        else:
            target_nid = home_node_nid
            logma.info(f'Defaulting to Home node: {target_nid}')
        try:
            tree = self.app.view.panes.get('left')
            if tree and tree.tree and tree.tree.model:
                root = tree.tree.model.invisibleRootItem()
                target_node = self._find_node_by_nid(root, target_nid)
                if target_node:
                    tree.tree.view.set_current_node(target_node)
                    logma.info(f'Selected node: {target_node.text(0)}')
                else:
                    logma.warning(f'Node {target_nid} not found, falling back to Home')
                    target_node = self._find_node_by_nid(root, home_node_nid)
                    if target_node:
                        tree.tree.view.set_current_node(target_node)
        except Exception as e:
            logma.warning(f'Could not select initial node: {e}')
        return self

    def _validate_operation(self, operation):
        """Centralized operation validation"""
        return PayloadBuilder.validate_and_get_operation(operation)

def get_node_base(nodetype, treeid=0, tabfocus=0):
    """"""
    if nodetype == 'appnode':
        base = [1, 0, 1, 0, 1, 1, 1]
    elif nodetype == 'datanode':
        base = [1, 0, 1, 0, 1, 1, 0]
    elif nodetype == 'usernode':
        base = [1, 0, 1, 0, 1, 1, 0]
    return treeid + base + tabfocus
TABLE_NAMES = ['documents', 'document_versions', 'document_links', 'chunks', 'chunks_fts', 'query_associations', 'webhooks', 'vec_chunks', 'scheduled_queries']

class GlainNchantdStore:
    """
    Glain Integration for NchantdStore.

    Allows embedding Glain knowledge base tables inside an existing
    NchantdStore (or any SQLite) database.

    Usage:
        # In NchantdStore application
        from glain.nchantdstore import GlainNchantdStore

        # Create or attach to existing database
        glain = GlainNchantdStore(
            connection=store.docs['db'].conn,  # Use NchantdStore's connection
            table_prefix="glain"                # Prefix to avoid collisions
        )

        # Use Glain as normal
        doc_id = glain.add_document("My document content")
        results = glain.search_fts("search query")
    """
    DEFAULT_PREFIX = 'glain'

    def __init__(self, connection: Optional[sqlite3.Connection]=None, db_path: Optional[str]=None, table_prefix: str=DEFAULT_PREFIX):
        """
        Initialize Glain for NchantdStore.

        Args:
            connection: SQLite connection (from NchantdStore)
            db_path: Path to database file (if creating standalone)
            table_prefix: Prefix for Glain tables (default: "glain")
        """
        self.table_prefix = table_prefix
        if self.table_prefix and (not self.table_prefix.endswith('_')):
            self.table_prefix += '_'
        self._db = GlainDatabase(db_path=db_path or ':memory:', conn=connection, table_prefix=table_prefix, load_extensions=True)
        if table_prefix:
            self._apply_prefixes()
        logma.info(f'GlainNchantdStore initialized')

    def _apply_prefixes(self):
        """Apply table prefix to internal database."""
        pass

    def _prefix_table(self, table: str) -> str:
        """Get prefixed table name."""
        if self.table_prefix:
            return f'{self.table_prefix}{table}'
        return table

    def add_document(self, content: str, metadata: Optional[Dict[str, Any]]=None, entities: Optional[List[Dict[str, Any]]]=None, summary: Optional[str]=None, privacy_level: str='public') -> int:
        """Add a document to the knowledge base."""
        return self._db.add_document(content=content, metadata=metadata, entities=entities, summary=summary, privacy_level=privacy_level)

    def add_chunk(self, doc_id: int, content: str, embedding):
        """Add a chunk to a document."""
        return self._db.add_chunk(doc_id, content, embedding)

    def add_chunks_batch(self, doc_id: int, contents: List[str], embeddings):
        """Add multiple chunks at once."""
        return self._db.add_chunks_batch(doc_id, contents, embeddings)

    def get_document(self, doc_id: int) -> Optional[Dict[str, Any]]:
        """Get a document by ID."""
        return self._db.get_document(doc_id)

    def search_fts(self, query: str, limit: int=10, metadata_filter: Optional[Dict[str, Any]]=None, privacy_levels: Optional[List[str]]=None) -> List[Dict[str, Any]]:
        """Full-text search."""
        return self._db.search_fts(query=query, limit=limit, metadata_filter=metadata_filter, privacy_levels=privacy_levels)

    def search_vector(self, query_embedding, limit: int=10, metadata_filter: Optional[Dict[str, Any]]=None, privacy_levels: Optional[List[str]]=None) -> List[Dict[str, Any]]:
        """Vector similarity search."""
        return self._db.search_vector(query_embedding=query_embedding, limit=limit, metadata_filter=metadata_filter, privacy_levels=privacy_levels)

    def delete_document(self, doc_id: int):
        """Delete a document and its chunks."""
        return self._db.delete_document(doc_id)

    def update_document(self, doc_id: int, content: Optional[str]=None, metadata: Optional[Dict[str, Any]]=None, privacy_level: Optional[str]=None):
        """Update a document."""
        return self._db.update_document(doc_id=doc_id, content=content, metadata=metadata, privacy_level=privacy_level)

    def get_document_versions(self, doc_id: int) -> List[Dict[str, Any]]:
        """Get version history of a document."""
        return self._db.get_document_versions(doc_id)

    def revert_document(self, doc_id: int, version_number: int):
        """Revert document to a specific version."""
        return self._db.revert_document(doc_id, version_number)

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        return self._db.get_stats()

    def list_documents(self, limit: int=100, offset: int=0) -> List[Dict[str, Any]]:
        """List documents with pagination."""
        return self._db.list_documents(limit=limit, offset=offset)

    def get_all_chunks(self) -> List[Dict[str, Any]]:
        """Get all chunks."""
        return self._db.get_all_chunks()

    def get_filtered_chunks(self, metadata_filter: Optional[Dict[str, Any]]=None, include_embeddings: bool=True, privacy_levels: Optional[List[str]]=None) -> List[Dict[str, Any]]:
        """Get chunks with filtering."""
        return self._db.get_filtered_chunks(metadata_filter=metadata_filter, include_embeddings=include_embeddings, privacy_levels=privacy_levels)

    def add_webhook(self, url: str, keyword: str) -> int:
        """Add a webhook."""
        return self._db.add_webhook(url, keyword)

    def list_webhooks(self) -> List[Dict[str, Any]]:
        """List all webhooks."""
        return self._db.list_webhooks()

    def delete_webhook(self, webhook_id: int):
        """Delete a webhook."""
        return self._db.delete_webhook(webhook_id)

    def get_webhooks_by_keyword(self, keyword: str) -> List[str]:
        """Get webhook URLs by keyword."""
        return self._db.get_webhooks_by_keyword(keyword)

    def add_scheduled_query(self, query_text: str, interval_seconds: int, metadata_filter: Optional[Dict[str, Any]]=None, privacy_levels: Optional[List[str]]=None) -> int:
        """Add a scheduled query."""
        return self._db.add_scheduled_query(query_text=query_text, interval_seconds=interval_seconds, metadata_filter=metadata_filter, privacy_levels=privacy_levels)

    def list_scheduled_queries(self) -> List[Dict[str, Any]]:
        """List all scheduled queries."""
        return self._db.list_scheduled_queries()

    def delete_scheduled_query(self, query_id: int):
        """Delete a scheduled query."""
        return self._db.delete_scheduled_query(query_id)

    def get_pending_scheduled_queries(self) -> List[Dict[str, Any]]:
        """Get queries due to run."""
        return self._db.get_pending_scheduled_queries()

    def update_scheduled_query_run(self, query_id: int):
        """Update scheduled query after running."""
        return self._db.update_scheduled_query_run(query_id)

    def add_query_association(self, query_text: str, chunk_id: int):
        """Associate a query with a chunk."""
        return self._db.add_query_association(query_text, chunk_id)

    def get_associated_queries(self, chunk_id: int) -> List[str]:
        """Get queries associated with a chunk."""
        return self._db.get_associated_queries(chunk_id)

    def get_expanded_associated_chunks(self, query_text: str) -> List[int]:
        """Get 2-hop expanded chunks for a query."""
        return self._db.get_expanded_associated_chunks(query_text)

    def add_document_link(self, source_id: int, target_id: int, reason: str, score: float):
        """Add a link between documents."""
        return self._db.add_document_link(source_id, target_id, reason, score)

    def get_document_links(self, doc_id: int) -> List[Dict[str, Any]]:
        """Get links from a document."""
        return self._db.get_document_links(doc_id)

    def update_document_summary(self, doc_id: int, summary: str):
        """Update document summary."""
        return self._db.update_document_summary(doc_id, summary)

    def update_document_entities(self, doc_id: int, entities: List[Dict[str, Any]]):
        """Update document entities."""
        return self._db.update_document_entities(doc_id, entities)

    def merge_database(self, source_db_path: str) -> Dict[str, Any]:
        """Merge another Glain database."""
        return self._db.merge_database(source_db_path)

    @property
    def connection(self) -> sqlite3.Connection:
        """Get the SQLite connection."""
        return self._db.conn

    def close(self):
        """Close the database connection."""
        if hasattr(self._db, '_owns_connection') and self._db._owns_connection:
            self._db.conn.close()

def attach_glain(nchantdstore_instance, table_prefix: str='glain') -> GlainNchantdStore:
    """
    Attach Glain to an existing NchantdStore instance.

    Args:
        nchantdstore_instance: An instance of NchantdStore or MicroStash
        table_prefix: Prefix for Glain tables

    Returns:
        GlainNchantdStore instance

    Usage:
        from glain.nchantdstore import attach_glain

        # In your NchantdStore application
        store = NchantdStore('myapp')
        glain = attach_glain(store)

        # Now use Glain features
        doc_id = glain.add_document("Hello world")
    """
    connection = None
    if hasattr(nchantdstore_instance, 'docs'):
        if 'db' in nchantdstore_instance.docs:
            db_doc = nchantdstore_instance.docs['db']
            if hasattr(db_doc, 'conn'):
                connection = db_doc.conn
            elif hasattr(db_doc, '_conn'):
                connection = db_doc._conn
    if connection is None and hasattr(nchantdstore_instance, 'conn'):
        connection = nchantdstore_instance.conn
    if connection is None:
        raise ValueError('Could not find SQLite connection in NchantdStore instance. Please ensure the store is initialized.')
    return GlainNchantdStore(connection=connection, table_prefix=table_prefix)