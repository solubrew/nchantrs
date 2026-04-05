# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Nchantrs@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""#																			||
---  #																			||
<(META)>:  #																	||
        docid: 'a75f07e9-73f9-4622-b748-5c9cc4c88e8b'  #							||
        name: Nchantrs Application Models Python Excecution Document  #				||
        description: >  #															||
        expirary: <[expiration]>  #													||
        version: <[version]>  #														||
        path: <[LEXIvrs]>  #														||
        authority: document|this  #													||
        security: sec|lvl2  #														||
        <(WT)>: -32  #																||
"""  # ||

# -*- coding: utf-8 -*-#														||
# ================================Core Modules===================================||
from os.path import abspath, dirname, join, exists, getmtime, expanduser
from os import chmod, environ, listdir
import inspect
import platform
import base64
from math import isnan
import json as j
from shutil import copyfile
from pandas import DataFrame

import logging

logger = logging.getLogger(__name__)
# ===============================================================================||
from condor import condor
from subtrix.subtrix import Mechanism
from subtrix.utilities import uuid
from nchantrs.models.models import NchantdStore
from nchantrs.utilities.users import NchantdUser
from nchantrs.utilities.policies import NchantdDataPolicy
from nchantrs.widgets.items.nodes import NchantdTreeNode
from ogma.logma import Logma
from pycurity.pyvice import Device

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
debug = True
if not log:
    logma.off()
# ===============================================================================||
pxcfg = join(here, "_data_", "applicationmodels.yaml")


class NchantdPantiesModel(object):
    """
    Class representing the NchantdPantiesModel.

    :param parent: The parent object.
    :param cfg: The configuration object.
    """

    def __init__(self, parent=None, cfg=None) -> None:
        """
        :param parent:
        :param cfg:
        """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdPantiesModel")
        logma.info(f"Tables {self.config.dikt['dstruct']['database']['objects']['table'].keys()}")
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.app = self.parent.app
        self.app_cfg = None
        self.application_path = None
        self.instance_path = None
        self.config_path = None
        self.library_path = None
        self.instance = None
        self.instances = {}
        self.config_imported = False
        self.connections = None
        self.current_tabset = None
        if self.config.dikt.get("override_format"):
            self.config_imported = True
        self.device = None
        self.slug = self.app.slug
        self.home = environ["HOME"]
        self.parents = [self.slug, "nchantrs"]
        self.policy = None
        self.location = None
        self.listeners = None
        self.node = None
        self.store = NchantdStore(self.slug, self.parent)
        self.os_type = platform.system().lower()
        self.user = None
        self.is_private = None  # Private will enforce a basic_js login when opening the application or instance and some sensitive data is encrypted when stored
        self.is_secure = None  # Secure will enforce the same as private but also encrypt all information stored and held in cache...this will not be available unless a true security audit is compeleted
        self.instance_cfg = None
        self.reset = None

    def initialize_application(self) -> None:
        """
        Check requires_auth before creating user to avoid unnecessary password dialogs.
        """
        self.is_private = False  # Private will enforce a basic_js login when opening the application or instance and some sensitive data is encrypted when stored
        self.is_secure = False  # Secure will enforce the same as private but also encrypt all information stored and held in cache...this will not be available unless a true security audit is compeleted
        self.device = Device()
        self.policy = NchantdDataPolicy(self)
        cfg = {}
        # Only create NchantdUser if authentication is required
        # This prevents unnecessary password dialogs for apps like NchantdAXN
        requires_auth = self.config.dikt.get("config", {}).get("requires_auth", False)
        if requires_auth:
            self.user = NchantdUser(self, cfg)

    def init_model_pre(self) -> None:
        """Initialize model pre-creation"""
        return self

    def initModel(self, reset=None, pre=True, post=True) -> None:
        """Initialize the model"""
        if pre:
            self.init_model_pre()
        if post:
            self.init_model_post()
        return self

    def init_model_post(self) -> None:
        """Initialize model post-creation"""
        self.store.store_app_event("initialized", "application_model_initialized")

    def _initialize_account(self) -> None:
        """Initialize account"""
        if self.new_account is True:
            self.new_account = False  # this account is referring to the Nchantrs online service account
            self.store.store_app_event("initialized", "application_account_created")
        else:
            self.new_account = False
            self.store.store_app_event("initialized", "application_account_selected")


class NchantdCapeModel(NchantdPantiesModel):
    """Nchantd Cape is a model that allows for simple independant dialog applications"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdSigilModel")
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)
        self.initialize_application()


