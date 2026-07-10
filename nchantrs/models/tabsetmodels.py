# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""#																			||
---  #																			||
<(META)>:  #																	||
    docid:   #																	||
    name:	#																	||
    description: >  #															||

    expirary: <[expiration]>  #													||
    version: <[version]>  #														||
    path: <[LEXIvrs]>  #														||
    outline: <[outline]>  #														||
    authority: document|this  #													||
    security: sec|lvl2  #														||
    <(WT)>: -32  #																||
"""  # ||

# -*- coding: utf-8 -*-#														||
# ================================Core Modules===================================||
from os.path import abspath, dirname, join
import json as j

# ===============================================================================||
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.widgets.controls.toolboxes import NchantdToolBox
from kahndor.logma import Logma
from subtrix.utilities import uuid
from nchantrs.utilities.models import combine_records
from nchantrs.widgets.widgets import loadWidget

# ===============================================================================||
here = join(dirname(__file__), "")
log = True
debug = True
logma = Logma(__name__)
if not log:
    logma.off()

# ===============================================================================||
pxcfg = join(abspath(here), "_data_", "tabsetmodels.yaml")


class NchantdTabSetModel(pyqt.QAbstractItemModel):
    """Model class for a given tabset filled with data from both configuration
    files supplied and database sources configured in application"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdTabSetModel")
        if parent is not None:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__()
        self.new_document = None
        self.current_tab = None
        self.current_tab_index = None
        self.current_tab_has_changed = False
        self.node = None
        self.tabsets = None  # = self.config.dikt['gui']['desktop']['tabsets']
        self.tabsdata = []
        self.tab_widgets = []
        self.table = "app_tab"
        self.tabcolumns = self.config.dikt["dstruct"]["database"]["objects"]["table"][self.table]["columns"]
        self.tabbase = [0, 1, 1, 1]
        self.max_position = 0
        self.initialize_database_objects = True

    def initModel(self, create_objects=True) -> None:
        """
        :param pos: the position of the model in the layout
        :param node: the node identifier for the model (default is '1')
        :param new_instance: boolean indicating whether this is a new instance of the model (default is False)
        :return: the current instance of the class

        Initializes the model for the given position and node identifier. This method is responsible for setting up
        the necessary data structures and connections for the model. It also performs any necessary operations specific
        to the model. The `pos` parameter indicates the position of the model in the layout. The `node` parameter is
        used to identify the specific node for the model. By default, it is set to '1'. The `new_instance` parameter is
        a boolean value indicating whether this is a new instance of the model. By default, it is set to False.
        This method starts by retrieving the tabs data structure using the `getTabs` method. It then iterates over
        each tab and calls the corresponding init method based on the tab type. This is done using dynamic method
        invocation using the tab name. After processing the tabs, this method logs the tabs information if the `log`
        variable is True. The remaining code is commented out and appears to be related to database writing and cache
        management, but it is not clear what exactly is happening. It seems to be related to storing data in a database
        and initializing a view based on configuration settings. Finally, this method returns the current instance of
        the class.

        Example usage:
            model = initModel('left', '2', True)
        """
        db = "db"
        if self.parent.app.model.instance is not None:
            if self.parent.app.model.instance.internal is False:
                db = self.parent.app.model.instance.db_instance_id
        objects = combine_records(self.config.dikt["dstruct"]["database"]["objects"])
        if self.parent.app.new_application and create_objects is True:
            if "table" not in objects:
                return self
            records = objects["table"]["app_tab"]["records"]
            objects["table"]["app_tab"]["records"] = [x + self.tabbase + [uuid()] for x in records if x is not None]
            app_objects = {
                "table": {
                    "app_tab": {
                        "records": objects["table"]["app_tab"]["records"],
                        "columns": objects["table"]["app_tab"]["columns"],
                    }
                },
                "view": self.config.dikt["dstruct"]["database"]["objects"].get("view", {}),
            }
            self.parent.app.model.store.create_objects(app_objects, "db", False)
            self.config.dikt["dstruct"]["database"]["objects"]["table"]["app_tab"]["records"] = []
            self.config.dikt["dstruct"]["database"]["objects"]["table"]["app_tab"]["system_records"] = []
        if (
            self.parent.app.new_application
        ) and create_objects is True:  # or self.parent.app.new_instance) and create_objects is True:
            records = objects["table"]["doc_tab"]["records"]

            # logma.info(f"DOC TAB RECORDS {records}")
            # logma.info(f"Tabbase {self.tabbase}")

            objects["table"]["doc_tab"]["records"] = [x + self.tabbase + [uuid()] for x in records if x is not None]
            doc_objects = {
                "table": {
                    "doc_tab": {
                        "records": objects["table"]["doc_tab"]["records"],
                        "columns": objects["table"]["doc_tab"]["columns"],
                    }
                }
            }
            self.parent.app.model.store.create_objects(doc_objects, db, False)
        # node = self.getTabs(node)  #[DONE]
        # if node is None:
        #     return self
        # tabs = node[self.table]["records"]
        # # for tab in tabs:
        # [DONE]
        # # tabs += getattr(self, f"init{tab[2][tab[2].rfind('.') + 1:]}Model")(tab[3])
        # [DONE]
        # if log:
        #     logma.info(f"TABS {tabs}")
        return self

    def add_tab(self, name, pid, pos, widget, widgdata="{}", doc_type="custom_widget", tabset_type="center") -> None:
        """
        :param name: Name of the tab to be added.
        :param pid: Process ID associated with the tab.
        :param pos: Position where the tab should be added.
        :param widget: Widget associated with the tab.
        :return: The current instance of the object.
        """
        self.parent.app.model.add_tab(name, pid, pos, widget, widgdata, doc_type, tabset_type)
        return self

    def buildTabSet(self, node, tabset="center", tabsdata=None, toolbox=None) -> None:
        """Dynamically create a tabset based on configurations and data whose parent is the selected node provided
        
        Implements lazy loading: Only the active tab is fully loaded on build.
        Other tabs are created as placeholder widgets to defer loading until needed.
        """
        # Prevent recursive builds
        if hasattr(self, "_building") and self._building:
            return self
        self._building = True
        
        try:
            self.tabset = tabset
            self.current_node = node
            self.tab_widgets = []
            logma.info(f"Tabsdata {tabsdata}")
            
            # Get tabs data if not provided
            if tabsdata is None or tabsdata == []:
                tabsdata = self.get_tabs(node, tabset)
                if tabsdata is None:
                    logma.info("No tabs in the tabset")
                    return self
                if not tabsdata.empty:
                    tabsdata = [tab for tab in tabsdata.to_dict(orient="records")]
                else:
                    return self
            
            logma.info(f"Tabsdata {tabsdata}")
            self.tabsdata = tabsdata
            
            # Determine active tab position - can be overridden by subclasses
            active_tab_position = self._get_active_tab_position(node, 0)
            
            # Load tabs with lazy loading
            for tabn, tab in enumerate(self.tabsdata):
                self.load_tab(tab, tabn, tabset, active_tab_position)
            
            # Set the active tab
            self.parent.setCurrentIndex(active_tab_position)
            
        finally:
            self._building = False
        
        return self
    
    def _get_active_tab_position(self, node, default=0):
        """Get the active tab position from node parameters.
        
        Subclasses can override to customize how the active tab is determined.
        
        Args:
            node: Node object containing tab configuration
            default: Default position if not found
            
        Returns:
            Integer tab position (0-indexed)
        """
        if hasattr(node, 'parameters') and node.parameters:
            active_pos = node.parameters.get("active_tab_position", default)
            try:
                active_pos = int(active_pos)
                # Ensure within bounds
                if active_pos < 0:
                    active_pos = 0
                elif self.tabsdata and active_pos >= len(self.tabsdata):
                    active_pos = 0
                return active_pos
            except (ValueError, TypeError):
                return default
        return default

    def create_toolbox(self, parent=None, cfg=None) -> None:
        """"""
        toolbox = NchantdToolBox(parent, cfg)
        return toolbox

    def columnCount(self, arg) -> None:
        """ """
        return 0

    def delete_tab(self) -> None:
        """ """
        return self

    def get_tabs(self, node, tabset) -> None:
        """"""
        logma.info(f"Get Node Nid {node.nid} Tabset {tabset}  ")
        tabs = self.parent.app.model.get_tabs(node.nid, tabset)  # [DONE]
        return tabs

    def load_tab_set(self, tabset, active_tab_position=0) -> None:
        """"""
        for tabn, tab in enumerate(self.tabsdata):
            self.load_tab(tab, tabn, tabset, active_tab_position)
        # self.parent.reconnect_tabs()
        self.parent.setCurrentIndex(self.current_node.tab_focus)
        return self

    def load_tab(self, tab, tabn=0, tabset="center", active_tab_position=0) -> None:
        """"""
        if tabn in self.tab_widgets and self.tab_widgets[tabn].dummy is True:
            self.parent.remove_tab(tabn)
        if tabn == tabn:  # using the dummy widget in tabs is problematic not sure how to make it work properly
            logma.info(f"Loading Tab {tab}")
            self.tab_widgets.insert(tabn, self.load_widget(self.parse_widget_data(tab), tabset, tab))
            self.tab_widgets[tabn].dummy = False
        else:
            self.tab_widgets.insert(tabn, pyqt.QWidget(self.parent))
            self.tab_widgets[tabn].dummy = True
        self.tab_widgets[tabn].position = tabn  # TODO move into tab
        self.tab_widgets[tabn].name = tab.get("name", tab.get("name_txt", None))
        _type = tab.get("tab_type", tab.get("tab_type_txt", None))
        self.tab_widgets[tabn].type = _type[-len(_type) + _type.rfind("_") + 1 :]
        if tabset == "right":
            if self.tab_widgets[tabn].name == "ToolBox":
                self.parent.app.toolbox = self.tab_widgets[tabn]
                self.parent.app.toolbox.position = tabn
        self.parent.insertTab(tabn, self.tab_widgets[tabn], self.tab_widgets[tabn].name)
        return self

    def load_widget(self, cfg, tabset="center", document=None, tab_type="custom_widget") -> None:
        """"""
        if document is None:
            document = {}
        cfg["widget"] = document.get("widget", document.get("widget_txt", None))
        cfg["tid"] = document.get("tid", document.get("tid_txt", None))
        cfg["apps"] = self.parent.app.config.dikt.get("apps", ["nchantrs", self.parent.app.application_name.lower()])
        cfg["app"] = self.parent.app.application_name.lower()
        cfg["pos"] = tabset
        cfg["document"] = document
        tabW = loadWidget(self.parent, cfg)
        return tabW

    def parse_widget_data(self, tab) -> None:
        """"""
        cfg = tab.get("widgdata_dict", "{}")
        if isinstance(cfg, str):
            logma.info(f"TAB WIDGDATA {cfg}")
            cfg = j.loads(cfg.replace("'", '"'))
        cfg["tab"] = tab
        cfg["file_path"] = cfg.get("file_path", cfg.get("path", ""))  # TODO refactor source
        return cfg

    def rowCount(self, arg) -> None:
        """ """
        return 0

    def save_tab(self) -> None:
        """"""

    def update_position(self, from_index, to_index) -> None:
        """"""
        logma.info(f"From Index {from_index} To Index {to_index}")
        if from_index == to_index:
            return self
        self.tab_widgets.insert(to_index, self.tab_widgets.pop(from_index))
        [x.update_position(i) for i, x in enumerate(self.tab_widgets)]
        return self

    def set_active_tab(self, tabset) -> None:
        """"""
        tabset = "error"
        if tabset == "center":
            tabn = self.parent.active_node.current_tab
        elif tabset == "right":
            tabn = self.parent.active_node.recent_right_tab
        else:
            tabn = len(self.tabs) - 1
        self.parent.setCurrentIndex(tabn)
        return self


# ===========================Code Source Examples================================||
"""
"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
