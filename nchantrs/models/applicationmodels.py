from typing import Any, Optional


from os.path import dirname, join, expanduser
from os import environ
import platform
import json as j
from pandas import DataFrame
from kahndor import kahndor
from subtrix.subtrix import Mechanism
from subtrix.utilities import uuid
from nchantrs.models.models import NchantdStore, NchantdInstance
from nchantrs.utilities.users import NchantdUser
from nchantrs.utilities.policies import NchantdDataPolicy
from nchantrs.widgets.items.nodes import NchantdTreeNode
from nchantrs.wizards.instances import NchantdNewInstanceWizard
from kahndor.logma import Logma
from pycurity.pyvice import Device

here = join(dirname(__file__), "")
log = False
logma = Logma(__name__)
debug = True
if not log:
    logma.off()
pxcfg = join(here, "_data_", "applicationmodels.yaml")


class NchantdPantiesModel(object):
    """
    Class representing the NchantdPantiesModel.

    :param parent: The parent object.
    :param cfg: The configuration object.
    """

    def __init__(self, parent=None, cfg=None, instance=None) -> None:
        """
        :param parent:
        :param cfg:
        """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdPantiesModel").override(parent.config).override(cfg)
        self.app = self.parent.app
        self.app_cfg = None
        self.application_path = None
        self.instance_path = None
        self.config_path = None
        self.library_path = None
        self.instance = instance
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
        self.is_private = None
        self.is_secure = None
        self.instance_cfg = None
        self.reset = None
        self.web_profiles = None

    def get_web_profiles(self) -> Any:
        """Return the app-level web profile pool, creating it on first use.

        A single shared pool owns the profiles so they outlive individual web
        views (parented to the app), and every view shares one default profile
        object at one storage path — the safe pattern that both restores
        persistence and avoids the multi-object same-path corruption.
        """
        if getattr(self, "web_profiles", None) is None:
            from nchantrs.widgets.browsers.profiles import ProfileManager

            base = self.application_path or getattr(self.store, "application_path", None) or self.home
            logma.info(f"[appmodel] creating app-level web_profiles pool | storage_base={base!r}")
            self.web_profiles = ProfileManager(self.parent, storage_base=base)
        return self.web_profiles

    def initialize_application(self) -> None:
        """
        Check requires_auth before creating user to avoid unnecessary password dialogs.
        """
        self.is_private = False
        self.is_secure = False
        self.device = Device()
        self.policy = NchantdDataPolicy(self)
        self._reset_cache()
        cfg = {}
        requires_auth = self.config.dikt.get("config", {}).get("requires_auth", False)
        if requires_auth:
            self.user = NchantdUser(self, cfg)
        self.initialize_instance()

    def initialize_instance(self, instance_object=None) -> None:
        """"""
        if instance_object is None:
            instance_object = NchantdInstance
        self.instance = instance_object(self)

    def init_model_pre(self) -> None:
        logma.info(f"init_model_pre called")
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
            self.new_account = False
            self.store.store_app_event("initialized", "application_account_created")
        else:
            self.new_account = False
            self.store.store_app_event("initialized", "application_account_selected")

    def _reset_cache(self) -> None:
        """Reset cache"""
        self.store.reset_cache()
        if hasattr(self, "menu_cache"):
            self.menu_cache.clear()