class NchantdCloakModel(NchantdPantiesModel):
    """The Nchantd Cloak Model sets up the connection to the data for a generic
    Nchantd Cloak application. A Cloak Application is a multipane application"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdCloakModel"))
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.store.config.override(self.config)
        self.has_library = False
        self.has_changed = False
        self.are_mini_games_active = False  # will be used to run the mini game logic
        self.is_internal_server_active = False  # will be used to run self hosted web based apps
        self.is_saved = False
        self.are_services_active = False  # will be used to connect to 3rd party services
        self.instance = None

    def initModel(self, reset=None) -> None:
        """"""
        super().initModel(reset)
        # self.set_paths()
        self.connect_nchantd_office()
        # self.user_config() #TODO need to connect user'
        # self.integration_config()
        # self.extension_config()
        return self

    def add_attachment(self, name, widgdata, pid, did, document_type, tabset_type) -> None:
        """"""
        readonly = False
        editable = True
        visible = True
        moveable = True
        row = [
            name,
            "widgets.media.documents.notes.NchantdOfficeStickyNote",  # TODO fix this shouldn't reference NchantdOffice
            widgdata,
            pid,
            did,
            document_type,
            tabset_type,
            readonly,
            editable,
            visible,
            moveable,
            uuid(),
        ]
        self.store.store_app_tab(row)

    def add_instance(self, instance) -> None:
        if instance.instance_id not in self.instances:
            self.instances[instance.instance_id] = instance
            if not instance.is_install_active:
                self.store.create_directories(instance.instance_path)
                self.store.init_database_instance(instance)
        return self

    def add_node(self, name, ntype, pid, pos, parameters=None, tabset=None, return_node=False) -> None:
        """Add a node to the document tree."""
        logma.info(f"Add Node")
        nid, row = self.store.store_doc_tree_node(name, ntype, pid, pos, parameters)
        if return_node is False:
            return nid
        columns = self.app.view.panes["left"].tree.model.nodecolumns + ["app_data_type"]
        row = row + ["doc"]
        logma.info(f"PID {pid} COLUMNS {columns}")
        if str(pid) == "0":
            parent_node = self.app.view.panes["left"].tree
        else:
            # Find the actual parent node in the tree by its nid
            parent_node = self.find_node_in_tree(pid)
            if parent_node is None:
                logma.warning(f"Parent node with nid {pid} not found in tree, using current node's parent")
                current = self.get_current_node()
                # If pid doesn't match current node's nid, this should be a sibling
                if current and str(current.nid) != str(pid):
                    parent_node = (
                        current.parent() if hasattr(current, "parent") and callable(current.parent) else current
                    )
                else:
                    parent_node = current
        logma.info(f"Parent Node {parent_node}")
        new_node = NchantdTreeNode(parent_node, name, nid, dict(zip(columns, row)))
        new_node.initWidget()
        new_node.setExpanded(True)
        if str(pid) == "0":
            parent_node.addTopLevelItem(new_node)
        else:
            parent_node.addChild(new_node)
        self.app.view.panes["left"].tree.model.current_node = new_node
        new_node.updateTabs("center")
        # Select and scroll to the new node directly without full tree refresh
        self.app.view.panes["left"].tree.view.set_current_node(new_node)
        return self

    def add_tab(
        self, name, pid, pos, widget, widgdata=None, did=None, doc_type=None, tabset=None, in_doc=True, db="db"
    ) -> None:
        """
        :param name: Name of the tab to be added.
        :param pid: Process ID associated with the tab.
        :param pos: Position where the tab should be added.
        :param widget: Widget associated with the tab.
        :return: The current instance of the object.
        """
        if widgdata is None:
            widgdata = "{}"
        if did is None:
            did = uuid()
        if doc_type is None:
            doc_type = "custom-widget"
        if tabset is None:
            tabset = "center"
        if isinstance(widgdata, dict):
            try:
                widgdata = j.dumps(widgdata)
            except Exception as e:
                logma.warning(f"Widgdata Cannot be Serialized to JSON")
                logma.warning(widgdata)
                if debug:
                    raise Exception(e)
        tabbase = self.app.view.panes[tabset].model.tabbase
        tid = uuid()
        logma.info(f"Widget {widget}")
        row = [name, widget, widgdata, pid, did, pos, doc_type, tabset] + tabbase + [tid]
        if in_doc is True:
            self.store.store_doc_tab(row, self.app.model.instance)
        else:
            self.store.store_app_tab(row)
        return tid

    def check_policy(self, policy, table, condition, value, db="db") -> None:
        """
            if policy == "Data Retention Policy":
                return self.check_data_retention_policy(table, condition, value, db)
            if policy == "Data Security Policy":
                return self.check_data_security_policy(table, condition, value, db)
            raise Exception(f"Policy {policy} not found")

        def check_data_retention_policy(self, table, condition, value, db="db") -> None:
        """
        policy = "Data Retention Policy"
        cfg = {"WHERE": {"EQUAL": {"type_txt": policy, "target_txt": table}}}
        data = self.store.get_app_policy(cfg, db)
        if not data.empty:
            policy = j.loads(data["policy_dict"].values[0])
            if policy.get(condition, None) == value:
                return True
        return False

    def check_data_security_policy(self, table, condition, value, db="db") -> None:
        """
            policy = "Data Security Policy"
            data = self.store.get_app_policy(table, policy, db)
            if not data.empty:
                policy = j.loads(data["policy_dict"].values[0])
                if policy.get(condition, None) == value:
                    return True
            return False

        def clear_doc_tables(self) -> None:
        """
        tables = ["doc_media", "doc_media_content", "doc_tab", "doc_tree_node", "doc_user"]
        for table in tables:
            self.store.clear_doc_table(table)
        return self

    def connect_nchantd_office(self) -> None:
        """Connect to the Nchantd Office API"""
        # need to make a connection to the Nchantd Office API
        return self

    def convert_database(self, version_from, version_to) -> None:
        """Convert database between versions"""
        # handle data updates
        return self

    def create_new_instance(self) -> None:
        """
            self.is_install_active = False
            cfg = {}
            _ = NchantdNewInstanceWizard(self, cfg).initWizard()
            [DONE]
            self.instance.set_independent()
            logma.info("Request New Instance")
            if not self.app.comms_manager.request_new_instance(self.instance.instance_id):
                self.app.comms_manager.launch_supervisor()
                if not self.app.comms_manager.request_new_instance(self.instance.instance_id):
                    raise Exception("No Supervisor Communication Bridge to Request New Instance")
            return self

        def deactivate(self, table, uuid=None, primary_key=None, db="db") -> None:
        """
        return self

    def delete_node(self, node) -> None:
        """
            logma.info(f"Node {node.nid} will be deleted")
            for tab in node.tabs:
                self.delete_tab(tab)
            self.store.delete_record("doc_tree_node", uuid=node.nid, column="nid_txt")
            return self

        def delete_tab(self, uuid=None, tab_pk=None, db="db") -> None:
        """
        # self.parent.current_tabset.remove_tab(self.app.model.current_tab.tabn)
        # if uuid is not None and tab_pk is None:
        #     tab_pk = self.store.get_primary_key("doc_tab", uuid=uuid)
        # if tab_pk is None:
        #     raise Exception(f"Tab UUID {uuid} Cannot be Deleted {tab_pk}")
        self._delete_record("doc_tab", uuid=uuid, column="tid_txt", db=db)
        cfg = {}
        self.store_event("NONACTIVE", "DeleteTab", cfg)
        self.has_changed = True
        return self

    def export_instance(self) -> None:
        """
            self.instance.set_instance_external()
            self.init_database_instance(self.instance.instance)

        def extension_config(self) -> None:
        """
        if self.config.dikt["dstruct"]["extensions"] is not None:
            for extension, details in self.config.dikt["dstruct"]["extensions"].items():
                if details["active"]:
                    self._activate_extension(extension, details)

    def generate_paths(self) -> None:
        """
        [DONE] where this method lives...could be moved to NchantdStore or NchantdApplicationStartupWizard
        :return:
        """
        data = {"<[application_slug]>": self.slug, "<[user_home]>": self.home}
        path = self.config.dikt["dstruct"]["filesystem"][self.os_type].get("application", "").get("path", "")
        self.application_path = Mechanism(path, data).run()
        data = {"<[application_slug]>": self.slug, "<[user_home]>": self.home}
        path = self.config.dikt["dstruct"]["filesystem"][self.os_type].get("config", "").get("path", "")
        self.config_path = Mechanism(path, data).run()
        data = {"<[application_slug]>": self.slug, "<[user_home]>": self.home}
        path = self.config.dikt["dstruct"]["filesystem"][self.os_type].get("library", "").get("path", "")
        self.library_path = Mechanism(path, data).run()
        # data = {"<[application_slug]>": self.slug, "<[user_home]>": self.home}
        # path = self.config.dikt["dstruct"]["filesystem"][self.os_type].get("shortcut", "").get("path", "")
        # self.shortcut_path = Mechanism(path, data).run()
        self.shortcut_path = ""  # self.config_path + "shortcuts/" + self.slug + ".lnk"
        data["<[application_icon]>"] = "launch_icon"
        path = self.config.dikt["dstruct"]["filesystem"][self.os_type].get("icon", "").get("path", "")
        self.icon_path = Mechanism(path, data).run()
        return [self.application_path, self.config_path, self.library_path, self.shortcut_path, self.icon_path]

    def get_current_node(self, pane="left") -> None:
        """"""
        node = self.app.view.panes[pane].tree.model.current_node
        return node

    def get_current_tab(self, pane="center") -> None:
        """"""
        tab = self.app.view.panes[pane].model.current_tab
        return tab

    def get_current_version(self) -> None:
        """"""
        df = self.store.get_app_version()
        logma.info(f"Current Version {df}")
        if df.empty:
            return "0.0.1.0.1.3"
        else:
            try:
                return df.iloc[0]["version_txt"]
            except Exception as e:
                logma.warning(f"Cannot Get Current Version {e}")
                return "0.0.1.0.1.3"

    def get_instance(self, instance_id=None) -> None:
        """"""
        return self.store.get_app_instance(instance_id)

    def get_instance_recent(self) -> None:
        """
            instance = self.get_instance_recents(1)
            if len(instance) == 0:
                instance = None
            else:
                instance = instance[0]
            self.create_instance(instance)
            return self

        def get_instance_recents(self, last=10) -> None:
        """
        instances = self.store.get_app_instance(most_recent=last)
        if instances.empty:
            return []
        instances = instances.to_list(orient="records")
        return instances

    def get_menu(self, name) -> None:
        """Get a menu from the database."""
        if name is None:
            return DataFrame()
        return self.store.get_app_menu(name)

    def find_node_in_tree(self, nid, tree_widget=None):
        """Find an existing node widget in the tree by its nid."""
        if tree_widget is None:
            tree_widget = self.app.view.panes["left"].tree

        # Search top-level items
        for i in range(tree_widget.topLevelItemCount()):
            item = tree_widget.topLevelItem(i)
            if hasattr(item, "nid") and str(item.nid) == str(nid):
                return item
            # Recursively search children
            found = self._find_node_recursive(item, nid)
            if found:
                return found
        return None

    def _find_node_recursive(self, parent_item, nid):
        """Recursively search for a node in the tree."""
        for i in range(parent_item.childCount()):
            child = parent_item.child(i)
            if hasattr(child, "nid") and str(child.nid) == str(nid):
                return child
            # Recursively search this child's children
            found = self._find_node_recursive(child, nid)
            if found:
                return found
        return None

    def get_node(self, nid=None, tree=None) -> None:
        """Get a node from the database."""
        # logma.info(f"Get Node {nid}")
        table = "vw_tree_node"
        # logma.info(f"Node {nid}")
        cfg = {"WHERE": {"EQUAL": {"pid_txt": "0", "position_int": 0}}}
        if nid is not None:
            cfg["WHERE"] = {"IN": {"nid_txt": [str(nid)]}}
        nodes = next(self.store.docs["db"].read({"table": table}, cfg)).dikt[table]["df"].to_dict(orient="records")
        logma.info(f"Nodes {nodes}")
        if len(nodes) == 0:
            raise Exception(f"Node {nid} not found")
        else:
            node = nodes[0]
        pnode = None
        if str(node["pid_txt"]) == "0":
            pnode = self.app.view.panes["left"].tree
        if pnode is None:
            pnode = self.app.view.panes["left"].tree.model.current_node
        # logma.info(f"PNode {pnode.parent}")
        if pnode is None:
            raise Exception("No Current Node")
        return NchantdTreeNode(pnode, node["name_txt"], node["nid_txt"], node).initWidget()

    def get_nodes(self, treeid=0) -> None:
        """"""
        table = "vw_tree_node"
        cfg = {
            "WHERE": {"EQUAL": {"treeid_txt": treeid, "visible_bit": 1}},
            "ORDER": [
                7,
            ],
        }
        return self.store.get_table(table, cfg)

    def get_policy(self, data_table, policy, db="db") -> None:
        """"""
        cfg = {"WHERE": {"EQUAL": {"type_txt": policy, "target_txt": data_table}}}
        df = self.store.get_app_policy(cfg, db)
        return df

    def get_tabs(self, node, tabset="center") -> None:
        """
            if node is None:
                return None
            filters = {"WHERE": {"IN": {"pid_txt": [node], "tabset_type_txt": [tabset]}}}
            if tabset == "right":
                filters["WHERE"]["IN"]["pid_txt"].append("0")
            filters["ORDER"] = [5]
            return self.store.get_view_tab(filters)

        def integration_config(self) -> None:
        """
        # if self.config.dikt['dstruct']['integrations'] is not None:
        # 	for integration, details in self.config.dikt['dstruct']['integrations'].items():
        # 		if details['active']:
        # 			self._activate_integration(integration, details)

    def maintain_application(self, db="db") -> None:
        """
            # self.maintain_doc_media_content()
            logma.info("Maintain Application")
            self.store.compact_instances()
            self.store.compact_database(db)
            self.store.backup_database(self.instance, db)
            return self

        def maintain_doc_media_content(self) -> None:
        """
        df = self.store.get_view_maintain_doc_media_content()
        values = df["doc_media_content_PK"].values.tolist()
        logma.info(f"Values {values}")
        self.store.delete_record("doc_media_content", primary_key=values)
        return self

    def open_instance(self, instance=None) -> None:
        """
            if instance is None:
                instance = self.get_instance_recent()
            self.parent.dbupdate.update_instance(instance)
            #
            return self

        def register_action(self, action) -> None:
        """
        self.registered_actions.append(action)
        return self

    def reload_table(self, table, keep, map_, filters={}, db="db") -> None:
        """"""
        if keep:
            logma.info(f"Copy Table {table} to temp_table")
            outcome = self.store.copy_table(table, f"temp_{table}", db)
            logma.info(f"Copy Table {table} to temp_table {outcome}"[:500])
            if not outcome:
                if debug:
                    raise Exception(f"Cannot Copy Table {table} to temp_table")
                # if not self.store.copy_table(table, f"temp_{table}", db):
                return False
        logma.info(f"Delete Table {table}")
        if not self.store.delete_table(table, db):
            logma.info(f"Cannot Delete Table {table}")
            return False
        logma.info(f"Create Table {table}")
        if not self.store.create_table(table, db):
            logma.info(f"Cannot Create Table {table}")
            return False
        if keep:
            logma.info(f"Merge Table {table} from temp_table")
            filter_ = DataFilter()
            [filter_.add_exclude(column, value) for column, value in filters.get("exclude", {}).items()]
            [filter_.add_include(column, value) for column, value in filters.get("include", {}).items()]
            if self.store.merge_table(f"temp_{table}", table, map_, filter_, db) is False:
                return False
            logma.info(f"Delete Table temp_{table}")
            # if not self.store.delete_table(f"temp_{table}", db):
            #     return False
        return True

    def remove_affiliate_links(self) -> None:
        """"""
        self.store.delete_record("links", column="type_txt", value=["base", "webapp", "affiliate"])
        return self

    def remove_data_by_date(self, table, date, direction="before", db="db") -> None:
        """
        remove data before a certain date should there be a min qty of records?

        :param table:
        :param date:
        :param direction:
        :return:

        #use mark_delete functionality
        """
        if direction == "before":
            cfg = {table: {"LESS": {"MODON_DTTM": self.time.store_now()}}}
        elif direction == "after":
            cfg = {table: {"GREATER": {"MODON_DTTM": self.time.store_now()}}}
        self.docs[db].mark_delete(cfg)

    def remove_telemetry(self, db="db") -> None:
        """
            cfg = {"telemetry": {"WHERE": {"LESS": {"CREON_DTTM": self.time.store_now()}}}}
            self.docs[db].mark_delete(cfg)

        def set_is_saved(self, saved=False) -> None:
        """
        self.is_saved = saved
        return self

    def save(self):
        """"""
        # TODO: need to implement application level save logic
        return self

    def set_instance_active(self, instance) -> None:
        """
            instance_id = instance.instance_id
            self.instances[instance_id] = instance
            self.instance = self.instances[instance_id]
            return self

        def set_paths(self) -> None:
        """
        self.app_path = join(expanduser("~"), ".local", "share", self.APP_NAME.lower())
        self.venv_path = join(self.app_path, ".venv")
        return self

    def store_cache(self, df, table) -> None:
        """
            self._store_cache(table, df, "dbc")

        def store_instance(self, instance) -> None:
        """
        self.store.store_app_instance(instance)
        return self

    def store_records(self, table, data, db="db") -> None:
        """
            self.store.store_records(table, data, db)
            return self

        def update_actions(self) -> None:
        """
        for action in self.registered_actions:
            action()
        return self

    def update_affilate_links(self, last_affilate_update_dttm: str = "2025-01-01 00:00:00", reload=False) -> None:
        """
        [DONE] where connection to the link_affiliate table
                SPLIT into affiliate links and non-affilate links
                create a link_affiliate entry for each non-affilate link
                where the affiliate exists
        :return:
        """
        API_URL = "https://nchantdoffice.com/api/"
        # client = self.mole.api.set_base_end_point(API_URL)
        if reload:
            last_affilate_update_dttm = "2025-01-01 00:00:00"
            self.remove_affiliate_links()
        params = {"since_dttm": last_affilate_update_dttm}
        # client.build_end_point(["affiliate/links/"])
        # self.update_affilate_links(client.get_end_point(params=params))
        return

    def update_node(self, node, data, db="db") -> None:
        """
            logma.info(f"Node {node.node_type} {node.nid} updated")
            if node.node_type in ("displaynode", "sysorgnode", "yearnode", "monthnode", "daynode"):
                return self
            elif node.node_type == "usernode":
                data = {"table": {"doc_tree_node": {"data": data}}}
            else:
                raise Exception(f"Node Type {node.node_type} not recognized")
            column = "nid_txt"
            value = node.nid
            self.store.update_record(data, column, value, db)
            return self

        def update_tab(self, tab, data, db="db") -> None:
        """
        logma.info(f"Tab {tab.app_data_type} {tab.tid} updated")
        if tab.app_data_type == "app":
            return self
        elif tab.app_data_type == "doc":
            data = {"table": {"doc_tab": {"data": data}}}
        else:
            raise Exception(f"Node Type {tab.tab_type} not recognized")

        column = "tid_txt"
        value = tab.tid
        self.store.update_record(data, column, value, db)
        return self

    def update_version(self, name, version, is_primary=False, db="db") -> None:
        """
            data = {"table": {"app_instance": {"data": {"version_txt": version, "is_primary_bit": is_primary}}}}
            self.store.update_record(data, "name_txt", name, db)
            return self

        def user_config(self) -> None:
        """
        if self._user_select() is None:
            self.user.create_user()
            self._user_select()
        return self

    def _activate_extension(self, extension, details) -> None:
        """

        def _activate_integration(self, integration, details) -> None:
        """

    def _archive_record(self, table, primary_key, uuid=None, column=None, db="db", flip=False) -> None:
        """
            self.store.archive_record(table, primary_key, uuid, column, db, flip)
            return self

        def _check_password_set(self) -> None:
        """
        if self.internal_password == self.password:
            return False
        return True

    def _delete_record(self, table, primary_key=None, uuid=None, column=None, db="db", flip=False) -> None:
        """Records are not deleted in a straight forward manner.  They are marked for deletion based on a policy
        and will then be removed during a compaction step when the policy is met."""
        policy = "Data Retention Policy"
        condition = "hold"
        value = "permanent"
        if self.check_policy(policy, table, condition, value, db):
            # tables with a data retention policy parameter of hold = permanent can only ever be archived
            self._archive_record(table, primary_key, uuid, column, db, flip)
            return self
        value = "indefinite"
        if self.check_policy(policy, table, condition, value, db):
            # tables with a data retention policy parameter of hold = indefinite are deletable by user action but will be
            # held based ont the hold window for the particular table in a deactivated state
            self.store.delete_record(table, primary_key, uuid, column, db, flip)
        value = "limited"
        if self.check_policy(policy, table, condition, value, db):
            # tables with a data retention policy parameter of hold = limited are only deleteable through standard
            # compaction processes based on the tables hold window
            return self
        return self

    def _load_application_configs(self) -> None:
        """
            filter = {"filter": {"instance_FK": self.instance.db_instance_id}}
            data = next(self.docs["db"].read({"table": {"appoptions"}}, filter)).dikt["appoptions"]["records"]
            logma.info(f"Data {data.dikt}")

        def _load_password(self) -> None:
        """
        filter = {"filter": {"username": self.parent.user}}
        user_data = next(self.docs["db"].read({"table": {"appusers"}}, filter))

        filter = {"filter": {"key": ["internal_password", user_data["password"]]}}
        data = next(self.docs["db"].read({"table": {"secure_store"}}, filter))
        if data["internal_password"] is None:
            self._set_internal_password()

    def _set_internal_password(self, db="db") -> None:
        """"""
        self.internal_password = uuid()
        self.password = self.internal_password
        data = [["internal_password", self.internal_password], ["password", self.password]]
        payload = {"table": {"secure_store": {"records": data, "columns": ["key", "value"]}}}
        self.docs[db].write(payload)
        return self

    def _user_select(self) -> None:
        """"""
        table = "app_user"
        data = next(self.store.docs["db"].read({"table": table})).dikt[table]["df"]
        logma.info(f"Current Users {data}")
        if not data.empty:
            self.user.select_user(data)
            return self
        return None


class NchantdSigilModel(NchantdPantiesModel):
    """Model used for dialog windows within larger applications"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super(NchantdSigilModel, self).__init__(parent, cfg)
        self.parent = parent
        self.config = condor.Instruct(pxcfg)
        self.config.select("NchantdSigilModel").override(cfg)
        if parent:
            logger.debug(f"Parent", parent.config.dikt["args"])
            self.config.override(parent.config)
            logger.debug(f"Self", self.config.dikt["args"])
        self.listeners = {}


class NchantdModel(object):

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdModel"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self, cfg=None) -> None:
        """Initialize the model"""
        super().initModel(cfg)
        return self


class DataFilter(object):
    """Data filter for pandas DataFrames"""

    def __init__(self) -> None:
        self.includes = []
        self.excludes = []

    def add_exclude(self, column, values) -> None:
        """Add column/value pairs to exclude filter"""
        self.excludes.append((column, values))
        return self

    def add_include(self, column, values) -> None:
        """Add column/value pairs to include filter"""
        self.includes.append((column, values))
        return self

    def process(self, data) -> None:
        """Apply filters to DataFrame"""
        for column, values in self.excludes:
            data = data[~data[column].isin(values)]
        for column, values in self.includes:
            data = data[data[column].isin(values)]
        return data


# ===========================Code Source Examples================================||
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
