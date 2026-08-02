"""
---
<(META)>:
    docid:
    name:
    description: >
        Migration of the a database to a new version. we should not enforce an upgrade except for on x.n.x versions.
        that means that all 0.1.x needs to be upgradable directly to 0.2.0.
    version: 0.0.0.0.0.0
    authority: filesystem
    security: seclvl2
    <(WT)>: -32
"""
from os.path import abspath, dirname, join
from typing import Optional, Dict, List, Any, Tuple
import datetime as dt
from copy import deepcopy
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.models.models import NchantdInstance
here = join(dirname(__file__), '')
log = False
logma = Logma(__name__)
debug = True
if not log:
    logma.off()
pxcfg = join(here, '_data_', 'db.yaml')

def migrate() -> None:
    logma.info(f'migrate called')
    return self

def migrate_index() -> None:
    logma.info(f'migrate_index called')
    return self

def migrate_table() -> None:
    logma.info(f'migrate_table called')
    return self

def migrate_view() -> None:
    logma.info(f'migrate_view called')
    return self

class NchantdDBUpdate(object):
    """"""

    def __init__(self, parent, cfg=None) -> None:
        """"""
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('DBUpdate').override(cfg)
        self.versions = deepcopy(self.config.dikt.get('versions'))
        self.current_version = None
        self.version = None
        self.hold_data = {}
        self.app = parent

    def add_uuid(self, table, control_column, data_column, db='db') -> Any:
        """Generate and insert a uuid to each record of a column given the filters"""
        self.app.model.store.add_uuid(table, control_column, data_column, db)
        return self

    def backup_db(self, db='db') -> None:
        """"""
        logma.info(f'Instance Active: {self.parent.app.model.instance}')
        instance = self.parent.app.model.instance
        if self.parent.app.model.instance is None:
            data = self.parent.app.model.get_instance(db)
            logma.info(f'Instance Data: {data}')
            if data.empty:
                raise Exception('No Instance Found')
            data = data.loc[0].to_dict()
        name = self.parent.model.store.backup_database(instance, db)
        return name

    def check_version(self, current_v) -> bool:
        """"""
        logma.info(f'Checking Version {current_v}')
        latest_v = self.get_latest_version()
        logma.info(f'Latest Version: {latest_v}')
        current_parts = self._parse_version_parts(current_v)
        latest_parts = self._parse_version_parts(latest_v)
        for current_level, latest_level in zip(current_parts, latest_parts):
            if current_level < latest_level:
                return True
            if current_level > latest_level:
                return False
        if len(latest_parts) > len(current_parts):
            return True
        return False

    def get_data(self, table, db='db') -> None:
        """"""
        return self.parent.app.model.store.get_table(table, None, db)

    def get_latest_version(self) -> str:
        """"""
        self.current_version = self.parent.model.get_current_version()
        logma.info(f'Current Version: {self.current_version}')
        logma.info(f'Versions: {self.versions.keys()}')
        version_data = self.versions.get(self.current_version).get('versions', None)
        if not isinstance(version_data, dict) or not version_data:
            return self.current_version
        latest_v = self.current_version
        latest_parts = self._parse_version_parts(latest_v)
        for version_key in version_data.keys():
            current_parts = self._parse_version_parts(version_key)
            is_newer = False
            for p1, p2 in zip(current_parts, latest_parts):
                if p1 > p2:
                    is_newer = True
                    break
                if p1 < p2:
                    break
            else:
                if len(current_parts) > len(latest_parts):
                    is_newer = True
            if is_newer:
                latest_v = version_key
                latest_parts = current_parts
        return latest_v

    def insert_data(self, table, data, db='db', column_map=None) -> bool:
        """"""
        try:
            if column_map:
                data = self.map_columns(data, column_map)
            self.parent.app.model.store_records(table, data, db)
            return True
        except Exception as e:
            logma.error(f'Insert failed for table {table}: {e}')
            return False

    def map_columns(self, data, column_map) -> None:
        """"""
        for column in column_map.keys():
            data[column_map[column]] = data[column]
            del data[column]
        return data

    def reload_index(self, index, db='db') -> bool:
        """"""
        try:
            self.parent.app.model.store.delete_index(index, db)
        except Exception as e:
            logma.warning(f'Index Not Deleted {e}')
        logma.info(f'RELOAD INDEX {index}')
        status = self.parent.app.model.store.create_index(index, db)
        if status == []:
            return True
        logma.info(f'INDEX Status {status}')
        return False

    def reload_table(self, table, keep, map_, filters, db='db') -> bool:
        """"""
        return self.parent.app.model.reload_table(table, keep, map_, filters, db)

    def reload_view(self, view, db='db') -> bool:
        """"""
        try:
            self.parent.app.model.store.delete_view(view, db)
        except Exception as e:
            logma.warning(f'View not Deleted {e}')
        status = self.parent.app.model.store.create_view(view, db)
        if status == []:
            return True
        logma.info(f'View Status {status}')
        return False

    def repair_table(self, cmd, db='db') -> None:
        logma.info(f'repair_table called')
        return self

    def restore_backup(self, instance, version=None) -> None:
        """"""
        self.parent.app.model.store.restore_backup(instance, version)
        return True

    def run_updates(self, db) -> str:
        """"""
        current_v = self.parent.model.get_current_version()
        logma.info(f'Current Version: {current_v}')
        if not self.check_version(current_v):
            logma.info('No updates needed')
            return current_v
        logma.info('Running Updates')
        updates_dict = self.versions.get(current_v, {})
        logma.info(f'Updates Dict: {updates_dict}')
        if not updates_dict:
            logma.info(f'No update paths found for version {current_v}')
            return current_v
        available_versions = sorted(updates_dict['versions'].keys(), key=lambda v: self._parse_version_parts(v))
        logma.info(f'Available Versions: {available_versions}')
        version = current_v
        if updates_dict.get('active', False) is False:
            logma.info('Updates are disabled')
            return current_v
        for version_key in available_versions:
            logma.info(f'Checking Version: {version_key}')
            if self._is_version_greater(version_key, version):
                update_data = updates_dict['versions'][version_key]
                if update_data is None:
                    continue
                logma.info(f'Applying update to {version_key}')
                if not self._process_single_version_update(version_key, update_data, db):
                    logma.error(f'Failed to update to {version_key}')
                    break
                version = version_key
        return version

    def run_update_indexes(self, indexes, db='db') -> bool:
        """"""
        if indexes is None:
            return True
        if indexes['reload'] is False:
            return True
        if indexes['all']:
            indexes = self.parent.app.model.store.get_indexes(db)
        else:
            indexes = indexes.get('indexes', {})
        for index, cmd in indexes.items():
            self._process_index_operations(index, cmd, db)
        return True

    def run_update_tables(self, tables, db='db') -> bool:
        """"""
        if tables is None:
            return True
        for table, params in tables.items():
            logma.info(f'Updating Table: {table}')
            if not self._process_table_operations(table, params, db):
                return False
        return True

    def run_update_views(self, views, db='db') -> bool:
        """"""
        if views is None:
            return True
        if views['reload'] is False:
            return True
        if views['all']:
            views = self.parent.app.model.store.get_views(db)
        else:
            views = views.get('views', {})
        for view, cmd in views.items():
            logma.info(f'Updating View: {view}')
            logma.info(f'Command: {cmd}')
            try:
                self._process_view_operations(view, cmd, db)
            except Exception as e:
                logma.error(f'Failed to update view {view}: {e}')
                return False
        return True

    def update(self, table, cfg, db='db') -> Any:
        """"""
        data = {'table': {table: cfg}}
        return self.parent.app.model.store.update_records(data, cfg, db)

    def _execute_update_step(self, step_name, step_function, step_data, db) -> None:
        """Execute a single update step with error handling and rollback."""
        logma.info(f'Update {step_name}')
        if not step_function(step_data, db):
            logma.error(f'{step_name} failed, restoring backup')
            logma.error(f'{step_function} failed function')
            instance = self.parent.app.model.instance
            version = None
            self.restore_backup(instance, version)
            if debug:
                raise Exception(f'Update Failed: {step_name}')
            return False
        return True

    def _is_version_greater(self, v1: str, v2: str) -> bool:
        """Returns True if v1 > v2."""
        parts1 = self._parse_version_parts(v1)
        parts2 = self._parse_version_parts(v2)
        for p1, p2 in zip(parts1, parts2):
            if p1 > p2:
                return True
            if p1 < p2:
                return False
        return len(parts1) > len(parts2)

    def _parse_version_parts(self, version_string) -> List[int]:
        """Parse version string into comparable integer parts."""
        if not version_string:
            return []
        logma.info(f'Parsing Version: {version_string}')
        return [int(part) for part in version_string.split('.') if part.isdigit()]

    def _process_single_version_update(self, version, update_data, db) -> bool:
        """Process updates for a single version."""
        logma.info(f'Processing Version {version}')
        if update_data is None:
            return True
        self.backup_db(db)
        update_steps = [('Tables', self.run_update_tables, update_data.get('tables')), ('Indexes', self.run_update_indexes, update_data.get('indexes')), ('Views', self.run_update_views, update_data.get('views'))]
        for step_name, step_function, step_data in update_steps:
            if not self._execute_update_step(step_name, step_function, step_data, db):
                return False
        try:
            self.parent.model.set_current_version(version, db)
            logma.info(f'Successfully updated to version {version}')
        except Exception as e:
            logma.error(f'Failed to update version metadata in DB: {e}')
        return True

    def _process_index_operations(self, index, params, db) -> None:
        """Process all operations for a single index."""
        if not self.reload_index(index, db):
            if debug:
                raise Exception('Reload Failed')
            return False
        return True

    def _process_table_operations(self, table, params, db) -> None:
        """Process all operations for a single table."""
        if params.get('reload', False):
            logma.info(f'Reloading Table: {table}')
            map_ = params.get('column-map', None)
            filters = params.get('filters', {})
            if not self.reload_table(table, params.get('keep-records', False), map_, filters, db):
                if debug:
                    raise Exception('Reload Failed')
                return False
        if params.get('update'):
            if not self._process_table_updates(table, params.get('update'), db):
                return False
        if params.get('insert'):
            logma.info(f"Inserting: {params.get('insert')}")
            if not self.insert_data(table, params.get('insert'), db):
                if debug:
                    raise Exception('Insert Failed')
                return False
        return True

    def _process_table_updates(self, table, updates, db) -> None:
        """Process update operations for a table."""
        for update in updates:
            logma.info(f'Updating: {update}')
            if not self.update(table, update, db):
                if debug:
                    raise Exception('Update Failed')
                return False
        return True

    def _process_view_operations(self, view, params, db) -> bool:
        """Process update operations for a view."""
        logma.info(f'Reloading View: {view}')
        if not self.reload_view(view, db):
            if debug:
                raise Exception('Reload Failed')
            return False
        return True