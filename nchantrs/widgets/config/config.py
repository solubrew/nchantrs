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
from pycurity.pyhash import text_hashing_function

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "config.yaml")
pxcfg = {}


class NchantdConfigStoreDocument(object):
    """"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("NchantdConfigStoreDocument").override(cfg)
        self.interface = None

    def get_settings(self):
        """"""
        return self

    def load_document(self, document=None):
        """"""
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        if isinstance(document, str):
            document = j.loads(document)
        self.set_document(document.get("document", {}))
        self.set_author(document.get("meta_data", {}).get("author", None))
        self.set_context(document.get("meta_data", {}).get("context", None))
        self.set_creon(document.get("meta_data", {}).get("creon", None))
        self.set_description(document.get("description", None))
        self.set_did(document.get("did", None))
        self.set_encoding(document.get("meta_data", {}).get("encoding", None))
        self.set_hash(document.get("meta_data", {}).get("hash", None))
        self.set_saved(True)
        self.set_modon(document.get("meta_data", {}).get("modon", None))
        self.set_name(document.get("name", None))
        self.set_tags(document.get("meta_data", {}).get("tags", None))
        return self

    def set_author(self, author):
        """"""
        if author is None:
            author = ""
        if author != self.author:
            self.add_change("author", self.author, author)
            self.author = author
        return self

    def set_context(self, context):
        """"""
        if context is None:
            context = ""
        if context != self.context:
            self.add_change("context", self.context, context)
            self.context = context
        return self

    def set_creon(self, creon=None):
        """"""
        if creon is None:
            creon = self.time.get_current_datetime_str()
        if creon != self.creon:
            self.add_change("creon", self.creon, creon)
            self.creon = creon
        return self

    def set_description(self, description):
        """"""
        if description is None:
            description = ""
        if description != self.description:
            self.add_change("description", self.description, description)
            self.description = description
        return self

    def set_did(self, did=None):
        """"""
        if did is None:
            did = uuid()
        if did != self.did:
            self.add_change("did", self.did, did)
            self.did = did
        return self

    def set_document(self, document):
        """"""
        if document is None:
            document = {}
        if isinstance(document, str):
            document = j.loads(document)
        self.document = document
        return self

    def set_encoding(self, encoding=None):
        """"""
        if encoding is None:
            encoding = "utf-8"
        if encoding != self.encoding:
            self.add_change("encoding", self.encoding, encoding)
            self.encoding = encoding
        return self

    def set_hash(self, hash_):
        """"""
        if hash_ is None:
            hash_ = text_hashing_function(self.context)
        logma.info(f"Hash {hash_}")
        # TODO need to determine what parts get hased and when/where that happens
        if hash_ != self.hash:
            self.add_change("hash", self.hash, hash_)
            self.hash = hash_
        return self

    def set_meta_data(self, meta_data):
        """"""
        if meta_data != self.meta_data:
            self.add_change("meta_data", self.meta_data, meta_data)
            self.meta_data = meta_data
        return self

    def set_modon(self, modon=None):
        """"""
        if modon is None:
            modon = self.time.get_current_datetime_str()
        if modon != self.modon:
            self.add_change("modon", self.modon, modon)
            self.modon = modon
        return self

    def set_name(self, name):
        """"""
        if name is None:
            name = self.did
        if name != self.name:
            self.add_change("name", self.name, name)
            self.name = name
        return self

    def set_saved(self, saved):
        """"""
        if saved != self.is_saved:
            self.add_change("saved", self.is_saved, saved)
            self.is_saved = saved
        return self

    def set_settings_account(self, account=None):
        """"""
        return self

    def set_settings_extensions(self, extensions=None):
        """"""
        # HOLD
        return self

    def set_settings_interface(self, interface=None):
        """"""
        self.enable_journal_node = True
        self.enable_settings_node = True
        self.show_left_pane = True
        self.show_quick_toolbar = True
        self.quick_launch_documents = {}
        self.show_document_catalog = True
        self.create_default_tab = True
        self.default_tab_type = "Nchantd Script"
        self.refocus_right_side_tab = True
        self.show_right_side_tab = True
        self.right_side_tab_type = "Journal"
        self.right_side_tabs = {}
        return self

    def set_settings_security(self, security=None):
        """"""
        self.user = security.get("user", None)
        # password
        self.lock_screen_enable = True
        self.lock_screen_time_out_mins = 15
        self.lock_screen_pin_enable = True
        # pin
        return self

    def set_settings_storages(self, storages=None):
        """"""
        self.auto_save_enable = True
        self.auto_save_interval_mins = 15
        self.marked_deleted_hold = True
        self.marked_deleted_hold_days = 3
        self.document_storage_type = "In-Place"  # Locally Managed Library, Internal Database
        self.library_path = ""
        self.document_file_path = ""
        self.document_file_name = ""
        return self

    def set_settings_theme(self, theme="midnight_mist"):
        """"""
        self.theme = theme
        return self

    def set_tags(self, tags):
        """"""
        if tags is None:
            tags = []
        if tags != self.tags:
            self.add_change("tags", self.tags, tags)
            self.tags = tags
        return self

    def to_dict(self):
        """"""
        doc = {}
        doc["document"] = {}
        document = doc["document"]
        if self.interface is not None:
            document["interface"]["is_changed"] = self.interface.is_changed
            document["interface"]["enable_journal_focus"] = self.interface.enable_journal_focus_bit
            document["interface"]["enable_settings_focus"] = self.interface.enable_settings_focus_bit
            document["interface"]["enable_automation"] = self.interface.enable_automation_bit
            document["interface"]["enable_data_sources"] = self.interface.enable_data_sources_bit
            document["interface"]["show_left_pane"] = self.interface.show_left_pane
            document["interface"]["show_quick_toolbar"] = self.interface.show_quick_toolbar
            document["interface"]["show_document_catalog"] = self.interface.show_document_catalog
            document["interface"]["set_default_tab"] = self.interface.create_default_tab
            document["interface"]["set_right_side_tab"] = self.interface.refocus_right_side_tab
            document["interface"]["set_d"] = self.interface.default_right_side_tab
            document["interface"][""] = self.interface.show_right_side_tab
        else:
            document["interface"]["is_changed"] = False
        document["storage"] = {}
        if self.storage is not None:
            document["storage"]["is_changed"] = self.storage.is_changed
        else:
            document["storage"]["is_changed"] = False
        document["security"] = {}
        if self.security is not None:
            document["security"]["is_changed"] = self.security.is_changed
        else:
            document["security"]["is_changed"] = False
        document["theme"] = {}
        if self.theme is not None:
            document["theme"]["is_changed"] = self.theme.is_changed
        else:
            document["theme"]["is_changed"] = False
        document["account"] = {}
        if self.account is not None:
            document["account"]["is_changed"] = self.account.is_changed
        else:
            document["account"]["is_changed"] = False
        return doc

    def to_string(self):
        """"""
        return j.dumps(self.to_dict())


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