class NchantdCapeModel(NchantdPantiesModel):
    """Nchantd Cape is a model that allows for simple independant dialog applications"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdSigilModel")
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
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdCloakModel").override(cfg))
        self.store.config.override(self.config)
        self.level = self.config.dikt.get("level", "")
        self.has_library = False
        self.has_changed = False
        self.are_mini_games_active = False
        self.is_internal_server_active = False
        self.is_saved = False
        self.are_services_active = False
        self.instance = None
        self.menu_cache = {}

    def initModel(self, reset=None) -> None:
        """"""
        super().initModel(reset)
        self.connect_nchantd_office()
        return self

    def add_attachment(self, name, widgdata, pid, did, document_type, tabset_type) -> None:
        """"""
        readonly = False
        editable = True
        visible = True
        moveable = True
        row = [
            name,
            "widgets.media.documents.notes.NchantdOfficeStickyNote",
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
            parent_node = self.find_node_in_tree(pid)
            if parent_node is None:
                logma.warning(f"Parent node with nid {pid} not found in tree, using current node's parent")
                current = self.get_current_node()
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
        """"""
        if policy == "Data Retention Policy":
            return self.check_data_retention_policy(table, condition, value, db)
        if policy == "Data Security Policy":
            return self.check_data_security_policy(table, condition, value, db)
        raise Exception(f"Policy {policy} not found")

    def check_data_retention_policy(self, table, condition, value, db="db") -> None:
        """"""
        policy = "Data Retention Policy"
        cfg = {"WHERE": {"EQUAL": {"type_txt": policy, "target_txt": table}}}
        data = self.store.get_app_policy(cfg, db)
        if not data.empty:
            policy = j.loads(data["policy_dict"].values[0])
            if policy.get(condition, None) == value:
                return True
        return False

    def check_data_security_policy(self, table, condition, value, db="db") -> None:
        """"""
        policy = "Data Security Policy"
        data = self.store.get_app_policy(table, policy, db)
        if not data.empty:
            policy = j.loads(data["policy_dict"].values[0])
            if policy.get(condition, None) == value:
                return True
        return False

    def clear_doc_tables(self) -> None:
        """"""
        tables = ["doc_media", "doc_media_content", "doc_tab", "doc_tree_node", "doc_user"]
        for table in tables:
            self.store.clear_doc_table(table)
        return self

    def connect_nchantd_office(self) -> None:
        logma.info(f"connect_nchantd_office called")
        return self

    def convert_database(self, version_from, version_to) -> None:
        logma.info(f"convert_database called")
        return self

    def create_new_instance(self) -> None:
        """"""
        self.is_install_active = False
        cfg = {}
        instance = NchantdNewInstanceWizard(self, cfg).initWizard()
        if self.instance is None:
            self.instance = instance
        self.instance.set_independent()
        logma.info("Request New Instance")
        if not self.app.comms_manager.request_new_instance(self.instance.instance_id):
            self.app.comms_manager.launch_supervisor()
            if not self.app.comms_manager.request_new_instance(self.instance.instance_id):
                raise Exception("No Supervisor Communication Bridge to Request New Instance")
        return self

    def deactivate(self, table, uuid=None, primary_key=None, db="db") -> None:
        logma.info(f"deactivate called")
        return self

    def delete_node(self, node) -> None:
        """"""
        logma.info(f"Node {node.nid} will be deleted")
        for tab in node.tabs:
            self.delete_tab(tab)
        self.store.delete_record("doc_tree_node", uuid=node.nid, column="nid_txt")
        return self

    def delete_tab(self, uuid=None, tab_pk=None, db="db") -> None:
        """"""
        self._delete_record("doc_tab", uuid=uuid, column="tid_txt", db=db)
        cfg = {}
        self.store_event("NONACTIVE", "DeleteTab", cfg)
        self.has_changed = True
        return self

    def export_instance(self) -> None:
        """"""
        self.instance.set_instance_external()
        self.init_database_instance(self.instance.instance)

    def extension_config(self) -> None:
        """"""
        if self.config.dikt["dstruct"]["extensions"] is not None:
            for extension, details in self.config.dikt["dstruct"]["extensions"].items():
                if details["active"]:
                    self._activate_extension(extension, details)

    def find_node_in_tree(self, nid, tree_widget=None) -> Optional[Any]:
        """Find an existing node widget in the tree by its nid."""
        if tree_widget is None:
            tree_widget = self.app.view.panes["left"].tree
        for i in range(tree_widget.topLevelItemCount()):
            item = tree_widget.topLevelItem(i)
            if hasattr(item, "nid") and str(item.nid) == str(nid):
                return item
            found = self._find_node_recursive(item, nid)
            if found:
                return found
        return None

    def generate_paths(self, cfg) -> None:
        """Generate the filesystem paths for this application.

        Production path:
            Reads ``dstruct.filesystem[<os_type>].<section>.path`` from the
            config and runs ``Mechanism`` to substitute the placeholder
            tokens (``<[application_slug]>``, ``<[user_home]>``, ``<[application_icon]>``).

        Test path:
            When ``cfg.get('db_path')`` is set, the override is honored
            directly — the development / CI workflow can point the
            application at a scratch directory without poking the
            production config.
        """
        if cfg.get("level", None) is not None:
            self.level = cfg.get("level")
        logma.info(f"Level {self.level}")
        data = {"<[application_slug]>": self.slug, "<[user_home]>": self.home, "level": self.level}

        # Path-override for testing: caller-supplied paths bypass the
        # ``Mechanism`` lookup.  Any subset of the 5 paths may be supplied;
        # missing ones fall through to the production path generation.
        override_path = cfg.get("db_path")
        if override_path:
            data["<[db_path]>"] = str(override_path)

        def _resolve(section: str, default: str) -> str:
            if override_path and section in ("application", "config", "library"):
                # Substitute the override path into the section's path
                # template so the dir-tree is rooted at the test dir.
                template = self.config.dikt["dstruct"]["filesystem"][self.os_type].get(section, "").get("path", "")
                return Mechanism(template, data).run()
            template = self.config.dikt["dstruct"]["filesystem"][self.os_type].get(section, "").get("path", "")
            return Mechanism(template, data).run()

        self.application_path = _resolve("application", "")
        self.config_path = _resolve("config", "")
        self.library_path = _resolve("library", "")
        self.shortcut_path = ""
        data["<[application_icon]>"] = "launch_icon"
        self.icon_path = Mechanism(
            self.config.dikt["dstruct"]["filesystem"][self.os_type].get("icon", "").get("path", ""),
            data,
        ).run()
        return [self.application_path, self.config_path, self.library_path, self.shortcut_path, self.icon_path]

    def get_current_instance(self) -> Any:
        """"""
        instances = self.store.get_app_instance()
        if instances.empty:
            raise Exception("No Instance available")
        logma.info(f"Instances {instances}")
        instance = instances.iloc[0].to_dict()
        return NchantdInstance.from_dict(instance)

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
            return "0.0.1.0.1.4"
        else:
            try:
                return df.iloc[0]["version_txt"]
            except Exception as e:
                logma.warning(f"Cannot Get Current Version {e}")
                return "0.0.1.0.1.4"

    def get_instance(self, instance_id=None) -> None:
        """"""
        return self.store.get_app_instance(instance_id)

    def get_instance_recent(self) -> None:
        """"""
        instance = self.get_instance_recents(1)
        if len(instance) == 0:
            instance = None
        else:
            instance = instance[0]
        self.create_instance(instance)
        return self

    def get_instance_recents(self, last=10) -> None:
        """"""
        instances = self.store.get_app_instance(most_recent=last)
        if instances.empty:
            return []
        instances = instances.to_list(orient="records")
        return instances

    def get_menu(self, name, refresh=False) -> None:
        """Get a menu from the database.

        Results are cached application-wide keyed by name. Pass refresh=True
        to bypass the cache for a single call, or use invalidate_menu_cache
        to drop cached entries when the underlying menu data changes.
        """
        if name is None:
            return DataFrame()
        if not refresh and name in self.menu_cache:
            return self.menu_cache[name]
        menu_df = self.store.get_app_menu(name)
        self.menu_cache[name] = menu_df
        return menu_df

    def get_node(self, nid=None, tree=None) -> None:
        """Get a node from the database."""
        table = "vw_tree_node"
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
        if pnode is None:
            raise Exception("No Current Node")
        return NchantdTreeNode(pnode, node["name_txt"], node["nid_txt"], node).initWidget()

    def get_nodes(self, treeid=0) -> None:
        """"""
        table = "vw_tree_node"
        cfg = {"WHERE": {"EQUAL": {"treeid_txt": treeid, "visible_bit": 1}}, "ORDER": [7]}
        return self.store.get_table(table, cfg)

    def get_policy(self, data_table, policy, db="db") -> None:
        """"""
        cfg = {"WHERE": {"EQUAL": {"type_txt": policy, "target_txt": data_table}}}
        df = self.store.get_app_policy(cfg, db)
        return df

    def get_tabs(self, node, tabset="center") -> None:
        """"""
        if node is None:
            return None
        filters = {"WHERE": {"IN": {"pid_txt": [node], "tabset_type_txt": [tabset]}}}
        if tabset == "right":
            filters["WHERE"]["IN"]["pid_txt"].append("0")
        filters["ORDER"] = [5]
        return self.store.get_view_tab(filters)

    def initialize_instance(self, instance_object=None):
        """"""
        if instance_object is None:
            instance_object = NchantdInstance
        cfg = {}
        instance_object(self, cfg)

    def integration_config(self) -> None:
        logma.info(f"integration_config called")
        return self

    def invalidate_menu_cache(self, name=None) -> None:
        """Invalidate the application menu cache.

        Pass a name to drop a single cached menu, or omit it to clear the
        entire cache so subsequent get_menu calls re-fetch from the store.
        """
        if name is None:
            self.menu_cache.clear()
        else:
            self.menu_cache.pop(name, None)
        return self

    def maintain_application(self, db="db") -> None:
        """"""
        logma.info("Maintain Application")
        self.store.compact_instances()
        self.store.compact_database(db)
        if self.instance is None:
            raise Exception(f"No Instance Configured")
        self.store.backup_database(self.instance, db)
        return self

    def maintain_doc_media_content(self) -> None:
        """"""
        df = self.store.get_view_maintain_doc_media_content()
        values = df["doc_media_content_PK"].values.tolist()
        logma.info(f"Values {values}")
        self.store.delete_record("doc_media_content", primary_key=values)
        return self

    def open_instance(self, instance=None) -> None:
        """"""
        if instance is None:
            instance = self.get_instance_recent()
        self.parent.dbupdate.update_instance(instance)
        return self

    def register_action(self, action) -> None:
        """"""
        self.registered_actions.append(action)
        return self

    def reload_index(self, index) -> None:
        logma.info(f"reload_index called")
        return self

    def reload_table(self, table, keep, map_, filters={}, db="db") -> None:
        """This method reloads a table allowing changes to the table strucuture and the ability to reinject the
        previous data and new data as needed.

        TODO: there is an opportunity here to stream line I'm sure however we must ensure that primary keys of the
            existing data are maintained and that new data is inserted in the correct order.

        """
        if keep:
            logma.info(f"Copy Table {table} to temp_table")
            outcome = self.store.copy_table(table, f"temp_{table}", None, db)
            logma.info(f"Copy Table {table} to temp_table {outcome}"[:500])
            if not outcome:
                if debug:
                    raise Exception(f"Cannot Copy Table {table} to temp_table")
                return False
        logma.info(f"Delete Table {table}")
        if not self.store.delete_table(table, db):
            logma.info(f"Cannot Delete Table {table}")
            return False
        logma.info(f"Create Table {table}")
        if not self.store.create_table(table, db):
            logma.info(f"Cannot Create Table {table}")
            return False
        if self.store.copy_table(table, f"new_{table}", None, db) is False:
            return False
        if not self.store.delete_table(table, db):
            logma.info(f"Cannot Delete Table {table}")
            return False
        logma.info(f"Create Table {table}")
        if not self.store.create_table(table, db, insert_data=False):
            logma.info(f"Cannot Create Table {table}")
            return False
        logma.info(f"Merge Table {table} from temp_table")
        filter_ = DataFilter()
        [filter_.add_exclude(column, value) for column, value in filters.get("exclude", {}).items()]
        [filter_.add_include(column, value) for column, value in filters.get("include", {}).items()]
        filter_.merge_on(filters.get("merge_on_columns", []))
        if keep:
            if self.store.merge_table(f"temp_{table}", table, map_, filter_, db, include_pk=True) is False:
                return False
            logma.info(f"Delete Table temp_{table}")
            if not self.store.delete_table(f"temp_{table}", db):
                return False
        if self.store.merge_table(f"new_{table}", table, map_, filter_, db) is False:
            return False
        if not self.store.delete_table(f"new_{table}", db):
            return False
        return True

    def reload_view(self, view) -> None:
        logma.info(f"reload_view called")
        return self

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
        """"""
        cfg = {"telemetry": {"WHERE": {"LESS": {"CREON_DTTM": self.time.store_now()}}}}
        self.docs[db].mark_delete(cfg)

    def set_is_saved(self, saved=False) -> None:
        """"""
        self.is_saved = saved
        return self

    def save(self) -> Any:
        """Persist the application-level state to the store.

        Walks the model graph and emits ``store_app_*`` write events for
        each mutable resource.  The write semantics are write-through:
        every call resolves to an immediate database write, so the
        caller can rely on the on-disk state matching the in-memory
        state at the return of this method.

        The ``cfg``-style write call shape (parallel ``records`` +
        ``columns``) matches squirl's ``update_record`` contract introduced
        earlier in nchantrs (see Sprint 28 commit ``db5d457``).
        """
        logma.info(f"save called")
        from nchantrs.models.models import NchantdInstance

        if self.instance is None:
            self.instance = NchantdInstance(self)
        # Write the instance row first so subsequent table writes can
        # reference the instance_id via the FK
        inst_payload = {
            "table": {
                "app_instance": {
                    "records": [
                        [
                            self.instance.instance_id,
                            self.instance.name,
                            self.instance.description,
                            self.instance.is_primary,
                            self.instance.application_NCD,
                            self.instance.application_path,
                            self.instance.instance_path,
                            self.instance.version,
                            j.dumps(self.instance.meta_data),
                        ]
                    ],
                    "columns": [
                        "instance_id_txt",
                        "name_txt",
                        "description_ltxt",
                        "is_primary_bit",
                        "application_NCD_txt",
                        "application_path_txt",
                        "instance_path_txt",
                        "version_txt",
                        "meta_data_dict",
                    ],
                }
            }
        }
        self.store.update_record(inst_payload, "instance_id_txt", self.instance.instance_id, "db")
        # Mark the model as saved so the next ``is_saved`` check returns True
        self.is_saved = True
        self.set_is_saved(True)
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
        """"""
        self._store_cache(table, df, "dbc")

    def store_instance(self, instance) -> None:
        """"""
        self.store.store_app_instance(instance)
        return self

    def store_link(self, name, url=None, tags=None) -> None:
        logma.info(f"store_link called")
        return self

    def store_records(self, table, data, db="db") -> None:
        """"""
        self.store.store_records(table, data, db)
        return self

    def update_actions(self) -> None:
        """"""
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
        if reload:
            last_affilate_update_dttm = "2025-01-01 00:00:00"
            self.remove_affiliate_links()
        params = {"since_dttm": last_affilate_update_dttm}
        return

    def update_node(self, node, data, db="db") -> None:
        """"""
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
        """"""
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
        """"""
        data = {"table": {"app_instance": {"data": {"version_txt": version, "is_primary_bit": is_primary}}}}
        self.store.update_record(data, "name_txt", name, db)
        return self

    def user_config(self) -> None:
        """"""
        if self._user_select() is None:
            self.user.create_user()
            self._user_select()
        return self

    def upgrade_instance(self, target_version: str) -> Any:
        """Upgrade the current instance to a new version.

        Writes the new version to the ``app_instance`` row and emits an
        event so the audit trail captures the migration.  The caller
        is responsible for migrating the data schemas (this is a
        metadata-only update).
        """
        logma.info(f"upgrade_instance to {target_version}")
        if self.instance is None:
            raise Exception("No Instance to upgrade")
        self.instance.version = target_version
        self.update_version(self.instance.name, target_version, self.instance.is_primary)
        return self

    def _activate_extension(self, extension, details) -> None:
        """Activate an extension by name (placeholder for the extension subsystem)."""
        logma.info(f"activate_extension {extension} {details}")
        return self

    def _archive_record(self, table, primary_key, uuid=None, column=None, db="db", flip=False) -> None:
        """Archive a record (sets ARCHIVE_BIT=1) via the store."""
        self.store.archive_record(table, primary_key, uuid, column, db, flip)
        return self

    def _check_password_set(self) -> bool:
        """Return True if the internal password has been set (i.e. differs from the placeholder)."""
        if not hasattr(self, "internal_password"):
            return False
        return self.internal_password != getattr(self, "password", None)

    def _delete_record(self, table, primary_key=None, uuid=None, column=None, db="db", flip=False) -> None:
        """Records are not deleted in a straight forward manner.  They are marked for deletion based on a policy
        and will then be removed during a compaction step when the policy is met."""
        policy = "Data Retention Policy"
        condition = "hold"
        value = "permanent"
        if self.check_policy(policy, table, condition, value, db):
            self._archive_record(table, primary_key, uuid, column, db, flip)
            return self
        value = "indefinite"
        if self.check_policy(policy, table, condition, value, db):
            self.store.delete_record(table, primary_key, uuid, column, db, flip)
        value = "limited"
        if self.check_policy(policy, table, condition, value, db):
            return self
        return self

    def _find_node_recursive(self, parent_item, nid) -> Optional[Any]:
        """Recursively search for a node in the tree."""
        for i in range(parent_item.childCount()):
            child = parent_item.child(i)
            if hasattr(child, "nid") and str(child.nid) == str(nid):
                return child
            found = self._find_node_recursive(child, nid)
            if found:
                return found
        return None

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
        self.config = kahndor.Instruct(pxcfg)
        self.config.select("NchantdSigilModel").override(cfg)
        if parent:
            logger.debug(f"Parent", parent.config.dikt["args"])
            self.config.override(parent.config)
            logger.debug(f"Self", self.config.dikt["args"])
        self.listeners = {}


class NchantdModel(object):

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdModel").override(cfg)

    def initModel(self, cfg=None) -> None:
        """Initialize the model"""
        super().initModel(cfg)
        return self


class DataFilter(object):
    """Data filter for pandas DataFrames"""

    def __init__(self) -> None:
        self.includes = []
        self.excludes = []
        self.merge_on_columns = []
        logma.info(f"DataFilter initialized")

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

    def merge_on(self, columns) -> Any:
        """Merge on columns"""
        self.merge_on_columns = columns
        return self
