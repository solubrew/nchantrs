"""
Debug Utilities Module

Provides dump utilities for debugging Nchantrs data sources.
Includes database inspection, model state dumps, and configuration logging.
"""
import logging
from typing import Any, Dict, List, Optional
logger = logging.getLogger(__name__)

class DataSourceDumper:
    """Dump utility for Nchantrs data sources."""

    def __init__(self, store=None, model=None) -> None:
        """
        Args:
            store: NchantdStore instance (from model.store)
            model: NchantdCapeModel or NchantdCloakModel instance
        """
        self.store = store
        self.model = model
        logma.info(f'DataSourceDumper initialized')

    def get_table_names(self) -> List[str]:
        """Get list of all available table names."""
        return ['app_action', 'app_document_type', 'app_event', 'app_instance', 'app_media', 'app_media_content', 'app_menu', 'app_option', 'app_option_key', 'app_policy', 'app_secure_store', 'app_user', 'app_vectored_data', 'doc_media', 'doc_media_content', 'doc_user', 'link']

    def dump_store_info(self) -> Dict[str, Any]:
        """Dump store metadata and configuration."""
        result = {'state': {}, 'error': None}
        if not self.store:
            result['error'] = 'No store available'
            return result
        try:
            result['state'] = {'name': self.store.name if hasattr(self.store, 'name') else None, 'db_path': self.store.get_file_path() if hasattr(self.store, 'get_file_path') else None, 'instance_id': self.store.instance_id if hasattr(self.store, 'instance_id') else None}
            result['tables'] = self.get_table_names()
        except Exception as e:
            result['error'] = str(e)
        return result

    def dump_model_state(self) -> Dict[str, Any]:
        """Dump model state and configuration."""
        result = {'state': {}, 'error': None}
        if not self.model:
            result['error'] = 'No model available'
            return result
        try:
            result['state'] = {'user': str(self.model.user) if self.model.user else None, 'instance': str(self.model.instance) if hasattr(self.model, 'instance') else None, 'config': str(self.model.config) if hasattr(self.model, 'config') else None, 'has_store': self.model.store is not None if hasattr(self.model, 'store') else False}
            if hasattr(self.model, 'instance') and self.model.instance:
                inst = self.model.instance
                result['instance_details'] = {'name': getattr(inst, 'name', None), 'id': getattr(inst, 'id', None)}
        except Exception as e:
            result['error'] = str(e)
        return result

    def dump_app_instances(self) -> Dict[str, Any]:
        """Dump all app instances."""
        result = {'instances': [], 'error': None}
        if not self.store:
            result['error'] = 'No store available'
            return result
        try:
            instances = self.store.get_app_instance(most_recent=10)
            result['instances'] = [{'id': str(i), 'name': getattr(i, 'name', 'unknown')} for i in instances] if instances else []
            result['count'] = len(result['instances'])
        except Exception as e:
            result['error'] = str(e)
        return result

    def dump_app_options(self, tag: str=None) -> Dict[str, Any]:
        """Dump app options, optionally filtered by tag."""
        result = {'options': [], 'error': None}
        if not self.store:
            result['error'] = 'No store available'
            return result
        try:
            options = self.store.get_app_option(tags=tag)
            result['options'] = options.to_dict() if hasattr(options, 'to_dict') else str(options)
            result['count'] = len(result['options']) if isinstance(result['options'], list) else 1
        except Exception as e:
            result['error'] = str(e)
        return result

    def dump_app_events(self, limit: int=50) -> Dict[str, Any]:
        """Dump recent app events."""
        result = {'events': [], 'error': None}
        if not self.store:
            result['error'] = 'No store available'
            return result
        try:
            events = self.store.get_app_event({}, db='db')
            result['events'] = events.to_dict() if hasattr(events, 'to_dict') else str(events)
            result['count'] = len(result['events']) if isinstance(result['events'], list) else 1
        except Exception as e:
            result['error'] = str(e)
        return result

    def dump_all(self) -> Dict[str, Any]:
        """Dump all available data sources."""
        return {'store': self.dump_store_info(), 'model': self.dump_model_state(), 'instances': self.dump_app_instances(), 'options': self.dump_app_options(), 'events': self.dump_app_events()}

def dump_data_sources(store=None, model=None) -> Dict[str, Any]:
    """
    Convenience function to dump all data sources.
    
    Args:
        store: NchantdStore instance
        model: NchantdCapeModel or NchantdCloakModel instance
        
    Returns:
        Dict containing dump of all data sources
    """
    dumper = DataSourceDumper(store, model)
    return dumper.dump_all()

def log_data_sources(store=None, model=None, level: int=logging.DEBUG) -> None:
    """
    Log all data sources at specified level.
    
    Args:
        store: NchantdStore instance
        model: NchantdCapeModel or NchantdCloakModel instance
        level: Logging level (default: DEBUG)
    """
    dumper = DataSourceDumper(store, model)
    dump = dumper.dump_all()
    logger.log(level, f'[DEBUG] Data Sources Dump: {dump}')
    if dump.get('store', {}).get('error'):
        logger.error(f"[DEBUG] Store Error: {dump['store']['error']}")
    if dump.get('model', {}).get('error'):
        logger.error(f"[DEBUG] Model Error: {dump['model']['error']}")

def quick_dump(dialog=None) -> None:
    """
    Quick dump from a dialog instance.
    
    Usage in REPL:
        >>> from nchantrs.utilities.debug import quick_dump
        >>> quick_dump(your_dialog_instance)
    """
    if not dialog:
        logger.warning('No dialog provided for quick_dump')
        return
    store = getattr(dialog, 'model', None)
    if store:
        store = getattr(store, 'store', None)
    model = getattr(dialog, 'model', None)
    dump = dump_data_sources(store=store, model=model)
    logger.debug('=' * 60)
    logger.debug('DATA SOURCES DUMP')
    logger.debug('=' * 60)
    for key, value in dump.items():
        logger.debug(f'\n--- {key.upper()} ---')
        if isinstance(value, dict):
            for k, v in value.items():
                logger.debug(f'  {k}: {v}')
        else:
            logger.debug(f'  {value}')
    return dump